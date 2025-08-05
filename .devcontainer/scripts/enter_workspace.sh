#!/bin/bash
docker exec -it "$WORKSPACE_NAME-app-1" bash -c "cd /workspaces/$WORKSPACE_NAME && exec bash"