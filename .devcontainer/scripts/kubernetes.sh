// entry point to setup docker container for development
{
  "name": "Django Dev Environment",
  "settings": {
    "python.defaultInterpreterPath": "/usr/local/bin/python",
    "python.linting.pylintEnabled": true,
    "editor.formatOnSave": true
  },
  "extensions": [
    "ms-python.python", // Core Python extension
    "ms-python.debugpy", // Debugging support
    "ms-python.vscode-pylance", // Pylance for Python IntelliSense
    "VisualStudioExptTeam.vscodeintellicode", // IntelliCode for AI-assisted suggestions
    "GitHub.copilot", // GitHub Copilot for AI-powered suggestions
  ],
  "postCreateCommand": "docker compose build --no-cache && docker compose up -d",
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspaces/${localWorkspaceFolderBasename},type=bind",
  "containerEnv": {
    "WORKSPACE_NAME": "${localWorkspaceFolderBasename}"
  }
}