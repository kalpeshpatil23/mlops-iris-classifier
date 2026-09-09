# Version Control Workflow — MLOps Iris Classifier

## 1. Overview

This document describes the Git-based version control workflow used for this
Machine Learning project, developed as part of MLOps Lab Experiment 2.

- **Repository:** https://github.com/kalpeshpatil23/mlops-iris-classifier
- **Primary language:** Python
- **Maintainer:** Kalpesh Patil

## 2. Branching Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, deployable code |
| `develop` | Integration branch for development |
| `feature/<name>` | Individual features or experiments |
| `conflict-demo-a` | Demonstration branch for conflict resolution |
| `conflict-demo-b` | Demonstration branch for conflict resolution |

Changes are developed in feature branches and merged into `develop`
through Pull Requests. `main` is kept stable.

## 3. Commit Convention

Commits follow the format:

`<type>: <short description>`

Examples:

- `feat: add classification report to training script`
- `docs: update README title`
- `chore: initialize project structure`
- `fix: handle missing values`
- `refactor: improve training code`

## 4. Standard Workflow

```bash
git switch develop
git pull origin develop
git switch -c feature/<short-description>

# Make changes

git add <files>
git commit -m "feat: <description>"
git push -u origin feature/<short-description>

# Create a Pull Request on GitHub
# Merge the Pull Request into develop
