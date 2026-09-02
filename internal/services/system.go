package services

import (
	"context"
	"fmt"
)

// SystemData holds the results of system diagnostic commands.
type SystemData struct {
	Uptime         string
	Ps             string
	Disk           string
	DumpsysBattery string
}

// SystemProvider defines the interface for fetching system diagnostics.
type SystemProvider interface {
	GetSystemData(ctx context.Context) (SystemData, error)
}

// SystemService implements SystemProvider.
type SystemService struct {
	runner CommandRunner
}

// NewSystemService creates a new instance of SystemService with the given CommandRunner.
func NewSystemService(runner CommandRunner) *SystemService {
	return &SystemService{
		runner: runner,
	}
}

// GetSystemData executes system commands and returns the aggregated results.
func (s *SystemService) GetSystemData(ctx context.Context) (SystemData, error) {
	uptime, err := s.runner.Run(ctx, "uptime")
	if err != nil {
		return SystemData{}, fmt.Errorf("failed to get uptime: %w", err)
	}

	ps, err := s.runner.Run(ctx, "ps", "aux")
	if err != nil {
		return SystemData{}, fmt.Errorf("failed to get process list: %w", err)
	}

	disk, err := s.runner.Run(ctx, "df", "-h")
	if err != nil {
		return SystemData{}, fmt.Errorf("failed to get disk usage: %w", err)
	}

	dumpsysBattery, err := s.runner.Run(ctx, "dumpsys", "battery")
	if err != nil {
		return SystemData{}, fmt.Errorf("failed to get dumpsys battery: %w", err)
	}

	return SystemData{
		Uptime:         uptime,
		Ps:             ps,
		Disk:           disk,
		DumpsysBattery: dumpsysBattery,
	}, nil
}
