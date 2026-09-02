package services

import (
	"context"
	"fmt"
	"net"
	"sync"
	"time"

	"github.com/FJ-cyberzilla/Tdoc/internal/cache"
)

// NetworkData holds the results of network diagnostic commands.
type NetworkData struct {
	Interfaces  string
	Routes      string
	Netstat     string
	DNS         []string
	PingLatency time.Duration
	DNSLatency  time.Duration
}

// NetworkProvider defines the interface for fetching network diagnostics.
type NetworkProvider interface {
	GetNetworkData(ctx context.Context) (NetworkData, error)
}

// NetworkService implements NetworkProvider.
type NetworkService struct {
	runner CommandRunner
	cache  *cache.Manager
}

// NewNetworkService creates a new instance of NetworkService with the given CommandRunner.
func NewNetworkService(runner CommandRunner) *NetworkService {
	return &NetworkService{
		runner: runner,
		cache:  cache.NewManager(),
	}
}

func (s *NetworkService) measureLatency(host string) time.Duration {
	start := time.Now()
	conn, err := net.DialTimeout("tcp", host, 2*time.Second)
	if err != nil {
		return 0
	}
	defer conn.Close()
	return time.Since(start)
}

func (s *NetworkService) measureDNSLatency(host string) time.Duration {
	start := time.Now()
	_, err := net.LookupHost(host)
	if err != nil {
		return 0
	}
	return time.Since(start)
}

// GetNetworkData executes network commands and returns the aggregated results.
func (s *NetworkService) GetNetworkData(ctx context.Context) (NetworkData, error) {
	// Try to get interfaces from cache
	if val, found := s.cache.Get("interfaces"); found {
		return val.(NetworkData), nil
	}

	var wg sync.WaitGroup
	wg.Add(3)

	var interfaces, routes, netstat string
	var errInterfaces, errRoutes, errNetstat error

	go func() {
		defer wg.Done()
		interfaces, errInterfaces = s.runner.Run(ctx, "ip", "addr")
	}()

	go func() {
		defer wg.Done()
		routes, errRoutes = s.runner.Run(ctx, "ip", "route")
	}()

	go func() {
		defer wg.Done()
		netstat, errNetstat = s.runner.Run(ctx, "netstat", "-tulpn")
	}()

	wg.Wait()

	if errInterfaces != nil {
		return NetworkData{}, fmt.Errorf("failed to get network interfaces: %w", errInterfaces)
	}
	if errRoutes != nil {
		return NetworkData{}, fmt.Errorf("failed to get network routes: %w", errRoutes)
	}
	if errNetstat != nil {
		return NetworkData{}, fmt.Errorf("failed to get netstat: %w", errNetstat)
	}

	// Perform diagnostics
	dns, _ := net.LookupHost("google.com")
	pingLatency := s.measureLatency("8.8.8.8:53")
	dnsLatency := s.measureDNSLatency("google.com")

	data := NetworkData{
		Interfaces:  interfaces,
		Routes:      routes,
		Netstat:     netstat,
		DNS:         dns,
		PingLatency: pingLatency,
		DNSLatency:  dnsLatency,
	}

	// Cache the result
	s.cache.Set("interfaces", data, 30*time.Second)

	return data, nil
}
