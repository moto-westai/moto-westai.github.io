import { Type } from "@sinclair/typebox";
import type { OpenClawPluginApi, AnyAgentTool } from "openclaw";
import * as fs from "fs";
import * as path from "path";

const CAMPAIGN_DIR = "/mnt/storage/JrShare/Dungeons and dragons campaign content";
const WORKSPACE_DIR = "/home/schmibbies-workstation/.openclaw/workspace";

const ALLOWED_WRITE_FILES = ["MEMORY.md", "AGENTS.md", "USER.md"];
const ALLOWED_WRITE_DIRS = ["memory/"];

export default function register(api: OpenClawPluginApi) {

    // 1. List campaign directory
    api.registerTool({
        name: "list_campaign_directory",
        description: "Lists all files and folders inside a specific directory of the D&D campaign.",
        parameters: Type.Object({
            path: Type.String({ description: "The path to list. Leave empty for root campaign folder." }),
        }),
        async execute(_id: string, params: { path: string }) {
            try {
                const targetPath = params.path ? path.join(CAMPAIGN_DIR, params.path) : CAMPAIGN_DIR;
                if (!targetPath.startsWith(CAMPAIGN_DIR)) return { content: [{ type: "text", text: "Error: Cannot access outside campaign folder." }] };
                if (!fs.existsSync(targetPath)) return { content: [{ type: "text", text: `Error: Directory '${targetPath}' does not exist.` }] };
                const files = fs.readdirSync(targetPath);
                return { content: [{ type: "text", text: `Contents of ${targetPath}:\n- ` + files.join("\n- ") }] };
            } catch (error: any) {
                return { content: [{ type: "text", text: `Failed to list directory: ${error.message}` }] };
            }
        },
    } as unknown as AnyAgentTool, { optional: true });

    // 2. Read campaign file
    api.registerTool({
        name: "read_campaign_file",
        description: "Reads the exact contents of a file in the D&D campaign directory.",
        parameters: Type.Object({
            path: Type.String({ description: "Relative path to the file, e.g. '_Notes & Lore/hohenheim-soul.md'" }),
        }),
        async execute(_id: string, params: { path: string }) {
            try {
                const targetPath = path.join(CAMPAIGN_DIR, params.path);
                if (!targetPath.startsWith(CAMPAIGN_DIR)) return { content: [{ type: "text", text: "Error: Cannot read outside campaign folder." }] };
                if (!fs.existsSync(targetPath)) return { content: [{ type: "text", text: `Error: File '${params.path}' does not exist. Try list_campaign_directory first.` }] };
                const content = fs.readFileSync(targetPath, "utf-8");
                return { content: [{ type: "text", text: `--- START OF ${params.path} ---\n${content}\n--- END OF FILE ---` }] };
            } catch (error: any) {
                return { content: [{ type: "text", text: `Failed to read file: ${error.message}` }] };
            }
        },
    } as unknown as AnyAgentTool, { optional: true });

    // 3. Read workspace file (SOUL.md, MEMORY.md, daily logs)
    api.registerTool({
        name: "read_workspace_file",
        description: "Reads a file from Hohenheim's workspace. Use for SOUL.md, MEMORY.md, AGENTS.md, WORKFLOW_AUTO.md, or memory/YYYY-MM-DD.md",
        parameters: Type.Object({
            filename: Type.String({ description: "Filename to read, e.g. 'SOUL.md' or 'memory/2026-02-25.md'" }),
        }),
        async execute(_id: string, params: { filename: string }) {
            try {
                const safe = params.filename.replace(/\.\.\/|\.\.\\/g, "");
                const targetPath = path.join(WORKSPACE_DIR, safe);
                if (!targetPath.startsWith(WORKSPACE_DIR)) return { content: [{ type: "text", text: "Error: Cannot read outside workspace." }] };
                if (!fs.existsSync(targetPath)) return { content: [{ type: "text", text: `File '${safe}' not found in workspace.` }] };
                const content = fs.readFileSync(targetPath, "utf-8");
                return { content: [{ type: "text", text: `--- ${safe} ---\n${content}` }] };
            } catch (error: any) {
                return { content: [{ type: "text", text: `Failed to read workspace file: ${error.message}` }] };
            }
        },
    } as unknown as AnyAgentTool, { optional: true });

    // 4. Write workspace file (MEMORY.md, AGENTS.md, daily logs only)
    api.registerTool({
        name: "write_workspace_file",
        description: "Writes or appends to a file in Hohenheim's workspace. Allowed files: MEMORY.md, AGENTS.md, or memory/YYYY-MM-DD.md daily logs. Use mode 'append' to add to existing content, 'overwrite' to replace.",
        parameters: Type.Object({
            filename: Type.String({ description: "Filename to write, e.g. 'MEMORY.md' or 'memory/2026-02-25.md'" }),
            content: Type.String({ description: "The content to write or append" }),
            mode: Type.String({ description: "'append' to add to file, 'overwrite' to replace entire file" }),
        }),
        async execute(_id: string, params: { filename: string; content: string; mode: string }) {
            try {
                const safe = params.filename.replace(/\.\.\/|\.\.\\/g, "");
                const targetPath = path.join(WORKSPACE_DIR, safe);

                // Safety: only allow specific files/directories
                const isAllowedFile = ALLOWED_WRITE_FILES.includes(safe);
                const isAllowedDir = ALLOWED_WRITE_DIRS.some(d => safe.startsWith(d));
                if (!isAllowedFile && !isAllowedDir) {
                    return { content: [{ type: "text", text: `Write not allowed for '${safe}'. Allowed: MEMORY.md, AGENTS.md, memory/*.md` }] };
                }
                if (!targetPath.startsWith(WORKSPACE_DIR)) {
                    return { content: [{ type: "text", text: "Error: Cannot write outside workspace." }] };
                }

                // Create memory/ dir if needed
                const dir = path.dirname(targetPath);
                if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

                if (params.mode === "append") {
                    fs.appendFileSync(targetPath, params.content, "utf-8");
                    return { content: [{ type: "text", text: `Appended to '${safe}' successfully.` }] };
                } else {
                    fs.writeFileSync(targetPath, params.content, "utf-8");
                    return { content: [{ type: "text", text: `Wrote '${safe}' successfully.` }] };
                }
            } catch (error: any) {
                return { content: [{ type: "text", text: `Failed to write workspace file: ${error.message}` }] };
            }
        },
    } as unknown as AnyAgentTool, { optional: true });

    // 5. commit_changes — parse [WRITE:filename:mode] and [REMEMBER] markers from text
    //
    // No post-processing hooks exist in the OpenClaw plugin API (confirmed by grepping src/).
    // This tool is the fallback: Hohenheim calls commit_changes with text containing markers,
    // and the plugin executes the corresponding file operations silently.
    //
    // Supported markers:
    //   [WRITE:filename:mode]\ncontent\n[/WRITE]
    //   [REMEMBER]\nfact lines\n[/REMEMBER]
    api.registerTool({
        name: "commit_changes",
        description: "Parse and execute file-write markers embedded in free-form text. Two marker types supported:\n1. [WRITE:filename:mode]...content...[/WRITE] — writes to a workspace file. mode=append|overwrite. Allowed: MEMORY.md, AGENTS.md, USER.md, memory/YYYY-MM-DD.md\n2. [REMEMBER]...lines...[/REMEMBER] — appends lines as bullet points to MEMORY.md.\nReturns a summary of operations.",
        parameters: Type.Object({
            text: Type.String({ description: "Text containing [WRITE:filename:mode]...[/WRITE] and/or [REMEMBER]...[/REMEMBER] marker blocks." }),
        }),
        async execute(_id: string, params: { text: string }) {
            const results: string[] = [];
            const ALLOWED = ["USER.md", "MEMORY.md", "AGENTS.md"];

            // Process [WRITE:filename:mode]...[/WRITE] blocks
            const writeRe = /\[WRITE:([^\]]+):([^\]]+)\]\n?([\s\S]*?)\[\/WRITE\]/g;
            let m: RegExpExecArray | null;
            while ((m = writeRe.exec(params.text)) !== null) {
                const filename = m[1].trim();
                const mode = m[2].trim();
                const fc = m[3];
                const safe = filename.replace(/\.\.\/|\.\.\\/g, "");
                const ok = ALLOWED.includes(safe) || ["memory/"].some((d: string) => safe.startsWith(d));
                if (!ok) { results.push("WRITE '" + safe + "' denied — not in allowlist."); continue; }
                const tp = path.join(WORKSPACE_DIR, safe);
                if (!tp.startsWith(WORKSPACE_DIR)) { results.push("WRITE '" + safe + "' denied — path escape."); continue; }
                try {
                    const dir = path.dirname(tp);
                    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
                    if (mode === "append") {
                        fs.appendFileSync(tp, fc, "utf-8");
                        results.push("WRITE appended to '" + safe + "'.");
                    } else {
                        fs.writeFileSync(tp, fc, "utf-8");
                        results.push("WRITE overwrote '" + safe + "'.");
                    }
                } catch (e: any) { results.push("WRITE '" + safe + "' failed: " + e.message); }
            }

            // Process [REMEMBER]...[/REMEMBER] blocks
            const remRe = /\[REMEMBER\]\n?([\s\S]*?)\[\/REMEMBER\]/g;
            let r: RegExpExecArray | null;
            while ((r = remRe.exec(params.text)) !== null) {
                const lines = r[1].split("\n").map((l: string) => l.trim()).filter(Boolean);
                if (!lines.length) continue;
                const entry = "\n### Auto-Memory\n" + lines.map((l: string) => "- " + l).join("\n") + "\n";
                const memPath = path.join(WORKSPACE_DIR, "MEMORY.md");
                try {
                    fs.appendFileSync(memPath, entry, "utf-8");
                    results.push("REMEMBER stored " + lines.length + " line(s) to MEMORY.md.");
                } catch (e: any) { results.push("REMEMBER failed: " + e.message); }
            }

            if (!results.length) {
                return { content: [{ type: "text", text: "No [WRITE] or [REMEMBER] markers found in text." }] };
            }
            return { content: [{ type: "text", text: results.join("\n") }] };
        },
    } as unknown as AnyAgentTool, { optional: true });

}
