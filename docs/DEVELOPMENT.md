# Termux-Doctor Development Guide

This guide covers setup, standards, and workflow for contributing to Termux-Doctor.

## 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/FJ-cyberzilla/Termux-Doctor.git
cd Termux-Doctor

# Build the project
make build

# Run the project
make run
```

## 2. Coding Standards
- **Go**: Adhere to Go idioms and formatting (`go fmt`).
- **Typing**: Ensure Go's strict type safety is maintained throughout the codebase.
- **Style**: Follow `Effective Go` guidelines. Keep functions focused and maintainable.
- **Linting/Testing**: Use `make lint` for static analysis and `make test` for comprehensive test coverage.

## 3. Testing & CI/CD
- **Unit Tests**: All new features require tests in the corresponding package (e.g., `internal/services/service_test.go`).
- **Execution**: Use `make test` to run the full test suite.
- **Coverage**: Maintain high test coverage for all diagnostic modules.
- **CI**: GitHub Actions runs linting, vet checks, and tests on push.

## 4. Contributing Workflow
1. **Branching**: Use `feature/` or `fix/` prefixes for branches.
2. **Pull Requests**: Open a PR against `main`. Ensure all tests pass (`make test`).
3. **Documentation**: Update this guide, `ARCHITECTURE.md`, or `USER_GUIDE.md` as needed.
4. **Data Collection**: When adding new Android-specific checks, refer to `docs/ANDROID_COMMANDS.md`.
