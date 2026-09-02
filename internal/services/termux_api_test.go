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
			"termux-battery-status":       `{"status": "CHARGING"}`,
			"termux-wifi-connectioninfo":  `{"ssid": "test-wifi"}`,
			"termux-telephony-deviceinfo": `{"imei": "12345"}`,
			"termux-location":             `{"lat": 0, "lon": 0}`,
		},
		errs: map[string]error{},
	}
	service := NewTermuxAPIService(mockRunner)

	data, err := service.Run(context.Background())
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	battery, ok := data["battery"].(map[string]interface{})
	if !ok {
		t.Fatalf("battery is not a map[string]interface{}, got %T", data["battery"])
	}
	if battery["status"] != "CHARGING" {
		t.Errorf("expected CHARGING, got %v", battery["status"])
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

	wifi, ok := data["wifi"].(map[string]string)
	if !ok {
		t.Fatalf("wifi is not a map[string]string, got %T", data["wifi"])
	}
	if wifi["status"] != "error" {
		t.Errorf("expected error status, got %v", wifi["status"])
	}
}
