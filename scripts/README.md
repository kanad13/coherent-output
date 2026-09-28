# Scripts

- [deploy.sh](deploy.sh) is the shell entry point for installation.
- [deploy.py](deploy.py) renders local configuration and installs the adapter links using the Python standard library.
- [test_deploy.py](test_deploy.py) exercises temporary checkouts and simulated home directories without touching installed applications.

```bash
./scripts/deploy.sh --dry-run
./scripts/deploy.sh --check
python3 scripts/test_deploy.py
```

The installer stops before changing destinations when it finds unknown existing content. `--backup-conflicts` explicitly preserves and replaces that content. See the [Mac setup guide](../docs/020-mac-setup.md) for backup locations and recovery.

Return to the [repository overview](../README.md).
