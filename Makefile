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
DIMRED  := \033[38;5;160m
MUTED   := \033[38;5;242m
WHITE   := \033[38;5;255m
ORANGE  := \033[38;5;208m
BOLD    := \033[1m
NC      := \033[0m

.PHONY: build check-deps clean diagnose format help install lint pack-install run sync test update

default: help

# ------------------------------------------------------------------------------------
# COMMAND MATRIX
# ------------------------------------------------------------------------------------

build:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Building Package...$(NC)\n"
	$(PYTHON) -m build
	@printf "$(GREEN) ✔$(NC) $(MUTED)Build successful$(NC)\n\n"

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

clean:
	@printf "\n$(MAGENTA) ◈$(NC) $(WHITE)Purging Workspace...$(NC)\n"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info .eggs .venv
	@printf "$(GREEN) ✔$(NC) $(MUTED)Caches, eggs, and environments flushed$(NC)\n\n"

diagnose: lint
	@$(PYTHON) -c "import os, sys; sys.exit(0 if os.path.exists('src/constants.py') else 1)" || exit 1

format:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Formatting Codebase (100-char max)...$(NC)\n"
	$(UV) run ruff format --line-length 100 .
	@printf "$(GREEN) ✔$(NC) $(MUTED)Codebase aligned$(NC)\n\n"

help:
	@printf "\n"
	@printf "$(CYAN) █$(NC) $(BOLD)$(WHITE)⚡ T D O C$(NC)\n"
	@printf "$(CYAN) █$(NC) $(ORANGE)Platform Automation Engine$(NC)\n"
	@printf "$(CYAN) │$(NC)\n"
	@printf "$(CYAN) │ $(NC)$(BOLD)❖ ARCHITECTURE$(NC)\n"
	@printf "$(CYAN) │ $(NC)$(DIMRED)  Termux diagnostic and telemetry suite.$(NC)\n"
	@printf "$(CYAN) │$(NC)\n"
	@printf "$(CYAN) │ $(NC)$(BOLD)❖ COMMAND MATRIX$(NC)\n"
	@printf "$(CYAN) │$(NC)\n"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "build"        "Build Python package"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "check-deps"   "Audit presence of uv and utilities"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "clean"        "Flush bytecode, cache, and venv"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "diagnose"     "linting & structural checks"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "format"       "Auto-format Python code via ruff"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "install"      "Setup system & dependencies via uv"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "lint"         "Run Ruff static code analysis"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "pack-install" "Bind global 'tdoc' execution alias"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "run"          "Boot the interactive telemetry HUD"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "sync"         "Synchronize project dependencies"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "test"         "Execute test suite via pytest"
	@printf "$(CYAN) │   $(MAGENTA)▷$(NC) $(BOLD)make$(NC) $(CYAN)%-13s$(NC) $(MUTED)%s$(NC)\n" "update"       "Robust project update"
	@printf "$(CYAN) │$(NC)\n"
	@printf "$(CYAN) ╰─$(NC) $(MAGENTA)FJ™ Cybertronic Systems$(NC) $(MUTED)· MMXXIV · V5.4.9$(NC)\n\n"

install:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Initializing Core Infrastructure...$(NC)\n"
	pkg install -y termux-api || (printf "$(RED) ✘$(NC) Failed to install termux-api\n" && exit 1)
	$(MAKE) sync

lint:
	@$(UV) run ruff check .

pack-install:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Binding Global Execution Shortcut...$(NC)\n"
	@mkdir -p "$${PREFIX:-/data/data/com.termux/files/usr}/bin"
	@printf '#!/data/data/com.termux/files/usr/bin/sh\n' > "$${PREFIX:-/data/data/com.termux/files/usr}/bin/tdoc"
	@printf 'cd "%s/Termux-Doctor" && uv run tdoc "$$@"\n' "$$HOME" >> "$${PREFIX:-/data/data/com.termux/files/usr}/bin/tdoc"
	@chmod +x "$${PREFIX:-/data/data/com.termux/files/usr}/bin/tdoc"
	@printf "$(GREEN) ✔$(NC) $(MUTED)Alias bound. Executable globally as 'tdoc'$(NC)\n\n"

run:
	@$(UV) run tdoc

sync:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Synchronizing Dependencies...$(NC)\n"
	@$(UV) sync --dev || (printf "$(RED) ✘$(NC) Failed to sync dependencies\n" && exit 1)
	@printf "$(GREEN) ✔$(NC) $(MUTED)Dependencies synchronized$(NC)\n\n"

test:
	@printf "\n$(CYAN) ◈$(NC) $(WHITE)Launching Test Suite...$(NC)\n"
	$(UV) run pytest
	@printf "$(GREEN) ✔$(NC) $(MUTED)All assertions satisfied$(NC)\n\n"

update:
	$(MAKE) sync
	$(MAKE) diagnose
