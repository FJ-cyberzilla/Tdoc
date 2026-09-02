package services

import (
	"context"
	"errors"
	"testing"
)

func TestGetDeviceData(t *testing.T) {
	ctx := context.Background()

	t.Run("Success", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			responses: map[string]string{
				"getprop ro.product.model":          "pixel6",
				"getprop ro.product.manufacturer":  "google",
				"getprop ro.product.brand":          "google",
				"getprop ro.product.device":         "oriole",
				"getprop ro.build.version.release":  "12",
				"getprop ro.build.version.sdk":      "31",
				"getprop ro.hardware":               "gs101",
				"getprop ro.board.platform":         "gs101",
				"getprop ro.soc.model":              "tensor",
				"cat /proc/cpuinfo":                "processor : 0",
				"cat /proc/meminfo":                "MemTotal: 8GB",
			},
			errs: map[string]error{},
		}
		service := NewDeviceService(mockRunner)

		data, err := service.GetDeviceData(ctx)
		if err != nil {
			t.Fatalf("expected no error, got %v", err)
		}

		if data.Properties["ro.product.model"] != "pixel6" {
			t.Errorf("expected pixel6, got %s", data.Properties["ro.product.model"])
		}
		if data.CpuInfo != "processor : 0" {
			t.Errorf("expected processor : 0, got %s", data.CpuInfo)
		}
		if data.MemInfo != "MemTotal: 8GB" {
			t.Errorf("expected MemTotal: 8GB, got %s", data.MemInfo)
		}
	})

	t.Run("PropertyError", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			responses: map[string]string{},
			errs: map[string]error{
				"getprop ro.product.model": errors.New("command failed"),
			},
		}
		service := NewDeviceService(mockRunner)

		_, err := service.GetDeviceData(ctx)
		if err == nil {
			t.Fatal("expected error, got nil")
		}
	})
}
