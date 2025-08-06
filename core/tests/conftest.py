# core/tests/conftest.py

import os
from decouple import Config, RepositoryEnv

def pytest_configure():
    # Detect project root: assumes pytest.ini and .env.test are at the same level
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    env_path = os.path.join(root_dir, ".env.test")

    if not os.path.isfile(env_path):
        raise FileNotFoundError(f"❌ .env.test not found at: {env_path}")

    # Load and override env variables from .env.test
    config = Config(repository=RepositoryEnv(env_path))
    for key, value in config.repository.data.items():
        os.environ[key] = value

    # Ensure DJANGO_SETTINGS_MODULE is set (fallback for safety)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")  # 🔁 update if needed
