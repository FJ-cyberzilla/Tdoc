package services

import (
	"context"
	"fmt"
	"net"
	"sync"
	"time"

	"github.com/FJ-cyberzilla/Termux-Doctor/internal/cache"
)

// NetworkData holds the results of network diagnostic commands and telemetry.
type NetworkData struct {
	Interfaces  string
	Routes      string
	Netstat     string
	DNS         []string
	PingLatency time.Duration
	DNSLatency  time.Duration
	DNSError    string
	PingError   string
}

// NetworkProvider defines the interface for fetching network diagnostics.
type NetworkProvider interface {
	GetNetworkData(ctx context.Context) (NetworkData, error)
}

// NetworkService implements NetworkProvider.
type NetworkService struct {
	runner CommandRunner
	cache  *cache.Manager[NetworkData]
}

// NewNetworkService creates a new instance of NetworkService with the given CommandRunner.
func NewNetworkService(runner CommandRunner) *NetworkService {
	return &NetworkService{
		runner: runner,
		cache:  cache.NewManager[NetworkData](),
	}
}

func (s *NetworkService) measureLatency(ctx context.Context, host string) (time.Duration, error) {
	var d net.Dialer
	ctx, cancel := context.WithTimeout(ctx, 2*time.Second)
	defer cancel()

	start := time.Now()
	conn, err := d.DialContext(ctx, "tcp", host)
	if err != nil {
		return 0, err
	}
	defer conn.Close()
	return time.Since(start), nil
}

func (s *NetworkService) measureDNSLatency(ctx context.Context, host string) (time.Duration, error) {
	ctx, cancel := context.WithTimeout(ctx, 2*time.Second)
	defer cancel()

	r := &net.Resolver{}
	start := time.Now()
	_, err := r.LookupHost(ctx, host)
	if err != nil {
		return 0, err
	}
	return time.Since(start), nil
}

// GetNetworkData executes network commands and returns the aggregated results.
func (s *NetworkService) GetNetworkData(ctx context.Context) (NetworkData, error) {
	// Try to get interfaces from cache
	if val, found := s.cache.Get("interfaces"); found {
		return val, nil
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

	// Perform diagnostics without ignoring errors
	r := &net.Resolver{}
	dnsCtx, dnsCancel := context.WithTimeout(ctx, 2*time.Second)
	defer dnsCancel()

	var dns []string
	var dnsErrStr string
	dnsHosts, err := r.LookupHost(dnsCtx, "google.com")
	if err != nil {
		dnsErrStr = err.Error()
	} else {
		dns = dnsHosts
	}

	pingLatency, err := s.measureLatency(ctx, "8.8.8.8:53")
	var pingErrStr string
	if err != nil {
		pingErrStr = err.Error()
	}

	dnsLatency, err := s.measureDNSLatency(ctx, "google.com")
	if err != nil && dnsErrStr == "" {
		dnsErrStr = err.Error()
	}

	data := NetworkData{
		Interfaces:  interfaces,
		Routes:      routes,
		Netstat:     netstat,
		DNS:         dns,
		PingLatency: pingLatency,
		DNSLatency:  dnsLatency,
		DNSError:    dnsErrStr,
		PingError:   pingErrStr,
	}

	// Cache the result
	s.cache.Set("interfaces", data, 30*time.Second)

	return data, nil
}
