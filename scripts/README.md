# Scripts

This directory contains deployment, synchronization, and automated verification scripts.

---

## 1. Script Inventory

- [deploy.sh](deploy.sh) — Shell entry point that invokes `deploy.py`.
- [deploy.py](deploy.py) — Core installer. Renders dynamic configuration templates, manages symlinks, detects conflicts, and creates backups.
- [test_deploy.py](test_deploy.py) — Integration test suite exercising isolated checkouts, conflict handling, and paths with spaces.
- [verify.sh](verify.sh) — Single-command verification runner for deployment sync, test suites, and Prettier formatting.

---

## 2. Usage

### Deployment & Sync

```bash
./scripts/deploy.sh --dry-run
./scripts/deploy.sh
./scripts/deploy.sh --check
```

### Full Verification

```bash
./scripts/verify.sh
```

Return to the [repository overview](../README.md).
