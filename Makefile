# ====================================================================================
# TDoc Command Center - Master Automation & Orchestration
# ====================================================================================

PYTHON   = python3
PIP      = pip

# Suppress sub-make directory messages
MAKEFLAGS += --no-print-directory

# ANSI Color Palette (Vintage Green/Orange Theme) – using \033
ORANGE    = \033[38;5;208m
LIGHT_ORANGE = \033[38;5;214m
DARK_AMBER   = \033[38;5;166m
VINTAGE_GREEN = \033[38;5;70m
BOLD      = \033[1m
UNDERLINE = \033[4m
STATUS_GREEN = \033[0;32m
STATUS_RED   = \033[0;31m
INFO_CYAN    = \033[0;36m
PINK        = \033[38;5;213m
NC         = \033[0m

.PHONY: default help install format lint diagnose check-deps run clean brand pack-install

default: help

help:
	@printf "\n$(ORANGE)====================================================================$(NC)\n"
	@printf "$(LIGHT_ORANGE) 🗲  T D O C  ::  P L A T F O R M  A U T O M a T I O N   🗲 $(NC)\n"
	@printf "$(ORANGE)====================================================================$(NC)\n"
	@printf "$(DARK_AMBER)$(BOLD)Functional Blueprint:$(NC)\n"
	@printf "  TDoc runs light diagnostic  across Termux, exposing hardware\n"
	@printf "  throttling, tracking network DNS leaks,isolation security traps.\n\n"
	@printf "$(DARK_AMBER)$(BOLD)Operational Core Targets:$(NC)\n"
	@printf "  $(LIGHT_ORANGE)make install$(NC)    - Sets up systems.\n"
	@printf "  $(LIGHT_ORANGE)make check-deps$(NC) - Audits presence of Ruff and  utilities.\n"
	@printf "  $(LIGHT_ORANGE)make run$(NC)        - Boots the interactive telemetry HUD control loop.\n"
	@printf "  $(LIGHT_ORANGE)make format$(NC)     - Auto-formats Python code  100‑character line limit.\n"
	@printf "  $(LIGHT_ORANGE)make lint$(NC)       - Runs Ruff static analysis (lint + format check).\n"
	@printf "  $(LIGHT_ORANGE)make diagnose$(NC)   - Full health audit: linting and structural checks.\n"
	@printf "  $(LIGHT_ORANGE)make clean$(NC)      - Flushes bytecode, cache, and build artifacts.\n"
	@printf "  $(LIGHT_ORANGE)make pack-install$(NC)- Compiles and registers 'tdoc' execution alias.\n"
# The 'brand' target is intentionally hidden – not shown in help.
	@printf "$(ORANGE)====================================================================$(NC)\n\n"
	@$(MAKE) brand   # Show signature at the end of help

install:
	@printf "$(ORANGE)🗲 Initializing TDoc Core Infrastructure with Ruff...$(NC)\n"
	pkg install -y termux-api
	$(PIP) install --upgrade pip build
	$(PIP) install -r requirements.txt ruff
	$(PIP) install --editable .
	@printf "$(STATUS_GREEN)✅ Dependencies installed, Ruff is ready.$(NC)\n"
	@$(MAKE) brand

check-deps:
	@printf "$(INFO_CYAN)🔍 Checking system dependencies...$(NC)\n"
	@if command -v termux-battery-status >/dev/null 2>&1; then \
		printf "$(STATUS_GREEN)[+] termux-api: OK$(NC)\n"; \
	else \
		printf "$(STATUS_RED)[-] termux-api missing (install: pkg install termux-api)$(NC)\n"; \
	fi
	@if command -v ruff >/dev/null 2>&1; then \
		printf "$(STATUS_GREEN)[+] Ruff: OK$(NC)\n"; \
	else \
		printf "$(STATUS_RED)[-] Ruff missing (install: pip install ruff)$(NC)\n"; \
	fi

lint:
	@printf "$(ORANGE)🗲 Running Ruff linter...$(NC)\n"
	ruff check .
	@printf "$(STATUS_GREEN)✅ Lint passed.$(NC)\n"

format:
	@printf "$(ORANGE)🗲 Formatting code with Ruff (100‑character line limit)...$(NC)\n"
	ruff format --line-length 100 .
	@printf "$(STATUS_GREEN)✅ Codebase formatted.$(NC)\n"

diagnose: lint
	@printf "$(INFO_CYAN)[Gate 2/2] Verifying operational directory footprint...$(NC)\n"
	@$(PYTHON) -c "import os, sys; sys.exit(0 if os.path.exists('src/constants.py') else 1)" && \
		printf "$(STATUS_GREEN)✓ Core components alignment verified.$(NC)\n" || \
		(printf "$(STATUS_RED)✗ Structural Anomaly: Missing configuration variables.$(NC)\n" && exit 1)
	@printf "$(STATUS_GREEN)✅ System diagnostics gate passed. Workspace structure is pristine.$(NC)\n"

run: check-deps
	@$(PYTHON) -m src.main
	@$(MAKE) brand

clean:
	@printf "$(DARK_AMBER)🧹 Flushing workspace compilation caches and storage artifacts...$(NC)\n"
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .ruff_cache .pylint.d build/ dist/ *.egg-info
	@printf "$(STATUS_GREEN)✨ Workspace tracking slate completely purged and reset.$(NC)\n"

pack-install:
	@printf "$(ORANGE)📦 Compiling TDoc Core into Global Utility Module...$(NC)\n"
	@mkdir -p $(PREFIX)/bin
	@printf '#!/data/data/com.termux/files/usr/bin/sh\n' > $(PREFIX)/bin/tdoc
	@printf 'export PYTHONPATH="$$HOME/TDoc:$$PYTHONPATH"\n' >> $(PREFIX)/bin/tdoc
	@printf 'python3 $$HOME/TDoc/main.py "$$@"\n' >> $(PREFIX)/bin/tdoc
	@chmod +x $(PREFIX)/bin/tdoc
	@printf "$(STATUS_GREEN)✅ Global execution layer bound. Run 'tdoc' from anywhere.$(NC)\n"
	@$(MAKE) brand

brand:
	@printf "$(PINK)$(BOLD)✨ FJ™ Cybertronic Systems ✨$(NC)\n"
	@printf "$(DARK_AMBER)MMXXIV -- V 3.0.2$(NC)\n\n"
