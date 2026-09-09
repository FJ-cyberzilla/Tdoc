package services

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/FJ-cyberzilla/Tdoc/internal/models"
	"golang.org/x/sync/errgroup"
)

// TermuxAPIProvider defines the interface for interacting with Termux APIs.
type TermuxAPIProvider interface {
	TriggerHaptic(ctx context.Context, durationMs int) (string, error)
	Run(ctx context.Context) (models.TermuxAPIResults, error)
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

// fetch runs a command and unmarshals the output into a specific type.
func fetch[T any](ctx context.Context, runner CommandRunner, cmd []string) (T, error) {
	var result T
	output, err := runner.Run(ctx, cmd[0], cmd[1:]...)
	if err != nil {
		return result, err
	}
	err = json.Unmarshal([]byte(output), &result)
	return result, err
}

// APIRequest defines the structure for a Termux API command and its result.
type APIRequest[T any] struct {
	Name    string
	Command []string
	Result  *models.APIResult[T]
}

// Run aggregates data from various Termux APIs.
func (s *TermuxAPIService) Run(ctx context.Context) (models.TermuxAPIResults, error) {
	results := models.TermuxAPIResults{}
	g, ctx := errgroup.WithContext(ctx)

	// Define tasks
	tasks := []func() error{
		func() error {
			data, err := fetch[models.BatteryStatus](ctx, s.runner, []string{"termux-battery-status"})
			if err != nil {
				results.Battery.Status = "error"
				results.Battery.Message = err.Error()
				return nil // Don't fail the whole run on a single API failure
			}
			results.Battery.Status = "ok"
			results.Battery.Data = data
			return nil
		},
		func() error {
			data, err := fetch[models.WiFiInfo](ctx, s.runner, []string{"termux-wifi-connectioninfo"})
			if err != nil {
				results.WiFi.Status = "error"
				results.WiFi.Message = err.Error()
				return nil
			}
			results.WiFi.Status = "ok"
			results.WiFi.Data = data
			return nil
		},
		func() error {
			data, err := fetch[models.TelephonyInfo](ctx, s.runner, []string{"termux-telephony-deviceinfo"})
			if err != nil {
				results.Telephony.Status = "error"
				results.Telephony.Message = err.Error()
				return nil
			}
			results.Telephony.Status = "ok"
			results.Telephony.Data = data
			return nil
		},
		func() error {
			data, err := fetch[models.LocationInfo](ctx, s.runner, []string{"termux-location"})
			if err != nil {
				results.Location.Status = "error"
				results.Location.Message = err.Error()
				return nil
			}
			results.Location.Status = "ok"
			results.Location.Data = data
			return nil
		},
	}

	for _, task := range tasks {
		g.Go(task)
	}

	if err := g.Wait(); err != nil {
		return results, err
	}

	return results, nil
}
