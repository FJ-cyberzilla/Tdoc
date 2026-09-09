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

// CommandError represents a detailed error when running a command.
type CommandError struct {
	Command string
	Args    []string
	Err     error
	Output  string
}

func (e *CommandError) Error() string {
	return fmt.Sprintf("command '%s %s' failed: %v, output: %s", e.Command, strings.Join(e.Args, " "), e.Err, e.Output)
}

func (e *CommandError) Unwrap() error {
	return e.Err
}

// OSCommandRunner implements CommandRunner using os/exec.
type OSCommandRunner struct{}

// Run executes the given command and returns its output.
func (r *OSCommandRunner) Run(ctx context.Context, command string, args ...string) (string, error) {
	cmd := exec.CommandContext(ctx, command, args...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return "", &CommandError{
			Command: command,
			Args:    args,
			Err:     err,
			Output:  strings.TrimSpace(string(output)),
		}
	}
	return strings.TrimSpace(string(output)), nil
}
