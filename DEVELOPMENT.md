# Termux-Doctor Development Guide

This guide covers setup, standards, and workflow for contributing to Termux-Doctor.

## 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/your-org/Termux-Doctor.git
cd Termux-Doctor

# Install dependencies (using uv is recommended)
uv sync

# Run the project
uv run tdoc
```

## 2. Coding Standards
- **Python**: Adhere to PEP 8. Use Google-style docstrings.
- **Typing**: All parameters and return values must be explicitly typed (`mypy` compliant).
- **Style**: Line length max 100 characters. Use MVC pattern for UI components.
- **Robustness**: Utilize `src/utils/robustness.py` for transient I/O operations.

## 3. Testing & CI/CD
- **Unit Tests**: All new features require tests in `src/tests/`.
- **Execution**: Use `make test` to run the full suite (`pytest`).
- **Coverage**: Maintain > 80% test coverage.
- **CI**: GitHub Actions runs linting, type checking, and tests on push.

## 4. Contributing Workflow
1. **Branching**: Use `feature/` or `fix/` prefixes for branches.
2. **Pull Requests**: Open a PR against `main`. Ensure all tests pass.
3. **Documentation**: Update this guide, `ARCHITECTURE.md`, or `USER_GUIDE.md` as needed.
4. **Data Collection**: When adding new Android-specific checks, refer to `docs/ANDROID_COMMANDS.md`.
