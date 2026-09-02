package services

import (
	"context"
	"strings"
)

// MockCommandRunner implements CommandRunner for testing purposes.
type MockCommandRunner struct {
	// For battery_test.go (Simple)
	output string
	err    error

	// For complex tests
	responses map[string]string
	errs      map[string]error
}

// Run returns the pre-set output or error based on the command and arguments.
func (m *MockCommandRunner) Run(ctx context.Context, command string, args ...string) (string, error) {
	// If responses or errs are used, behave like the map-based runner
	if m.responses != nil || m.errs != nil {
		key := command
		if len(args) > 0 {
			key += " " + strings.Join(args, " ")
		}
		if err, ok := m.errs[key]; ok {
			return "", err
		}
		return m.responses[key], nil
	}

	// Otherwise, behave like the simple runner
	return m.output, m.err
}
