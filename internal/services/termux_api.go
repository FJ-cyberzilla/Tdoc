package services

import (
	"context"
	"encoding/json"
	"fmt"
)

// TermuxAPIProvider defines the interface for interacting with Termux APIs.
type TermuxAPIProvider interface {
	TriggerHaptic(ctx context.Context, durationMs int) (string, error)
	Run(ctx context.Context) (map[string]interface{}, error)
}

// TermuxAPIService implements TermuxAPIProvider.
type TermuxAPIService struct {
	runner CommandRunner
}

// NewTermuxAPIService creates a new instance of TermuxAPIService with the given CommandRunner.
func NewTermuxAPIService(runner CommandRunner) *TermuxAPIService {
	return &TermuxAPIService{
		runner: runner,
	}
}

// TriggerHaptic triggers haptic feedback on the device.
func (s *TermuxAPIService) TriggerHaptic(ctx context.Context, durationMs int) (string, error) {
	return s.runner.Run(ctx, "termux-vibrate", "-d", fmt.Sprintf("%d", durationMs))
}

// Run aggregates data from various Termux APIs.
func (s *TermuxAPIService) Run(ctx context.Context) (map[string]interface{}, error) {
	commands := map[string][]string{
		"battery":    {"termux-battery-status"},
		"wifi":       {"termux-wifi-connectioninfo"},
		"telephony":  {"termux-telephony-deviceinfo"},
		"location":   {"termux-location"},
	}

	results := make(map[string]interface{})
	for key, cmd := range commands {
		output, err := s.runner.Run(ctx, cmd[0], cmd[1:]...)
		if err != nil {
			results[key] = map[string]string{
				"status":  "error",
				"message": err.Error(),
			}
			continue
		}
		var data interface{}
		if err := json.Unmarshal([]byte(output), &data); err != nil {
			results[key] = string(output)
		} else {
			results[key] = data
		}
	}
	return results, nil
}
