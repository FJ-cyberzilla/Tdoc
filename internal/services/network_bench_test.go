package services

import (
	"context"
	"testing"
	"time"
)

func BenchmarkGetNetworkData(b *testing.B) {
	ctx := context.Background()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		mockRunner := &MockCommandRunner{
			responses: map[string]string{
				"ip addr":        "eth0: ...",
				"ip route":       "default via ...",
				"netstat -tulpn": "tcp 0 0 ...",
			},
			delays: map[string]time.Duration{
				"ip addr":        100 * time.Millisecond,
				"ip route":       100 * time.Millisecond,
				"netstat -tulpn": 100 * time.Millisecond,
			},
			errs: map[string]error{},
		}
		service := NewNetworkService(mockRunner)
		_, _ = service.GetNetworkData(ctx)
	}
}
