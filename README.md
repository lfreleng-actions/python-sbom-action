<!--
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation
-->

# 🐍📋 Python SBOM Generator Action

A comprehensive GitHub Action that generates CycloneDX Software Bill of
Materials (SBOM) reports for Python projects with automatic detection and
support for different Python dependency management tools.

## python-sbom-action

## 🚀 Features

- **Multi-tool Support**: Automatically detects and works with:
  - [uv](https://github.com/astral-sh/uv) (uv.lock)
  - [PDM](https://pdm.fming.dev/) (pdm.lock)
  - [Poetry](https://python-poetry.org/) (poetry.lock)
  - [Pipenv](https://pipenv.pypa.io/) (Pipfile.lock)
  - [pip-tools](https://github.com/jazzband/pip-tools) (requirements.txt
    with hashes)
  - Plain pip (requirements.txt)

- **Smart Detection**: Automatically identifies the dependency management tool
  used in your project
- **Supported Formats**: Generate SBOM in JSON, XML, or both
- **Flexible Configuration**: Control inclusion of development dependencies,
  output formats, and more
- **Comprehensive Validation**: Validates generated SBOM files for correctness
- **Rich Outputs**: Provides detailed information about the generated SBOMs

## 📋 Quick Start

### Basic Usage

```yaml
name: "Generate SBOM"
on: [push]
jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: "Generate SBOM"
        uses: lfreleng-actions/python-sbom-action@v1
```

### With Artifact Upload

```yaml
name: "SBOM Generation"
on: [push]
jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: "Generate SBOM"
        id: sbom
        uses: lfreleng-actions/python-sbom-action@v1
        with:
          include_dev: "false"
          sbom_format: "both"

      - name: "Upload SBOM artifacts"
        uses: actions/upload-artifact@v4
        with:
          name: sbom-files
          path: |
            sbom-cyclonedx.json
            sbom-cyclonedx.xml
          retention-days: 90

      - name: "Summary"
        run: |
            echo "SBOM count: ${{ steps.sbom.outputs.component_count }}"
            echo "Tool used: ${{ steps.sbom.outputs.dependency_manager }}"
```

### Advanced Configuration with Custom Output Directory

```yaml
steps:
  - name: "Generate SBOM with dev dependencies"
    uses: lfreleng-actions/python-sbom-action@v1
    with:
      python_version: "3.11"
      include_dev: "true"
      sbom_format: "json"
      sbom_spec_version: "1.6"
      path_prefix: "src/myproject"           # Source code location
      output_directory: "reports"            # Custom report location
      filename_prefix: "my-project-sbom"

  - name: "Upload SBOM artifacts"
    uses: actions/upload-artifact@v4
    with:
      name: sbom-files
      path: reports/my-project-sbom.json
```

## 📥 Inputs

<!-- markdownlint-disable MD013 -->

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `python_version` | No | `3.12` | Python version for SBOM generation |
| `include_dev` | No | `false` | Include dev dependencies in SBOM |
| `sbom_format` | No | `both` | SBOM format: 'json', 'xml', or 'both' |
| `sbom_spec_version` | No | `1.5` | CycloneDX specification version |
| `filename_prefix` | No | `sbom-cyclonedx` | Base filename for SBOM output |
| `path_prefix` | No | `.` | Directory location containing project code |
| `output_directory` | No | `.` | Directory location to write SBOM reports |
| `fail_on_error` | No | `true` | Fail action if SBOM generation fails |

<!-- markdownlint-enable MD013 -->

### Input Parameter Notes

- **`path_prefix` vs `output_directory`**: These parameters serve different
purposes. `path_prefix` specifies where your Python project source code is,
while `output_directory` specifies where the SBOM/report files get saved.
This allows you to generate SBOMs from source code in one directory
and write the reports to another location.

- **`filename_prefix`**: This parameter sets the base filename for SBOM outputs
(without file extension). For example, `filename_prefix: "my-app"` will
generate `my-app.json` and `my-app.xml` files. The action automatically
appends the appropriate extensions based on the `sbom_format` setting.

## 📤 Outputs

<!-- markdownlint-disable MD013 -->

| Name | Description |
|------|-------------|
| `sbom_json_path` | Full path to generated JSON SBOM file |
| `sbom_xml_path` | Full path to generated XML SBOM file |
| `dependency_manager` | Detected Python dependency manager |
| `component_count` | Number of components found in the generated SBOM |

<!-- markdownlint-enable MD013 -->

## 🛠️ Supported Tools & Detection

### Detection Priority

The action detects dependency management tools in the following priority order:

1. **uv** - `uv.lock` present
2. **PDM** - `pdm.lock` present
3. **Poetry** - `poetry.lock` present
4. **Pipenv** - `Pipfile.lock` present
5. **pip-tools** - `requirements.txt` with `requirements.in` or version pins
6. **pip** - Plain `requirements.txt` (fallback)

### Tool-Specific Behavior

<!-- markdownlint-disable MD013 -->

| Tool | Lock File | Install Command | Dev Dependencies |
|------|-----------|-----------------|------------------|
| uv | `uv.lock` | `uv sync --locked [--no-dev]` | Via `include_dev` |
| PDM | `pdm.lock` | `pdm sync [--prod] --no-self` | Via `include_dev` |
| Poetry | `poetry.lock` | `poetry install --no-root` | Via `include_dev` |
| Pipenv | `Pipfile.lock` | `pipenv install --deploy` | Via `include_dev` |
| pip-tools | `requirements.txt` | `pip install -r requirements.txt` | Via dev |
| pip | `requirements.txt` | `pip install -r requirements.txt` | Via dev |

<!-- markdownlint-enable MD013 -->

## 📚 Usage Examples

### Tool-Specific Examples

#### uv Projects

```yaml
# For projects with uv.lock
- name: "Generate SBOM (uv project)"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    python_version: "3.12"
    include_dev: "false"  # Excludes dev dependencies for production SBOM
```

#### PDM Projects

```yaml
# For projects with pdm.lock
- name: "Generate SBOM (PDM project)"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    python_version: "3.11"
    include_dev: "true"   # Include dev dependencies
    sbom_format: "json"   # JSON format for CI integration
```

#### Poetry Projects

```yaml
# For projects with poetry.lock
- name: "Generate SBOM (Poetry project)"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    include_dev: "true"
    filename_prefix: "poetry-sbom"
```

#### Pipenv Projects

```yaml
# For projects with Pipfile.lock
- name: "Generate SBOM (Pipenv project)"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    sbom_spec_version: "1.6"
    fail_on_error: "false"  # Continue on errors
```

#### pip-tools Projects

```yaml
# For projects with requirements.txt + requirements.in
- name: "Generate SBOM (pip-tools project)"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    include_dev: "true"  # Will use requirements-dev.txt if present
```

#### Plain pip Projects

```yaml
# For projects with requirements.txt files
- name: "Generate SBOM (pip project)"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    fail_on_error: "false"  # Recommended for pip projects
```

### Advanced Patterns

#### Path Prefix and Output Directory Support

```yaml
name: "SBOM with Path Prefix and Custom Output"
on: [push]
jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: "Generate SBOM for project in subdirectory"
        uses: lfreleng-actions/python-sbom-action@v1
        with:
          path_prefix: "backend/api"          # Where the source code is
          output_directory: "sbom-reports"    # Where to write SBOM files
          filename_prefix: "api-sbom"         # Creates api-sbom.json
          sbom_format: "json"

      - name: "Upload SBOM"
        uses: actions/upload-artifact@v4
        with:
          name: api-sbom
          path: sbom-reports/api-sbom.json
```

#### Filename Prefix Examples

```yaml
# Different filename prefixes create different output files
- name: "Generate SBOMs with custom names"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    filename_prefix: "my-app-v1.2.3"       # Creates: my-app-v1.2.3.json, my-app-v1.2.3.xml
    sbom_format: "both"

- name: "Generate timestamped SBOM"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    filename_prefix: "sbom-${{ github.sha }}"  # Creates: sbom-abc123def.json
    sbom_format: "json"
```

#### Monorepo Support with Centralized Reports

```yaml
name: "Multi-project SBOM"
on: [push]
jobs:
  sbom:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        project: [api, worker, dashboard, shared]
    steps:
      - uses: actions/checkout@v4

      - name: "Generate SBOM for ${{ matrix.project }}"
        id: sbom
        uses: lfreleng-actions/python-sbom-action@v1
        with:
          path_prefix: "./${{ matrix.project }}"          # Source code location
          output_directory: "sbom-reports"                # Centralized report location
          filename_prefix: "sbom-${{ matrix.project }}"
          include_dev: "false"

      - name: "Upload ${{ matrix.project }} SBOM"
        uses: actions/upload-artifact@v4
        with:
          name: sbom-${{ matrix.project }}
          path: sbom-reports/sbom-${{ matrix.project }}.*

      - name: "Summary for ${{ matrix.project }}"
        run: |
          echo "Generated SBOM for ${{ matrix.project }}"
          echo "Tool: ${{ steps.sbom.outputs.dependency_manager }}"
          echo "Components: ${{ steps.sbom.outputs.component_count }}"
```

#### Integration with Security Scanning

```yaml
name: "SBOM + Security Scan"
on: [push]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: "Generate SBOM"
        id: sbom
        uses: lfreleng-actions/python-sbom-action@v1
        with:
          sbom_format: "json"
          include_dev: "false"
          output_directory: "security-reports"

      - name: "Security scan with Grype"
        uses: anchore/scan-action@v3
        with:
          path: "${{ steps.sbom.outputs.sbom_json_path }}"
          format: "cyclonedx-json"
```

#### Release Automation with Custom Output

```yaml
name: "Release with SBOM"
on:
  release:
    types: [published]
jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: "Generate production SBOM"
        uses: lfreleng-actions/python-sbom-action@v1
        with:
          include_dev: "false"
          sbom_format: "both"
          sbom_spec_version: "1.6"
          output_directory: "release-artifacts"
          filename_prefix: "production-sbom"

      - name: "Attach SBOM to release"
        uses: softprops/action-gh-release@v1
        with:
          files: |
            release-artifacts/production-sbom.json
            release-artifacts/production-sbom.xml
```

#### Scheduled SBOM Updates

```yaml
name: "Weekly SBOM Update"
on:
  schedule:
    - cron: "0 2 * * 1"  # Monday 2 AM UTC
  workflow_dispatch:

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: "Generate weekly SBOM"
        id: sbom
        uses: lfreleng-actions/python-sbom-action@v1

      - name: "Upload current SBOM"
        uses: actions/upload-artifact@v4
        with:
          name: sbom-cyclonx
          path: sbom-cyclonedx.*
          retention-days: 30
```

### Error Handling

#### Graceful Error Handling

```yaml
- name: "Generate SBOM with error handling"
  id: sbom
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    fail_on_error: "false"
  continue-on-error: true

- name: "Handle SBOM generation failure"
  if: steps.sbom.outcome == 'failure'
  run: |
    echo "::warning::SBOM generation failed, continuing without SBOM"
    echo "SBOM generation failed" >> $GITHUB_STEP_SUMMARY
```

#### Conditional Generation

```yaml
name: "Conditional SBOM"
on: [push, pull_request]
jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: "Check for Python project"
        id: check
        run: |
          if [[ -f "pyproject.toml" || -f "requirements.txt" || \
                -f "Pipfile" ]]; then
            echo "is_python=true" >> $GITHUB_OUTPUT
          else
            echo "is_python=false" >> $GITHUB_OUTPUT
          fi

      - name: "Generate SBOM"
        if: steps.check.outputs.is_python == 'true'
        uses: lfreleng-actions/python-sbom-action@v1
        with:
          fail_on_error: "false"
```

## 🔧 Implementation Details

### SBOM Generation Process

1. **Detection**: Scans for supported dependency files in priority order
2. **Tool Setup**: Installs the detected dependency management tool
3. **Dependency Installation**: Installs dependencies according to lock files
4. **SBOM Generation**: Uses CycloneDX Python library to generate SBOM from
   environment
5. **Validation**: Validates generated SBOM files for correctness
6. **Outputs**: Provides paths and metadata about generated files

### CycloneDX Integration

The action uses the
[CycloneDX Python library](https://github.com/CycloneDX/cyclonedx-python)
to generate SBOMs by analyzing the Python environment after dependency
installation. This approach ensures the SBOM accurately reflects the resolved
dependency tree.

### Error Handling and Recovery

- **Graceful Degradation**: Can continue on errors when `fail_on_error: false`
- **Comprehensive Logging**: Detailed output for troubleshooting
- **Validation**: Built-in SBOM file validation with helpful error messages

## 🔍 Troubleshooting

### Common Issues

#### No supported dependency files found

- Ensure your project has one of the supported lock/requirements files
- Check that the file is in the `path_prefix` directory specified

#### Tool installation fails

- Verify the Python version is compatible with your dependency manager
- Check if there are any conflicting system packages

#### SBOM generation fails

- Ensure all dependencies install without errors
- Check for missing system dependencies required by Python packages
- Try with `fail_on_error: false` to get more diagnostic information

### Debug Mode

Set `fail_on_error: false` to enable verbose error handling and continue
execution when errors occur.

```yaml
- name: "Generate SBOM (debug mode)"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    fail_on_error: "false"
  env:
    ACTIONS_STEP_DEBUG: true
    RUNNER_DEBUG: 1
```

## 📋 Best Practices

### 1. Pin Action Versions

```yaml
# Good: Pin to specific version
uses: lfreleng-actions/python-sbom-action@v1.2.3

# Better: Pin to commit SHA for security
uses: lfreleng-actions/python-sbom-action@a1b2c3d4...
```

### 2. Appropriate Triggers

```yaml
# Trigger on dependency changes
on:
  push:
    paths:
      - "pyproject.toml"
      - "*.lock"
      - "requirements*.txt"
      - "Pipfile.lock"
```

### 3. Retention Policies

```yaml
# Short retention for PR builds
- name: "Upload SBOM (PR)"
  if: github.event_name == 'pull_request'
  uses: actions/upload-artifact@v4
  with:
    retention-days: 7

# Longer retention for main branch
- name: "Upload SBOM (main)"
  if: github.ref == 'refs/heads/main'
  uses: actions/upload-artifact@v4
  with:
    retention-days: 90
```

### 4. Output Directory Organization

```yaml
# Organize SBOMs by environment/purpose
- name: "Generate production SBOM"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    include_dev: "false"
    output_directory: "sbom/production"
    filename_prefix: "app-prod"

- name: "Generate development SBOM"
  uses: lfreleng-actions/python-sbom-action@v1
  with:
    include_dev: "true"
    output_directory: "sbom/development"
    filename_prefix: "app-dev"
```

### 5. Resource Optimization

```yaml
jobs:
  sbom:
    runs-on: ubuntu-latest
    timeout-minutes: 15  # Reasonable timeout
    steps:
      - name: "Generate SBOM"
        uses: lfreleng-actions/python-sbom-action@v1
        with:
          python_version: "3.12"  # Use latest stable
```

## 🤝 Contributing

Contributions are welcome! Please see our contributing guidelines and code of
conduct.

## 📄 License

This project uses the Apache License 2.0. See the [LICENSE](LICENSE) file for
details.

## 🔗 Related Projects

- [CycloneDX Python](https://github.com/CycloneDX/cyclonedx-python) -
  The underlying SBOM generation library
- [SPDX SBOM Generator](https://github.com/opensbom-generator/spdx-sbom-generator):
  Alternative SBOM format
- [Syft](https://github.com/anchore/syft) - Container and filesystem SBOM
  generator
