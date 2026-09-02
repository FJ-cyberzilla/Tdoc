package services

import (
	"context"
	"errors"
	"testing"
)

func TestGetDumpsysData(t *testing.T) {
	ctx := context.Background()

	t.Run("Success", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			responses: map[string]string{
				"dumpsys cpuinfo": "Load: 0.1 / 0.1 / 0.1",
				"dumpsys meminfo": "Total PSS: 1024 KB",
			},
			errs: map[string]error{},
		}
		service := NewDumpsysService(mockRunner)

		data, err := service.GetDumpsysData(ctx)
		if err != nil {
			t.Fatalf("expected no error, got %v", err)
		}

		if data.CPUInfo != "Load: 0.1 / 0.1 / 0.1" {
			t.Errorf("expected CPUInfo 'Load: 0.1 / 0.1 / 0.1', got '%s'", data.CPUInfo)
		}
		if data.MemInfo != "Total PSS: 1024 KB" {
			t.Errorf("expected MemInfo 'Total PSS: 1024 KB', got '%s'", data.MemInfo)
		}
	})

	t.Run("CommandError", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			responses: map[string]string{},
			errs: map[string]error{
				"dumpsys cpuinfo": errors.New("command failed"),
			},
		}
		service := NewDumpsysService(mockRunner)

		_, err := service.GetDumpsysData(ctx)
		if err == nil {
			t.Fatal("expected error, got nil")
		}
	})
}
