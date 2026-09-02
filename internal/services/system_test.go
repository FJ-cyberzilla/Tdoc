package services

import (
	"context"
	"errors"
	"testing"
)

func TestGetSystemData(t *testing.T) {
	ctx := context.Background()

	t.Run("Success", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			responses: map[string]string{
				"uptime":          "up 1 day",
				"ps aux":          "proc1",
				"df -h":           "disk usage",
				"dumpsys battery": "battery info",
			},
			errs: map[string]error{},
		}
		service := NewSystemService(mockRunner)

		data, err := service.GetSystemData(ctx)
		if err != nil {
			t.Fatalf("expected no error, got %v", err)
		}

		if data.Uptime != "up 1 day" {
			t.Errorf("expected uptime 'up 1 day', got '%s'", data.Uptime)
		}
		if data.Ps != "proc1" {
			t.Errorf("expected ps 'proc1', got '%s'", data.Ps)
		}
		if data.Disk != "disk usage" {
			t.Errorf("expected disk 'disk usage', got '%s'", data.Disk)
		}
		if data.DumpsysBattery != "battery info" {
			t.Errorf("expected dumpsys battery 'battery info', got '%s'", data.DumpsysBattery)
		}
	})

	t.Run("CommandError", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			responses: map[string]string{},
			errs: map[string]error{
				"uptime": errors.New("command failed"),
			},
		}
		service := NewSystemService(mockRunner)

		_, err := service.GetSystemData(ctx)
		if err == nil {
			t.Fatal("expected error, got nil")
		}
	})
}
