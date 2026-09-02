package services

import (
	"context"
	"fmt"
)

// NetworkData holds the results of network diagnostic commands.
type NetworkData struct {
	Interfaces string
	Routes     string
	Netstat    string
}

// NetworkProvider defines the interface for fetching network diagnostics.
type NetworkProvider interface {
	GetNetworkData(ctx context.Context) (NetworkData, error)
}

// NetworkService implements NetworkProvider.
type NetworkService struct {
	runner CommandRunner
}

// NewNetworkService creates a new instance of NetworkService with the given CommandRunner.
func NewNetworkService(runner CommandRunner) *NetworkService {
	return &NetworkService{
		runner: runner,
	}
}

// GetNetworkData executes network commands and returns the aggregated results.
func (s *NetworkService) GetNetworkData(ctx context.Context) (NetworkData, error) {
	interfaces, err := s.runner.Run(ctx, "ip", "addr")
	if err != nil {
		return NetworkData{}, fmt.Errorf("failed to get network interfaces: %w", err)
	}

	routes, err := s.runner.Run(ctx, "ip", "route")
	if err != nil {
		return NetworkData{}, fmt.Errorf("failed to get network routes: %w", err)
	}

	netstat, err := s.runner.Run(ctx, "netstat", "-tulpn")
	if err != nil {
		return NetworkData{}, fmt.Errorf("failed to get netstat: %w", err)
	}

	return NetworkData{
		Interfaces: interfaces,
		Routes:     routes,
		Netstat:    netstat,
	}, nil
}
