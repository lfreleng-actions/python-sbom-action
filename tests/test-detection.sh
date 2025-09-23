#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 The Linux Foundation

# Test script for Python dependency manager detection logic
# This script validates the detection priority and logic used in the action

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_BASE_DIR="$SCRIPT_DIR/detection-tests"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

print_header() {
    echo -e "${BLUE}🧪 Python SBOM Action - Dependency Manager Detection Tests${NC}"
    echo "=================================================================="
}

print_test() {
    local test_name="$1"
    echo -e "${YELLOW}▶ Testing: $test_name${NC}"
    ((TESTS_RUN++))
}

print_pass() {
    local message="$1"
    echo -e "${GREEN}  ✅ $message${NC}"
    ((TESTS_PASSED++))
}

print_fail() {
    local message="$1"
    echo -e "${RED}  ❌ $message${NC}"
    ((TESTS_FAILED++))
}

print_summary() {
    echo ""
    echo "=================================================================="
    echo -e "Tests run: $TESTS_RUN | ${GREEN}Passed: $TESTS_PASSED${NC} | ${RED}Failed: $TESTS_FAILED${NC}"

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed!${NC}"
        return 0
    else
        echo -e "${RED}💥 Some tests failed!${NC}"
        return 1
    fi
}

# Detection function (extracted from action.yaml logic)
detect_dependency_manager() {
    local test_dir="$1"
    local detected_tool=""
    local original_dir
    original_dir="$(pwd)"

    # Change to test directory
    if ! cd "$test_dir" 2>/dev/null; then
        echo "error"
        return 1
    fi

    # Priority order for detection (same as in action.yaml)
    if [[ -f "uv.lock" ]]; then
        detected_tool="uv"
    elif [[ -f "pdm.lock" ]]; then
        detected_tool="pdm"
    elif [[ -f "poetry.lock" ]]; then
        detected_tool="poetry"
    elif [[ -f "Pipfile.lock" ]]; then
        detected_tool="pipenv"
    elif [[ -f "requirements.txt" ]] && (grep -q "==" requirements.txt 2>/dev/null || [[ -f "requirements.in" ]]); then
        detected_tool="pip-tools"
    elif [[ -f "requirements.txt" ]]; then
        detected_tool="pip"
    else
        detected_tool="none"
    fi

    # Return to original directory
    cd "$original_dir"
    echo "$detected_tool"
}

run_test() {
    local test_name="$1"
    local expected="$2"
    local setup_function="$3"

    print_test "$test_name"

    local test_dir="$TEST_BASE_DIR/$test_name"
    mkdir -p "$test_dir"

    # Run setup function to create test files
    $setup_function "$test_dir"

    # Run detection
    local result
    result=$(detect_dependency_manager "$test_dir")

    # Check result
    if [ "$result" = "$expected" ]; then
        print_pass "Expected '$expected', got '$result'"
    else
        print_fail "Expected '$expected', got '$result'"
    fi

    # Clean up test directory
    rm -rf "$test_dir"
}

# Setup functions for different test scenarios
setup_uv() {
    local dir="$1"
    echo "# uv.lock file" > "$dir/uv.lock"
}

setup_pdm() {
    local dir="$1"
    echo "# pdm.lock file" > "$dir/pdm.lock"
}

setup_poetry() {
    local dir="$1"
    echo "# poetry.lock file" > "$dir/poetry.lock"
}

setup_pipenv() {
    local dir="$1"
    echo '{"_meta": {}, "default": {}, "develop": {}}' > "$dir/Pipfile.lock"
}

setup_pip_tools_with_in() {
    local dir="$1"
    echo "requests>=2.25.0" > "$dir/requirements.in"
    echo "requests==2.31.0" > "$dir/requirements.txt"
}

setup_pip_tools_with_pins() {
    local dir="$1"
    cat > "$dir/requirements.txt" << 'EOF'
requests==2.31.0
click==8.1.7
urllib3==2.0.7
EOF
}

setup_pip() {
    local dir="$1"
    cat > "$dir/requirements.txt" << 'EOF'
requests>=2.25.0
click>=8.0.0
flask
EOF
}

setup_empty() {
    local dir="$1"
    echo "# README" > "$dir/README.md"
}

setup_priority_uv_over_pdm() {
    local dir="$1"
    echo "# uv.lock" > "$dir/uv.lock"
    echo "# pdm.lock" > "$dir/pdm.lock"
}

setup_priority_pdm_over_poetry() {
    local dir="$1"
    echo "# pdm.lock" > "$dir/pdm.lock"
    echo "# poetry.lock" > "$dir/poetry.lock"
}

setup_priority_poetry_over_pipenv() {
    local dir="$1"
    echo "# poetry.lock" > "$dir/poetry.lock"
    echo '{"_meta": {}}' > "$dir/Pipfile.lock"
}

setup_priority_pipenv_over_pip_tools() {
    local dir="$1"
    echo '{"_meta": {}}' > "$dir/Pipfile.lock"
    echo "requests>=2.25.0" > "$dir/requirements.in"
    echo "requests==2.31.0" > "$dir/requirements.txt"
}

setup_priority_pip_tools_over_pip() {
    local dir="$1"
    echo "requests>=2.25.0" > "$dir/requirements.in"
    echo "requests==2.31.0" > "$dir/requirements.txt"
}

setup_empty_requirements() {
    local dir="$1"
    touch "$dir/requirements.txt"
}

setup_comments_requirements() {
    local dir="$1"
    cat > "$dir/requirements.txt" << 'EOF'
# This is a comment
# Another comment
EOF
}

# Main test execution
main() {
    print_header

    # Clean up and create test base directory
    rm -rf "$TEST_BASE_DIR"
    mkdir -p "$TEST_BASE_DIR"

    # Basic detection tests
    run_test "uv-detection" "uv" "setup_uv"
    run_test "pdm-detection" "pdm" "setup_pdm"
    run_test "poetry-detection" "poetry" "setup_poetry"
    run_test "pipenv-detection" "pipenv" "setup_pipenv"
    run_test "pip-tools-with-in" "pip-tools" "setup_pip_tools_with_in"
    run_test "pip-tools-with-pins" "pip-tools" "setup_pip_tools_with_pins"
    run_test "pip-detection" "pip" "setup_pip"
    run_test "no-files" "none" "setup_empty"

    # Priority tests
    run_test "priority-uv-over-pdm" "uv" "setup_priority_uv_over_pdm"
    run_test "priority-pdm-over-poetry" "pdm" "setup_priority_pdm_over_poetry"
    run_test "priority-poetry-over-pipenv" "poetry" "setup_priority_poetry_over_pipenv"
    run_test "priority-pipenv-over-pip-tools" "pipenv" "setup_priority_pipenv_over_pip_tools"
    run_test "priority-pip-tools-over-pip" "pip-tools" "setup_priority_pip_tools_over_pip"

    # Edge case tests
    run_test "empty-requirements" "pip" "setup_empty_requirements"
    run_test "comments-requirements" "pip" "setup_comments_requirements"

    # Clean up
    rm -rf "$TEST_BASE_DIR"

    print_summary
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
