# Dev Container Template: Markdown + Python + Node

This folder contains the configuration for a VS Code Dev Container. It is designed as a "portable environment" that can be dropped into any project to provide a consistent workspace with Python, Node.js, and Markdown tools.

## File Map & Purpose

| File                | Purpose                                                                    | Why it’s here                                                                                            |
| ------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `devcontainer.json` | The Brain. Configures VS Code settings, extensions, and the build process. | It orchestrates how the container starts and what extensions are pre-installed.                          |
| `Dockerfile`        | The Skeleton. Defines the OS-level environment.                            | Uses the "Universal" image (Omni-base) but allows you to `apt-get` system tools like `tree` or `pandoc`. |
| `package.json`      | Node/JS Deps. Manages Node.js utilities.                                   | Used for JS-based tools (e.g., `figlet` for banners, `prettier` for formatting).                         |
| `requirements.txt`  | Python Deps. Manages Python libraries.                                     | Used for Python-based logic (e.g., `cowsay`, `pandas`, or automation scripts).                           |
| `welcome.sh`        | Health Check. A script that runs once the container is ready.              | It visually confirms the shell, Node, and Python are all working correctly.                              |

## Updating Dependencies

- **Python:** Add new libraries to `.devcontainer/requirements.txt`.
- **Node.js:** Add new packages to `.devcontainer/package.json`.
- **System/OS:** Add `apt-get install` commands to the `Dockerfile`.
- **Note:** After changing these files, run the command **Dev Containers: Rebuild Container** to apply changes.

## Using with Project-Root Files

If your project already has a `requirements.txt` or `package.json` in the root folder, you have two choices:

1. **Project Files take precedence:** Keep your project-root files and delete the contents of `.devcontainer/requirements.txt` and `.devcontainer/package.json`.
2. **Dev Container Files take precedence:** Keep the `.devcontainer` files as the source of truth and remove or ignore the project-root files.

## Keeping Files "Empty"

If you don't need specific Python or Node packages for a project, do not delete the files. Instead:

- `requirements.txt`: Leave it empty or keep a "dummy" package like `cowsay`.
- `package.json`: Keep the basic structure `{ "name": "...", "dependencies": {} }`.
- **Why?** The `devcontainer.json` expects these files to exist to complete the build. If they are missing, the build will fail.

## The "All Good" Test

Upon a successful build, the `welcome.sh` script runs automatically. It uses `figlet` (Node) and `cowsay` (Python) to print a confirmation banner in your terminal. If you see the **"READY!"** banner, your environment is fully functional.
