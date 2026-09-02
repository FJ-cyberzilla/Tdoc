package services

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/FJ-cyberzilla/Tdoc/internal/models"
)

// BatteryProvider defines the interface for fetching battery status.
type BatteryProvider interface {
	GetBatteryStatus(ctx context.Context) (models.Battery, error)
}

// BatteryService implements BatteryProvider.
type BatteryService struct {
	runner CommandRunner
}

// NewBatteryService creates a new instance of BatteryService with the given CommandRunner.
func NewBatteryService(runner CommandRunner) *BatteryService {
	return &BatteryService{
		runner: runner,
	}
}

// GetBatteryStatus executes the Termux battery command and parses the result.
func (s *BatteryService) GetBatteryStatus(ctx context.Context) (models.Battery, error) {
	output, err := s.runner.Run(ctx, "termux-battery-status")
	if err != nil {
		return models.Battery{}, fmt.Errorf("failed to get battery status: %w", err)
	}

	var battery models.Battery
	if err := json.Unmarshal([]byte(output), &battery); err != nil {
		return models.Battery{}, fmt.Errorf("failed to parse battery status: %w", err)
	}

	return battery, nil
}
