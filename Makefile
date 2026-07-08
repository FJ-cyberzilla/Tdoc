# ====================================================================================
# TDoc Command Center - Master Automation & Orchestration Interface
# ====================================================================================

PYTHON = python3
PIP = pip

# ANSI Color Matrix (Orange Spectrum Theme Core)
PRIMARY_ORANGE = \033[38;5;208m
LIGHT_ORANGE   = \033[38;5;214m
DARK_AMBER     = \033[38;5;166m
STATUS_GREEN   = \033[0;32m
STATUS_RED     = \033[0;31m
INFO_CYAN      = \033[0;36m
NC             = \033[0m

.PHONY: default help install run format clean diagnose check-deps pack-install

default: help

help:
	@clear
	@echo "$(PRIMARY_ORANGE)====================================================================$(NC)"
	@echo "$(LIGHT_ORANGE) 🗲  T D O C  ::  P L A T F O R M  A U T O M a T I O N  E N G I N E  🗲 $(NC)"
	@echo "$(PRIMARY_ORANGE)====================================================================$(NC)"
	@echo "$(DARK_AMBER)Functional Blueprint:$(NC)"
	@echo "  TDoc runs low-level diagnostic boundaries across Termux, exposing hardware"
	@echo "  throttling, tracking active network DNS leaks, and isolation security traps."
	@echo ""
	@echo "$(DARK_AMBER)Operational Core Targets:$(NC)"
	@echo "  $(LIGHT_ORANGE)make install$(NC)    - Sets up system dependencies, 'termux-api', & pip assets."
	@echo "  $(LIGHT_ORANGE)make check-deps$(NC) - Audits presence of optional system utility layers."
	@echo "  $(LIGHT_ORANGE)make run$(NC)        - Boots the interactive telemetry HUD control loop."
	@echo "  $(LIGHT_ORANGE)make format$(NC)     - Enforces the strict 100-character line rule via Black."
	@echo "  $(LIGHT_ORANGE)make diagnose$(NC)   - Executes static workspace integrity & safety check gates."
	@echo "  $(LIGHT_ORANGE)make clean$(NC)      - Flushes bytecode artifacts, tracking layers, & cache blocks."
	@echo "  $(LIGHT_ORANGE)make pack-install$(NC)- Compiles and registers global 'tdoc' execution alias."
	@echo "$(PRIMARY_ORANGE)====================================================================$(NC)"

install:
	@echo "$(PRIMARY_ORANGE)🗲 Initializing TDoc Core Infrastructure Requirements...$(NC)"
	pkg install -y termux-api
	$(PIP) install --upgrade pip build
	$(PIP) install -r requirements.txt black pylint
	$(PIP) install --editable .
	@echo "$(STATUS_GREEN)✅ Dependency matrix bound and linked to global paths successfully.$(NC)"

check-deps:
	@if command -v termux-battery-status >/dev/null 2>&1; then \
	    echo "$(STATUS_GREEN)[+] Termux API bridge verified and active.$(NC)"; \
	else \
	    echo "$(STATUS_RED)[-] Notice: 'termux-api' binary is missing. Install via 'pkg install termux-api'.$(NC)"; \
	fi

run: check-deps
	@$(PYTHON) -m main

format:
	@echo "$(PRIMARY_ORANGE)🗲 Enforcing 100-Character Space Alignment Limits...$(NC)"
	black --line-length 100 .
	@echo "$(STATUS_GREEN)✅ Codebase formatting standardized seamlessly.$(NC)"

diagnose:
	@echo "$(PRIMARY_ORANGE)🗲 Spawning Static Workspace Integrity & Health Audit Engine...$(NC)"
	@echo "$(INFO_CYAN)[Gate 1/2] Checking internal execution code syntax linting...$(NC)"
	pylint --rcfile=.pylintrc main.py manager.py advanced/
	@echo "$(INFO_CYAN)[Gate 2/2] Verifying operational directory footprint...$(NC)"
	@$(PYTHON) -c "import os, sys; sys.exit(0 if os.path.exists('constants.py') else 1)" && \
		echo "$(STATUS_GREEN)✓ Core components alignment verified.$(NC)" || \
		(echo "$(STATUS_RED)✗ Structural Anomaly: Missing configuration variables.$(NC)" && exit 1)
	@echo "$(STATUS_GREEN)✅ System diagnostics gate passed. Workspace structure is pristine.$(NC)"

clean:
	@echo "$(DARK_AMBER)🧹 Flushing workspace compilation caches and storage artifacts...$(NC)"
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .pylint.d build/ dist/ *.egg-info
	@echo "$(STATUS_GREEN)✨ Workspace tracking slate completely purged and reset.$(NC)"

# --- GLOBAL UTILITY COMPILATION ---
pack-install:
	@echo "$(PRIMARY_ORANGE)📦 Compiling TDoc Core into Global Utility Module...$(NC)"
	@mkdir -p $(PREFIX)/bin
	@echo '#!/data/data/com.termux/files/usr/bin/sh' > $(PREFIX)/bin/tdoc
	@echo 'export PYTHONPATH="$$HOME/TDoc:$$PYTHONPATH"' >> $(PREFIX)/bin/tdoc
	@echo 'python3 $$HOME/TDoc/main.py "$$@"' >> $(PREFIX)/bin/tdoc
	@chmod +x $(PREFIX)/bin/tdoc
	@echo "$(STATUS_GREEN)✅ Global execution layer bound. Run 'tdoc' from anywhere.$(NC)"
