package services

import (
	"context"
	"fmt"
	"github.com/FJ-cyberzilla/Tdoc/internal/models"
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

// GetDumpsysData executes dumpsys commands and returns the aggregated results.
func (s *DumpsysService) GetDumpsysData(ctx context.Context) (models.DumpsysData, error) {
	cpuInfo, err := s.runner.Run(ctx, "dumpsys", "cpuinfo")
	if err != nil {
		return models.DumpsysData{}, fmt.Errorf("failed to get dumpsys cpuinfo: %w", err)
	}

	memInfo, err := s.runner.Run(ctx, "dumpsys", "meminfo")
	if err != nil {
		return models.DumpsysData{}, fmt.Errorf("failed to get dumpsys meminfo: %w", err)
	}

	return models.DumpsysData{
		CPUInfo: cpuInfo,
		MemInfo: memInfo,
	}, nil
}
