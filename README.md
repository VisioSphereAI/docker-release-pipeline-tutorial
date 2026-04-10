# 🚀 Docker CI/CD Release Pipeline with GitHub Actions

## 📌 Overview

This repository demonstrates a **production-grade CI/CD pipeline** using:
- Docker
- GitHub Actions
- Artifactory (or any container registry)
- Multi-branch strategy

It supports:
- Feature → Dev → Prod promotion
- Tag-based releases
- Automated validation and gating
- Release creation and notifications

---

## 🧱 Branch Strategy

| Branch   | Purpose |
|----------|--------|
| `main`   | Production-ready code |
| `dev`    | Pre-production / staging |
| `feature/*` | Feature development |

---

## 🔄 Workflow Overview

### 1️⃣ Feature Development
- Developers push code to `feature/*` branches
- PR is created to `dev`

---

### 2️⃣ Dev Deployment (Pre-Prod Testing)

Triggered when:
- User selects `dev` environment manually

#### Steps:
1. Create a Git tag
2. Build Docker image
3. Push image to Artifactory (dev repo)
4. Create a pre-release
5. Send notification (success/failure)

---

### 3️⃣ Production Promotion

Triggered when:
- User selects `prod` environment
- Provides a release tag

#### Validations:
- ✅ Tag exists
- ✅ Docker image exists in dev registry
- ✅ Release/tag exists in GitHub

#### Steps:
1. Promote Docker image (dev → prod)
2. Create GitHub Release
3. Generate release notes
4. Create PR (`dev` → `main`)
5. Send notification

---

## 🏗️ Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── pipeline.yml
├── app/
│   └── (application code)
├── docker/
│   └── Dockerfile
├── scripts/
│   ├── build.sh
│   ├── validate.sh
│   ├── promote.sh
├── README.md
```

---

## ⚙️ GitHub Actions Workflow

### 🔹 Manual Trigger Inputs

| Input        | Description |
|-------------|------------|
| `environment` | dev / prod |
| `tag`        | Required for prod |

---

## 🐳 Docker Build

```bash
docker build -t <repo>:<tag> .
docker push <repo>:<tag>
```

---

## 🧪 Validation Logic (Prod)

- Check tag exists
- Check Docker image exists
- Check GitHub release/tag exists

Example:
```bash
./scripts/validate.sh <tag>
```

---

## 🔁 Image Promotion

Instead of rebuilding:
- Pull from dev registry
- Retag
- Push to prod registry

```bash
docker pull dev-repo/app:<tag>
docker tag dev-repo/app:<tag> prod-repo/app:<tag>
docker push prod-repo/app:<tag>
```

---

## 📢 Notifications

You can integrate:
- Email (SMTP)
- Slack
- Teams

---

## 🔐 Required Secrets

Add in GitHub Secrets:

| Secret Name | Description |
|------------|------------|
| `DOCKER_USERNAME` | Docker registry username |
| `DOCKER_PASSWORD` | Docker registry password |
| `ARTIFACTORY_URL` | Registry URL |
| `EMAIL_USERNAME` | SMTP username |
| `EMAIL_PASSWORD` | SMTP password |

---

## 📦 Sample Workflow (Simplified)

```yaml
name: CI/CD Pipeline

on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Environment"
        required: true
      tag:
        description: "Release Tag"
        required: false

jobs:
  pipeline:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Set Variables
        run: |
          echo "ENV=${{ github.event.inputs.environment }}" >> $GITHUB_ENV
          echo "TAG=${{ github.event.inputs.tag }}" >> $GITHUB_ENV

      - name: Dev Flow
        if: env.ENV == 'dev'
        run: |
          ./scripts/build.sh

      - name: Validate for Prod
        if: env.ENV == 'prod'
        run: |
          ./scripts/validate.sh $TAG

      - name: Promote to Prod
        if: env.ENV == 'prod'
        run: |
          ./scripts/promote.sh $TAG
```

---

## 🧠 Key Concepts Used

- Git branching strategy
- CI/CD pipelines
- Docker image lifecycle
- Release management
- Environment promotion

---

## 📈 Future Enhancements

- Kubernetes deployment (Helm)
- Canary deployments
- Automated rollback
- OpenTelemetry tracing

---

## 🤝 Contribution

1. Fork repo
2. Create feature branch
3. Submit PR

---

## 📄 License


---

## ⭐ Summary

This project demonstrates a **real-world Dev → Prod promotion pipeline** with:


