# Makefile for Termux-Doctor
# CLI: tdoc

# Colors and Symbols
GREEN  = \033[32m
RED    = \033[31m
CYAN   = \033[36m
RESET  = \033[0m
BOLD   = \033[1m
CHECK  = ✅
CROSS  = ❌
INFO   = ℹ️

# OS/Arch Detection
OS := $(shell uname -s)
ARCH := $(shell uname -m)
GO_VERSION := $(shell go version)

.PHONY: all build test install run clean help lint vet tidy

all: build

build:
	@printf "$(CYAN)$(INFO)$(RESET) $(BOLD)Detected System: $(OS)/$(ARCH)$(RESET)\n"
	@printf "$(CYAN)$(CHECK)$(RESET) Building tdoc... "
	@go build -o tdoc ./cmd/tdoc && printf "$(GREEN)Success!$(RESET)\n" || (printf "$(RED)$(CROSS) Build failed!$(RESET)\n" && exit 1)

tidy:
	@printf "$(CYAN)$(CHECK)$(RESET) Running go mod tidy... "
	@go mod tidy && printf "$(GREEN)Success!$(RESET)\n" || (printf "$(RED)$(CROSS) Tidy failed!$(RESET)\n" && exit 1)

lint:
	@printf "$(CYAN)$(CHECK)$(RESET) Running go vet... "
	@go vet ./... && printf "$(GREEN)Success!$(RESET)\n" || (printf "$(RED)$(CROSS) Vet failed!$(RESET)\n" && exit 1)

vet:
	@printf "$(CYAN)$(CHECK)$(RESET) Running go vet... "
	@go vet ./... && printf "$(GREEN)Success!$(RESET)\n" || (printf "$(RED)$(CROSS) Vet failed!$(RESET)\n" && exit 1)

test:
	@printf "$(CYAN)$(CHECK)$(RESET) Running elite tests... "
	@go test -v ./... && printf "$(GREEN)Success!$(RESET)\n" || (printf "$(RED)$(CROSS) Tests failed!$(RESET)\n" && exit 1)

install: build
	@printf "$(CYAN)$(CHECK)$(RESET) Installing tdoc to ~/.local/bin... "
	@mkdir -p $(HOME)/.local/bin
	@cp tdoc $(HOME)/.local/bin/tdoc && printf "$(GREEN)Success!$(RESET)\n" || (printf "$(RED)$(CROSS) Install failed!$(RESET)\n" && exit 1)

run: build
	@printf "$(CYAN)$(INFO)$(RESET) Executing tdoc...\n"
	@./tdoc

clean:
	@printf "$(CYAN)$(CHECK)$(RESET) Cleaning build artifacts... "
	@rm -f tdoc
	@go clean && printf "$(GREEN)Done.$(RESET)\n"

help:
	@printf "$(BOLD)Termux-Doctor Makefile Targets:$(RESET)\n"
	@printf "  build   : $(CYAN)Compile the tdoc CLI$(RESET)\n"
	@printf "  lint    : $(CYAN)Run golangci-lint$(RESET)\n"
	@printf "  vet     : $(CYAN)Run go vet$(RESET)\n"
	@printf "  test    : $(CYAN)Run full test suite$(RESET)\n"
	@printf "  tidy    : $(CYAN)Run go mod tidy$(RESET)\n"
	@printf "  install : $(CYAN)Install tdoc to ~/.local/bin$(RESET)\n"
	@printf "  run     : $(CYAN)Build and execute tdoc$(RESET)\n"
	@printf "  clean   : $(CYAN)Remove build artifacts$(RESET)\n"
