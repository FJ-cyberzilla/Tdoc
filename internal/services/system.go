package services

import (
	"context"
	"fmt"

	"golang.org/x/sync/errgroup"
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

// GetSystemData executes system commands in parallel and returns the aggregated results.
func (s *SystemService) GetSystemData(ctx context.Context) (SystemData, error) {
	g, ctx := errgroup.WithContext(ctx)

	var uptime, ps, disk, dumpsysBattery string

	g.Go(func() error {
		var err error
		uptime, err = s.runner.Run(ctx, "uptime")
		if err != nil {
			return fmt.Errorf("failed to get uptime: %w", err)
		}
		return nil
	})

	g.Go(func() error {
		var err error
		ps, err = s.runner.Run(ctx, "ps", "aux")
		if err != nil {
			return fmt.Errorf("failed to get process list: %w", err)
		}
		return nil
	})

	g.Go(func() error {
		var err error
		disk, err = s.runner.Run(ctx, "df", "-h")
		if err != nil {
			return fmt.Errorf("failed to get disk usage: %w", err)
		}
		return nil
	})

	g.Go(func() error {
		var err error
		dumpsysBattery, err = s.runner.Run(ctx, "dumpsys", "battery")
		if err != nil {
			return fmt.Errorf("failed to get dumpsys battery: %w", err)
		}
		return nil
	})

	if err := g.Wait(); err != nil {
		return SystemData{}, err
	}

	return SystemData{
		Uptime:         uptime,
		Ps:             ps,
		Disk:           disk,
		DumpsysBattery: dumpsysBattery,
	}, nil
}
