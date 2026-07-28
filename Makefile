# ====================================================================================
# TDoc Command Center - Master Automation & Orchestration
# ====================================================================================

PYTHON := uv run python
UV     := uv

# Suppress sub-make directory messages
MAKEFLAGS += --no-print-directory

# Sleek 256-Color Palette (Cyberpunk / Modern CLI Aesthetic)
CYAN    := \033[38;5;51m
MAGENTA := \033[38;5;198m
GREEN   := \033[38;5;46m
RED     := \033[38;5;196m
MUTED   := \033[38;5;242m
WHITE   := \033[38;5;255m
BOLD    := \033[1m
NC      := \033[0m

.PHONY: default help install format lint diagnose check-deps run clean pack-install test brand

default: help

help:
	@printf "\n"
	@printf "$(CYAN) █$(NC) $(BOLD)$(WHITE)⚡ T D O C$(NC)\n"
	@printf "$(CYAN) █$(NC) $(MAGENTA)Platform Automation Engine$(NC)\n"
	@printf "$(CYAN) │$(NC)\n"
	@printf "$(CYAN) │ $(NC)$(BOLD)❖ ARCHITECTURE$(NC)\n"
	@printf "$(CYAN) │ $(NC)$(MUTED)  Lightweight Termux diagnostics, hardware telemetry,$(NC)\n"
	@printf "$(CYAN) │ $(NC)$(MUTED)  and security isolation routing.$(NC)\n"
	@printf "$(CYAN) │$(NC)\n"
	@printf "$(CYAN) │ $(NC)$(BOLD)❖ COMMAND MATRIX$(NC)\n"
	@printf "$(CYAN) │$(NC)\n"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "install"      "Setup system & dependencies via uv"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "check-deps"   "Audit presence of uv and utilities"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "run"          "Boot the interactive telemetry HUD"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "test"         "Execute test suite via pytest"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "format"       "Auto-format Python code via ruff"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "lint"         "Run Ruff static code analysis"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "diagnose"     "linting & structural checks"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "clean"        "Flush bytecode, cache, and venv"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "pack-install" "Register global 'tdoc' execution alias"
	@printf "$(CYAN) │$(NC)\n"
	@printf "$(CYAN) ╰─$(NC) $(WHITE)FJ™ Cybertronic Systems$(NC) $(MUTED)· MMXXIV · V3.0.2$(NC)\n\n"

install:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Initializing Core Infrastructure...$(NC)\n"
	pkg install -y termux-api
	$(UV) sync
	@printf "$(GREEN) ✔$(NC) $(MUTED)Dependencies synchronized$(NC)\n\n"

check-deps:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Auditing System Dependencies...$(NC)\n"
	@if command -v termux-battery-status >/dev/null 2>&1; then \
		printf "   $(GREEN)✔$(NC) $(MUTED)termux-api$(NC)\n"; \
	else \
		printf "   $(RED)✘$(NC) $(MUTED)termux-api (Run: pkg install termux-api)$(NC)\n"; \
	fi
	@if command -v uv >/dev/null 2>&1; then \
		printf "   $(GREEN)✔$(NC) $(MUTED)uv$(NC)\n\n"; \
	else \
		printf "   $(RED)✘$(NC) $(MUTED)uv (Run: curl -LsSf https://astral.sh/uv/install.sh | sh)$(NC)\n\n"; \
	fi

lint:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Executing Static Analysis...$(NC)\n"
	$(UV) run ruff check .
	@printf "$(GREEN) ✔$(NC) $(MUTED)Linting passed cleanly$(NC)\n\n"

format:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Formatting Codebase (100-char max)...$(NC)\n"
	$(UV) run ruff format --line-length 100 .
	@printf "$(GREEN) ✔$(NC) $(MUTED)Codebase aligned$(NC)\n\n"

test:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Launching Test Suite...$(NC)\n"
	$(UV) run pytest
	@printf "$(GREEN) ✔$(NC) $(MUTED)All assertions satisfied$(NC)\n\n"

diagnose: lint
	@printf "$(CYAN) ◈$(NC) $(WHITE)Validating Operational Footprint...$(NC)\n"
	@$(PYTHON) -c "import os, sys; sys.exit(0 if os.path.exists('src/constants.py') else 1)" && \
		printf "   $(GREEN)✔$(NC) $(MUTED)Core artifacts verified$(NC)\n" || \
		(printf "   $(RED)✘$(NC) $(MUTED)Anomaly: Missing key configuration$(NC)\n" && exit 1)
	@printf "$(GREEN) ✔$(NC) $(MUTED)Diagnostic gates passed$(NC)\n\n"

run:
	@$(UV) run tdoc

clean:
	@printf "\n$(MAGENTA) ◈$(NC) $(WHITE)Purging Workspace...$(NC)\n"
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .ruff_cache .pylint.d build/ dist/ *.egg-info .venv
	@printf "$(GREEN) ✔$(NC) $(MUTED)Caches and environments flushed$(NC)\n\n"

pack-install:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Binding Global Execution Shortcut...$(NC)\n"
	@mkdir -p "$${PREFIX:-/data/data/com.termux/files/usr}/bin"
	@printf '#!/data/data/com.termux/files/usr/bin/sh\n' > "$${PREFIX:-/data/data/com.termux/files/usr}/bin/tdoc"
	@printf 'cd "%s/Termux-Doctor" && uv run tdoc "$$@"\n' "$$HOME" >> "$${PREFIX:-/data/data/com.termux/files/usr}/bin/tdoc"
	@chmod +x "$${PREFIX:-/data/data/com.termux/files/usr}/bin/tdoc"
	@printf "$(GREEN) ✔$(NC) $(MUTED)Alias bound. Executable globally as 'tdoc'$(NC)\n\n"
