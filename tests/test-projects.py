#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation

"""
Test project generator for Python SBOM Action

This script creates test projects with different Python dependency management tools
for manual testing of the python-sbom-action.
"""

import sys
from pathlib import Path


def create_test_project(name: str, tool: str, base_dir: Path = Path("test-projects")):
    """Create a test project for the specified tool."""
    project_dir = base_dir / name
    project_dir.mkdir(parents=True, exist_ok=True)

    print(f"Creating {tool} test project: {project_dir}")

    if tool == "uv":
        create_uv_project(project_dir)
    elif tool == "pdm":
        create_pdm_project(project_dir)
    elif tool == "poetry":
        create_poetry_project(project_dir)
    elif tool == "pipenv":
        create_pipenv_project(project_dir)
    elif tool == "pip":
        create_pip_project(project_dir)
    elif tool == "pip-tools":
        create_pip_tools_project(project_dir)
    else:
        print(f"Unknown tool: {tool}")
        return False

    return True


def create_uv_project(project_dir: Path):
    """Create a uv-based test project."""
    pyproject_content = """[project]
name = "test-uv-project"
version = "0.1.0"
description = "Test project for uv SBOM generation"
authors = [{name = "Test User", email = "test@example.com"}]
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0",
    "pydantic>=2.0.0",
    "typer>=0.9.0",
]
requires-python = ">=3.8"

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

    with open(project_dir / "pyproject.toml", "w") as f:
        f.write(pyproject_content)

    # Create a simple Python file
    with open(project_dir / "main.py", "w") as f:
        f.write("""import requests
import click

@click.command()
def hello():
    \"\"\"Simple program that greets NAME.\"\"\"
    response = requests.get("https://httpbin.org/json")
    click.echo(f"Response: {response.status_code}")

if __name__ == '__main__':
    hello()
""")

    print("  ✓ Created pyproject.toml and main.py")
    print("  → Run 'uv lock' in the project directory to create uv.lock")


def create_pdm_project(project_dir: Path):
    """Create a PDM-based test project."""
    pyproject_content = """[project]
name = "test-pdm-project"
version = "0.1.0"
description = "Test project for PDM SBOM generation"
authors = [{name = "Test User", email = "test@example.com"}]
dependencies = [
    "requests>=2.25.0",
    "fastapi>=0.100.0",
    "uvicorn>=0.20.0",
]
requires-python = ">=3.8"

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[tool.pdm]
distribution = true

[tool.pdm.dev-dependencies]
test = [
    "pytest>=7.0.0",
    "httpx>=0.24.0",
]
lint = [
    "ruff>=0.1.0",
    "black>=23.0.0",
]
"""

    with open(project_dir / "pyproject.toml", "w") as f:
        f.write(pyproject_content)

    with open(project_dir / "app.py", "w") as f:
        f.write("""from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/fetch")
async def fetch_data():
    response = requests.get("https://httpbin.org/json")
    return {"status": response.status_code, "data": response.json()}
""")

    print("  ✓ Created pyproject.toml and app.py")
    print("  → Run 'pdm lock' in the project directory to create pdm.lock")


def create_poetry_project(project_dir: Path):
    """Create a Poetry-based test project."""
    pyproject_content = """[tool.poetry]
name = "test-poetry-project"
version = "0.1.0"
description = "Test project for Poetry SBOM generation"
authors = ["Test User <test@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.25.0"
django = "^4.2.0"
psycopg2-binary = "^2.9.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
pytest-django = "^4.5.0"
black = "^23.0.0"
isort = "^5.12.0"

[tool.poetry.group.docs.dependencies]
sphinx = "^7.0.0"
sphinx-rtd-theme = "^1.3.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""

    with open(project_dir / "pyproject.toml", "w") as f:
        f.write(pyproject_content)

    with open(project_dir / "README.md", "w") as f:
        f.write("# Test Poetry Project\n\nTest project for Poetry SBOM generation.\n")

    with open(project_dir / "manage.py", "w") as f:
        f.write("""#!/usr/bin/env python
import os
import sys
import requests

def main():
    \"\"\"Run administrative tasks.\"\"\"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""")

    print("  ✓ Created pyproject.toml, README.md, and manage.py")
    print("  → Run 'poetry lock' in the project directory to create poetry.lock")


def create_pipenv_project(project_dir: Path):
    """Create a Pipenv-based test project."""
    pipfile_content = """[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = ">=2.25.0"
flask = ">=2.3.0"
gunicorn = ">=21.0.0"
redis = ">=4.5.0"

[dev-packages]
pytest = ">=7.0.0"
flask-testing = ">=0.8.1"
coverage = ">=7.0.0"
flake8 = ">=6.0.0"

[requires]
python_version = "3.8"

[scripts]
dev = "python app.py"
test = "pytest"
"""

    with open(project_dir / "Pipfile", "w") as f:
        f.write(pipfile_content)

    with open(project_dir / "app.py", "w") as f:
        f.write("""from flask import Flask, jsonify
import requests
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/')
def hello():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/fetch')
def fetch_data():
    try:
        response = requests.get("https://httpbin.org/json")
        return jsonify({"status": response.status_code, "data": response.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cache/<key>')
def get_cache(key):
    value = redis_client.get(key)
    return jsonify({"key": key, "value": value})

if __name__ == '__main__':
    app.run(debug=True)
""")

    print("  ✓ Created Pipfile and app.py")
    print("  → Run 'pipenv lock' in the project directory to create Pipfile.lock")


def create_pip_project(project_dir: Path):
    """Create a pip-based test project."""
    requirements_content = """requests>=2.31.0
flask>=2.3.0
jinja2>=3.1.0
werkzeug>=2.3.0
markupsafe>=2.1.0
itsdangerous>=2.1.0
click>=8.1.0
blinker>=1.6.0
urllib3>=2.0.0
certifi>=2023.7.0
charset-normalizer>=3.3.0
idna>=3.6
"""

    requirements_dev_content = """pytest>=7.4.0
pytest-flask>=1.3.0
coverage>=7.3.0
black>=23.12.0
flake8>=6.1.0
mypy>=1.8.0
"""

    with open(project_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)

    with open(project_dir / "requirements-dev.txt", "w") as f:
        f.write(requirements_dev_content)

    with open(project_dir / "setup.py", "w") as f:
        f.write("""from setuptools import setup, find_packages

setup(
    name="test-pip-project",
    version="0.1.0",
    description="Test project for pip SBOM generation",
    author="Test User",
    author_email="test@example.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "flask>=2.3.0",
    ],
    python_requires=">=3.8",
)
""")

    with open(project_dir / "server.py", "w") as f:
        f.write("""from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from pip-managed Flask app!"

@app.route('/proxy')
def proxy():
    url = request.args.get('url', 'https://httpbin.org/json')
    try:
        response = requests.get(url, timeout=10)
        return jsonify({
            "url": url,
            "status_code": response.status_code,
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
""")

    print("  ✓ Created requirements.txt, requirements-dev.txt, setup.py, and server.py")


def create_pip_tools_project(project_dir: Path):
    """Create a pip-tools-based test project."""
    requirements_in_content = """# Production dependencies
requests>=2.25.0
fastapi>=0.100.0
uvicorn[standard]>=0.20.0
pydantic>=2.0.0
sqlalchemy>=2.0.0
alembic>=1.12.0
"""

    requirements_dev_in_content = """# Development dependencies
-r requirements.in
pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
black>=23.0.0
isort>=5.12.0
mypy>=1.5.0
pre-commit>=3.0.0
"""

    # Generate locked requirements (simulated)
    requirements_txt_content = f"""# This file is autogenerated by pip-compile with Python {sys.version_info.major}.{sys.version_info.minor}
# To update, run:
#
#    pip-compile requirements.in
#
alembic==1.13.2
    # via -r requirements.in
annotated-types==0.7.0
    # via pydantic
anyio==4.3.0
    # via
    #   httpcore
    #   uvicorn
certifi==2024.2.2
    # via
    #   httpcore
    #   requests
charset-normalizer==3.3.2
    # via requests
click==8.1.7
    # via uvicorn
fastapi==0.110.0
    # via -r requirements.in
greenlet==3.0.3
    # via sqlalchemy
h11==0.14.0
    # via uvicorn
httpcore==1.0.4
    # via httpx
httptools==0.6.1
    # via uvicorn
httpx==0.27.0
    # via httpx
idna==3.7
    # via
    #   anyio
    #   requests
mako==1.3.2
    # via alembic
markupsafe==2.1.5
    # via
    #   jinja2
    #   mako
pydantic==2.6.4
    # via
    #   -r requirements.in
    #   fastapi
pydantic-core==2.16.3
    # via pydantic
python-dotenv==1.0.1
    # via uvicorn
python-multipart==0.0.9
    # via fastapi
pyyaml==6.0.1
    # via uvicorn
requests==2.31.0
    # via -r requirements.in
sniffio==1.3.1
    # via
    #   anyio
    #   httpcore
    #   httpx
sqlalchemy==2.0.29
    # via
    #   -r requirements.in
    #   alembic
starlette==0.36.3
    # via fastapi
typing-extensions==4.10.0
    # via
    #   alembic
    #   pydantic
    #   pydantic-core
    #   sqlalchemy
urllib3==2.2.1
    # via requests
uvicorn==0.29.0
    # via -r requirements.in
uvloop==0.19.0
    # via uvicorn
watchfiles==0.21.0
    # via uvicorn
websockets==12.0
    # via uvicorn
"""

    with open(project_dir / "requirements.in", "w") as f:
        f.write(requirements_in_content)

    with open(project_dir / "requirements-dev.in", "w") as f:
        f.write(requirements_dev_in_content)

    with open(project_dir / "requirements.txt", "w") as f:
        f.write(requirements_txt_content)

    with open(project_dir / "api.py", "w") as f:
        f.write("""from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI(title="Test API", version="0.1.0")

class HealthResponse(BaseModel):
    status: str
    version: str

class ProxyRequest(BaseModel):
    url: str
    method: str = "GET"

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", version="0.1.0")

@app.post("/proxy")
async def proxy_request(request: ProxyRequest):
    try:
        if request.method.upper() == "GET":
            response = requests.get(request.url, timeout=10)
        else:
            raise HTTPException(status_code=400, detail="Only GET method supported")

        return {
            "url": request.url,
            "method": request.method,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text[:1000]  # Limit response size
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
""")

    print(
        "  ✓ Created requirements.in, requirements-dev.in, requirements.txt, and api.py"
    )
    print("  → This project uses pip-tools (requirements.txt with hashes/pins)")


def main():
    """Main function to create all test projects."""
    if len(sys.argv) > 1:
        tools = sys.argv[1:]
    else:
        tools = ["uv", "pdm", "poetry", "pipenv", "pip", "pip-tools"]

    base_dir = Path("test-projects")
    base_dir.mkdir(exist_ok=True)

    print(f"Creating test projects in: {base_dir.absolute()}")
    print(f"Tools to create: {', '.join(tools)}")
    print()

    success_count = 0
    for tool in tools:
        project_name = f"test-{tool}-project"
        if create_test_project(project_name, tool, base_dir):
            success_count += 1
        print()

    print(f"✅ Successfully created {success_count}/{len(tools)} test projects")

    print("\n📝 Next steps:")
    print("1. Navigate to each test project directory")
    print("2. Run the appropriate lock command for each tool:")
    print("   - uv: 'uv lock'")
    print("   - pdm: 'pdm lock'")
    print("   - poetry: 'poetry lock'")
    print("   - pipenv: 'pipenv lock'")
    print("   - pip/pip-tools: lock files already provided")
    print("3. Test the python-sbom-action in each directory")

    print("\n🧪 Test the action with:")
    print("cd test-projects/test-uv-project")
    print("../../python-sbom-action (if using local action)")


if __name__ == "__main__":
    main()
