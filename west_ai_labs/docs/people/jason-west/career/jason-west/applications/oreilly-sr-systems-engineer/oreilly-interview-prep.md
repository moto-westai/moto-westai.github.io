# O'Reilly Interview Prep — Senior System Engineer (Terraform/GCP)

> **Date:** Monday, Feb 23, 2026 — 9:30-10:30 AM CST
> **Format:** Zoom (862 6084 5435 / passcode: 424671)
> **Role:** Senior System Engineer, Terraform/GCP team
> **Note:** Jason previously worked at O'Reilly (let go April 2025), returning to a *different* team

---

## 🎯 Key Narrative

**The story:** 30+ years in systems engineering → built AI infrastructure company → hands-on Terraform/GCP lab with real deployed resources → ready to bring enterprise-grade IaC discipline to O'Reilly's platform team.

**Why O'Reilly again?** Different team, different role. You know the culture and company mission. This is a technical role aligned with what you've been doing daily — not a rehire into the old position.

**The Terraform lab is your ace.** You literally have a 6-phase GCP project with 29+ deployed resources. This isn't theoretical — you can talk about real `terraform apply` decisions.

---

## 💪 Strengths to Highlight

### 1. Terraform / IaC (Hands-On, Recent)
- Built `westailabs/ai-inference-lab`: 6 phases, 29+ resources, all applied
- GCP services used: VPC, Cloud Run, Load Balancer, IAM, networking
- Real cost awareness: ~$43/mo idle, knows when to tear down
- **Origin story:** Started with Vagrant → Ansible → Terraform progression
- Can speak to state management, module structure, plan/apply workflow

### 2. GCP Experience
- Cloud Run deployments, VPC networking, IAM configuration
- Load balancer setup (IP: 34.8.167.69)
- Cost optimization mindset (monitoring, right-sizing)

### 3. Systems Engineering Depth
- 30+ years across Linux, networking, containerization
- Docker expertise (compose, volumes, networking, debugging)
- Ansible for configuration management (31+ files in current project)
- systemd service management (migrated OpenClaw from container to bare metal)
- Ubuntu 24.04, kernel 6.17 — daily driver

### 4. AI/ML Infrastructure (Differentiator)
- Built Nebulus Stack: local-first AI inference platform
- GPU inference management (TabbyAPI, ExLlamaV2, vLLM)
- Understanding of AI workload requirements at infrastructure level
- O'Reilly is investing heavily in AI content — you understand the infrastructure needs

### 5. Culture Fit
- Already know O'Reilly's values, tools, processes
- No ramp-up time on company culture
- Veteran: disciplined, mission-oriented, team player

---

## 🔮 Likely Questions & Answers

### "Tell me about yourself"
> "30 years in systems engineering. After leaving O'Reilly, I founded West AI Labs — an AI infrastructure consultancy. In the process, I built production Terraform on GCP from scratch: a 6-phase lab with VPCs, Cloud Run, load balancers, IAM — 29 resources deployed and managed. I also run bare-metal Linux infrastructure with Ansible, Docker, and systemd. I'm looking to bring that hands-on IaC discipline to a team where infrastructure is the product."

### "Why come back to O'Reilly?"
> "Different team, different role. I know the company and believe in the mission. This role aligns with what I've been doing daily — Terraform, GCP, infrastructure automation. I can contribute from day one."

### "Walk me through your Terraform experience"
> "I built a multi-phase GCP project: Phase 1 networking (VPC, subnets, firewall rules), Phase 2 compute, Phase 3 Cloud Run services, Phase 4 load balancing, Phase 5 IAM/security, Phase 6 monitoring. All applied with real resources. I manage state carefully, use modules for reuse, and think about cost from the start — I know my idle cost is $43/month and I tear down what I don't need."

### "How do you handle state management?"
> "Remote state in GCS backend with locking. State is versioned. I never edit state manually — `terraform import` and `terraform state mv` when needed. For team environments, I'd advocate for Terraform Cloud or Atlantis for PR-based workflows."

### "Describe a challenging infrastructure problem you solved"
> "Migrating a production AI assistant from Docker to bare-metal systemd. Zero data loss requirement — config, credentials, databases, workspace all had to transfer intact. I wrote an Ansible-based migration plan, created the systemd service, validated with checksums, and kept a rollback path. Completed with no downtime and no data loss."

### "How do you approach security in infrastructure?"
> "Least privilege IAM, no credentials in code, secrets in vault or environment. I recently audited MCP tool security and found 118 vulnerabilities across 68 packages — I take supply chain security seriously. For Terraform, I use `checkov` or `tfsec` for policy-as-code scanning."

### "Experience with CI/CD?"
> "GitHub Actions for Terraform plan on PR, apply on merge to main. I've also used Jenkins and Cloud Build. The key is: no one runs `terraform apply` on their laptop in production — it goes through the pipeline."

### "Where do you see infrastructure going?"
> "Platform engineering is the trend — internal developer platforms that abstract infrastructure. Terraform is the IaC standard but tools like Pulumi and Crossplane are growing. AI workloads are changing infrastructure requirements — GPU scheduling, model serving, inference optimization. O'Reilly is perfectly positioned to both teach and practice this."

---

## ⚠️ Potential Concerns & How to Address

### "You were let go — what happened?"
> Keep it brief and professional. "It was a business decision. I've used the time productively — built a company, deepened my technical skills, and I'm ready to contribute to a team again."

### "You've been self-employed — will you adjust to a team?"
> "I've always worked in teams. Running my own company required even more collaboration — with clients, partners, and the open-source community. I'm looking forward to being part of a dedicated infrastructure team."

### "Your experience is broad but is it deep enough in Terraform?"
> Point to the lab. Real resources. Real state. Real costs. Not just tutorials — production-grade work.

---

## 📋 Pre-Interview Checklist

- [ ] Review your Terraform lab code (`westailabs/ai-inference-lab`)
- [ ] Have the GCP console open to show resources if asked
- [ ] Test Zoom link 15 min early
- [ ] Quiet room, good lighting, professional background
- [ ] Have questions ready for them (see below)

---

## ❓ Questions to Ask Them

1. "What does the Terraform/GCP team's current infrastructure look like? Monorepo or multi-repo?"
2. "What's the team's approach to Terraform modules — internal registry or shared modules?"
3. "How does the team handle Terraform state — Cloud backend, Terraform Cloud, or something else?"
4. "What's the deployment pipeline? PR-based plans? Atlantis? GitHub Actions?"
5. "What does on-call look like for this team?"
6. "Where is the team headed in the next 12 months — any big migrations or new services?"
7. "How does the infrastructure team interact with the AI/ML content teams?"

---

## 🧠 Technical Quick Reference

### Terraform Commands
```bash
terraform init          # Initialize providers/backend
terraform plan          # Preview changes
terraform apply         # Apply changes
terraform destroy       # Tear down
terraform state list    # Show managed resources
terraform import        # Import existing resource
terraform workspace     # Manage workspaces
```

### GCP Key Services
- **Compute:** GCE, GKE, Cloud Run, Cloud Functions
- **Networking:** VPC, subnets, firewall rules, Cloud Load Balancing, Cloud CDN
- **Storage:** GCS, Cloud SQL, BigQuery, Firestore
- **IAM:** Roles, service accounts, workload identity
- **Ops:** Cloud Monitoring, Cloud Logging, Error Reporting

### Terraform Best Practices
- Remote state with locking (GCS + DynamoDB-style)
- Modular structure: `modules/`, `environments/`
- Variables in `tfvars`, secrets in Vault
- `terraform fmt` + `terraform validate` in CI
- Policy-as-code: Sentinel, OPA, or checkov
- Tagging strategy for cost allocation

---

*Prepared by Moto | Last updated: 2026-02-18*
