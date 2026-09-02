package services

import (
	"context"
	"fmt"
	"os/exec"
	"strings"
)

// CommandRunner defines the interface for executing shell commands.
type CommandRunner interface {
	Run(ctx context.Context, command string, args ...string) (string, error)
}

// OSCommandRunner implements CommandRunner using os/exec.
type OSCommandRunner struct{}

// Run executes the given command and returns its output.
func (r *OSCommandRunner) Run(ctx context.Context, command string, args ...string) (string, error) {
	cmd := exec.CommandContext(ctx, command, args...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("command %s failed: %w, output: %s", command, err, string(output))
	}
	return strings.TrimSpace(string(output)), nil
}
