---
name: git-ops
description: Local Git repository operations and GitHub CLI workflows. Use when the user asks to commit, branch, merge, check status, view diffs, manage repos, or any git/gh operations. Covers local git workflow, branching strategy, commit conventions, and repo maintenance.
---

# Git Operations

## Environment

- Standard `git` CLI
- GitHub CLI (`gh`) available
- Local operations focus (no remote push unless asked)

## Daily Workflow

```bash
# Status and overview
git status
git log --oneline -20
git branch -a

# Stage and commit
git add -A
git commit -m "type: description"

# Diff review
git diff
git diff --staged
git diff HEAD~1
```

## Commit Convention

Use Conventional Commits:

```
feat: add model routing endpoint
fix: resolve VRAM overflow on 30B models
docs: update API reference
refactor: extract inference client
chore: update dependencies
```

Keep messages concise. Lowercase. No period at end.

## Branching

```bash
# Create feature branch
git checkout -b feat/description

# Merge back (prefer fast-forward)
git checkout main
git merge --ff-only feat/description

# Clean up
git branch -d feat/description
```

## Useful Commands

```bash
# Find who changed a line
git blame <file>

# Search commit messages
git log --grep="keyword"

# Search code history
git log -S "search_string" --oneline

# Stash work in progress
git stash
git stash pop

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View file at specific commit
git show <commit>:<file>
```

## GitHub CLI (gh)

```bash
# Repo info
gh repo view

# List issues
gh issue list

# Create issue
gh issue create --title "title" --body "body"

# PR list
gh pr list
```

## Guidelines

- Always check `git status` before committing
- Never force push without asking the user
- Never rebase shared branches without asking
- Use descriptive branch names: `feat/`, `fix/`, `docs/`, `chore/`
- Commit workspace changes (MEMORY.md, daily notes, etc.) regularly
