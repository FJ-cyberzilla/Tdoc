package services

import (
	"context"
	"errors"
	"testing"
)

func TestGetNetworkData(t *testing.T) {
	ctx := context.Background()

	t.Run("Success", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			responses: map[string]string{
				"ip addr":          "eth0: ...",
				"ip route":         "default via ...",
				"netstat -tulpn": "tcp 0 0 ...",
			},
			errs: map[string]error{},
		}
		service := NewNetworkService(mockRunner)

		data, err := service.GetNetworkData(ctx)
		if err != nil {
			t.Fatalf("expected no error, got %v", err)
		}

		if data.Interfaces != "eth0: ..." {
			t.Errorf("expected interfaces 'eth0: ...', got '%s'", data.Interfaces)
		}
		if data.Routes != "default via ..." {
			t.Errorf("expected routes 'default via ...', got '%s'", data.Routes)
		}
		if data.Netstat != "tcp 0 0 ..." {
			t.Errorf("expected netstat 'tcp 0 0 ...', got '%s'", data.Netstat)
		}
		if data.DNS == nil {
			t.Errorf("expected DNS to be set, got nil")
		}
	})

	t.Run("CommandError", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			responses: map[string]string{},
			errs: map[string]error{
				"ip addr": errors.New("command failed"),
			},
		}
		service := NewNetworkService(mockRunner)

		_, err := service.GetNetworkData(ctx)
		if err == nil {
			t.Fatal("expected error, got nil")
		}
	})
}
