
## Writing to Files

When you want to save a memory, update your notes, or write to a workspace file, use the **`commit_changes`** tool.

Pass text with one or more marker blocks:

### WRITE marker — write or append to a file

    [WRITE:MEMORY.md:append]
    ## Session Note
    - Something important I learned.
    [/WRITE]

Allowed filenames: MEMORY.md, AGENTS.md, USER.md, memory/YYYY-MM-DD.md
Modes: append (add to end) or overwrite (replace entire file)

### REMEMBER marker — append facts to MEMORY.md

    [REMEMBER]
    Jason prefers bullet summaries over long paragraphs.
    The campaign's main villain is Lord Harkon.
    [/REMEMBER]

Each non-blank line becomes a bullet point under ### Auto-Memory in MEMORY.md.

### How to use

Call commit_changes with text containing your markers:

    commit_changes({ text: "[REMEMBER]\nJason wants shorter combat descriptions.\n[/REMEMBER]" })

You can combine WRITE and REMEMBER blocks in the same call.
