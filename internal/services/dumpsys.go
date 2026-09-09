package services

import (
	"context"
	"fmt"

	"github.com/FJ-cyberzilla/Tdoc/internal/models"
	"golang.org/x/sync/errgroup"
)

// DumpsysProvider defines the interface for fetching dumpsys diagnostics.
type DumpsysProvider interface {
	GetDumpsysData(ctx context.Context) (models.DumpsysData, error)
}

// DumpsysService implements DumpsysProvider.
type DumpsysService struct {
	runner CommandRunner
}

// NewDumpsysService creates a new instance of DumpsysService.
func NewDumpsysService(runner CommandRunner) *DumpsysService {
	return &DumpsysService{runner: runner}
}

// GetDumpsysData executes dumpsys commands in parallel and returns the aggregated results.
func (s *DumpsysService) GetDumpsysData(ctx context.Context) (models.DumpsysData, error) {
	g, ctx := errgroup.WithContext(ctx)

	var cpuInfo, memInfo string

	g.Go(func() error {
		var err error
		cpuInfo, err = s.runner.Run(ctx, "dumpsys", "cpuinfo")
		if err != nil {
			return fmt.Errorf("failed to get dumpsys cpuinfo: %w", err)
		}
		return nil
	})

	g.Go(func() error {
		var err error
		memInfo, err = s.runner.Run(ctx, "dumpsys", "meminfo")
		if err != nil {
			return fmt.Errorf("failed to get dumpsys meminfo: %w", err)
		}
		return nil
	})

	if err := g.Wait(); err != nil {
		return models.DumpsysData{}, err
	}

	return models.DumpsysData{
		CPUInfo: cpuInfo,
		MemInfo: memInfo,
	}, nil
}
