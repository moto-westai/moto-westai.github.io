---
name: job-search
description: "Search and scrape job postings for Jason West (Sr.) using Scrapling. Use when running job search pipelines or finding relevant openings."
homepage: https://www.linkedin.com/in/jasonlwest/
metadata: { "openclaw": { "emoji": "💼", "requires": { "bins": ["npx"] } } }
---

# Job Search Skill

Search and scrape job postings for Jason West using Scrapling, score them against his profile, and produce ranked output with tailored resume/cover letters.

## Career Folder Structure (MANDATORY)

All career documents live under `west_ai_labs/docs/career/` using this structure:

```
career/
  {person-slug}/           # e.g. jason-west, jason-jr
    applications/
      {company-role-YYYY-MM-DD}/  # e.g. nmi-devops-2026-02-27
        resume.md
        cover-letter.md
        notes.md           # fit assessment, status, follow-up notes
    application-tracker.md
```

Rules: one folder per application, never dump in root career/, each person gets their own directory.

## When to Use

✅ **USE this skill when:**
- Running a job search pipeline
- Finding relevant openings for Jason
- Scoring job postings against Jason's profile
- Generating tailored resume or cover letter drafts

## Prerequisites

**Read the Scrapling skill first** — this skill builds on it for scraping protected job boards.

## Jason's Profile

| Field | Details |
|-------|---------|
| Experience | 25+ years IT, Navy veteran |
| Location | Springfield MO (CST) |
| Key Skills | Terraform, GCP, AWS, Python, Linux, Docker, K8s, DevOps, SRE, AI/ML |
| Salary Target | $130K+ minimum |
| Location Pref | Remote-first, or onsite: KC / STL / NW Arkansas / Tulsa / Springfield |
| Title Targets | Senior Systems Engineer, Cloud Engineer, DevOps Engineer, SRE, Infrastructure Engineer |
| Resume | `~/projects/west_ai_labs/docs/career/jason-resume-linkedin.md` |
| Output Dir | `~/projects/west_ai_labs/docs/career/` |

## Scrape Commands

### LinkedIn Job Search
```bash
npx mcporter call --stdio "scrapling mcp" stealthy_fetch \
  'url=https://www.linkedin.com/jobs/search/?keywords=senior+devops+engineer&location=Remote&f_TPR=r604800&f_SB2=2' \
  extraction_type=markdown \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'][0])"
```
> `f_TPR=r604800` = last 7 days; `f_SB2=2` = salary filter; always use `stealthy_fetch` for LinkedIn.

### Indeed Job Search
```bash
npx mcporter call --stdio "scrapling mcp" get \
  'url=https://www.indeed.com/jobs?q=senior+devops+engineer&l=Remote&fromage=7&salary=130000' \
  extraction_type=markdown \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'][0])"
```

### Customize Keywords
Swap `senior+devops+engineer` for other title targets:
- `senior+cloud+engineer`
- `senior+sre`
- `senior+infrastructure+engineer`
- `senior+systems+engineer`

## Scoring Rubric

| Factor | Weight |
|--------|--------|
| Tech stack match (Terraform, GCP, AWS, K8s, Python…) | 40% |
| Salary fit ($130K+) | 30% |
| Location / remote match | 20% |
| Company signal (size, industry, stability) | 10% |

Score each job 0–100 using the rubric.

## Output Format

**Filename:** `~/projects/west_ai_labs/docs/career/job-search-YYYY-MM-DD.md`

**Structure:**
```markdown
# Job Search — YYYY-MM-DD

## Ranked Results

| Rank | Score | Title | Company | Location | Salary | Link |
|------|-------|-------|---------|----------|--------|------|
| 1 | 87 | Senior DevOps Engineer | Acme Corp | Remote | $145K | URL |
...

## Top Job Details

### 1. Senior DevOps Engineer — Acme Corp
[Full job description summary]

**Why it fits:** ...

**Tailored resume highlights:**
- ...

**Cover letter draft:**
...
```

## Workflow

1. Scrape LinkedIn + Indeed for each title target
2. Parse and deduplicate listings
3. Score each against rubric
4. Write ranked output to `job-search-YYYY-MM-DD.md`
5. For top 3-5 jobs: add tailored resume bullet points + cover letter draft

## Notes

- Use `stealthy_fetch` for LinkedIn (always blocked otherwise)
- `get` usually works for Indeed; fallback to `stealthy_fetch` if empty
- Cross-reference Jason's resume before writing tailored content: `~/projects/west_ai_labs/docs/career/jason-resume-linkedin.md`
- Use RAG skill to pull strategy/positioning context if writing cover letters
