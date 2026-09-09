package services

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/FJ-cyberzilla/Termux-Doctor/internal/models"
)

// SensorProvider defines the interface for fetching sensor diagnostics.
type SensorProvider interface {
	GetSensorData(ctx context.Context) (models.SensorData, error)
}

// SensorService implements SensorProvider.
type SensorService struct {
	runner CommandRunner
}

// NewSensorService creates a new instance of SensorService.
func NewSensorService(runner CommandRunner) *SensorService {
	return &SensorService{runner: runner}
}

// GetSensorData executes sensor commands and returns the parsed results.
func (s *SensorService) GetSensorData(ctx context.Context) (models.SensorData, error) {
	output, err := s.runner.Run(ctx, "termux-sensor", "-n", "1")
	if err != nil {
		return models.SensorData{}, fmt.Errorf("failed to get sensor data: %w", err)
	}

	var data models.SensorData
	if err := json.Unmarshal([]byte(output), &data); err != nil {
		return models.SensorData{}, fmt.Errorf("failed to parse sensor data: %w", err)
	}

	return data, nil
}
