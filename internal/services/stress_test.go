package services

import (
	"context"
	"sync"
	"testing"
)

// TestServiceStress simulates high-concurrency access to services.
func TestServiceStress(t *testing.T) {
	runner := &MockCommandRunner{
		responses: map[string]string{
			"df -h": "OK",
			"ping":  "OK",
		},
	}
	sysSvc := NewSystemService(runner)
	netSvc := NewNetworkService(runner)

	var wg sync.WaitGroup
	for i := 0; i < 50; i++ {
		wg.Add(2)
		go func() {
			defer wg.Done()
			_, _ = sysSvc.GetSystemData(context.Background())
		}()
		go func() {
			defer wg.Done()
			_, _ = netSvc.GetNetworkData(context.Background())
		}()
	}
	wg.Wait()
}
