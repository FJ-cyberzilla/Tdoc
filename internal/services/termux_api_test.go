package services

import (
	"context"
	"errors"
	"testing"
)

func TestTriggerHaptic(t *testing.T) {
	mockRunner := &MockCommandRunner{
		responses: map[string]string{
			"termux-vibrate -d 100": "OK",
		},
		errs: map[string]error{},
	}
	service := NewTermuxAPIService(mockRunner)

	output, err := service.TriggerHaptic(context.Background(), 100)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if output != "OK" {
		t.Errorf("expected OK, got %s", output)
	}
}

func TestRun(t *testing.T) {
	mockRunner := &MockCommandRunner{
		responses: map[string]string{
			"termux-battery-status":       `{"percentage": 80, "status": "CHARGING"}`,
			"termux-wifi-connectioninfo":  `{"ssid": "test-wifi", "ip": "192.168.1.1"}`,
			"termux-telephony-deviceinfo": `{"imei": "12345"}`,
			"termux-location":             `{"latitude": 0, "longitude": 0}`,
		},
		errs: map[string]error{},
	}
	service := NewTermuxAPIService(mockRunner)

	data, err := service.Run(context.Background())
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	if data.Battery.Data.Status != "CHARGING" {
		t.Errorf("expected CHARGING, got %v", data.Battery.Data.Status)
	}
}

func TestRun_Error(t *testing.T) {
	mockRunner := &MockCommandRunner{
		responses: map[string]string{
			"termux-battery-status": `{}`,
		},
		errs: map[string]error{
			"termux-wifi-connectioninfo": errors.New("command failed"),
		},
	}
	service := NewTermuxAPIService(mockRunner)

	data, err := service.Run(context.Background())
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	if data.WiFi.Status != "error" {
		t.Errorf("expected error status, got %v", data.WiFi.Status)
	}
}
