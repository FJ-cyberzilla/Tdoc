package services

import (
	"context"
	"fmt"
	"strings"
)

// DeviceData holds the results of device diagnostic commands.
type DeviceData struct {
	Properties map[string]string
	CpuInfo    string
	MemInfo    string
}

// DeviceProvider defines the interface for fetching device diagnostics.
type DeviceProvider interface {
	GetDeviceData(ctx context.Context) (DeviceData, error)
}

// DeviceService implements DeviceProvider.
type DeviceService struct {
	runner CommandRunner
}

// NewDeviceService creates a new instance of DeviceService with the given CommandRunner.
func NewDeviceService(runner CommandRunner) *DeviceService {
	return &DeviceService{
		runner: runner,
	}
}

// GetDeviceData executes device commands and returns the aggregated results.
func (s *DeviceService) GetDeviceData(ctx context.Context) (DeviceData, error) {
	props := []string{
		"ro.product.model",
		"ro.product.manufacturer",
		"ro.product.brand",
		"ro.product.device",
		"ro.build.version.release",
		"ro.build.version.sdk",
		"ro.hardware",
		"ro.board.platform",
		"ro.soc.model",
	}

	properties := make(map[string]string)
	for _, prop := range props {
		val, err := s.runner.Run(ctx, "getprop", prop)
		if err != nil {
			return DeviceData{}, fmt.Errorf("failed to get property %s: %w", prop, err)
		}
		properties[prop] = strings.TrimSpace(val)
	}

	cpuInfo, err := s.runner.Run(ctx, "cat", "/proc/cpuinfo")
	if err != nil {
		return DeviceData{}, fmt.Errorf("failed to get cpuinfo: %w", err)
	}

	memInfo, err := s.runner.Run(ctx, "cat", "/proc/meminfo")
	if err != nil {
		return DeviceData{}, fmt.Errorf("failed to get meminfo: %w", err)
	}

	return DeviceData{
		Properties: properties,
		CpuInfo:    cpuInfo,
		MemInfo:    memInfo,
	}, nil
}
