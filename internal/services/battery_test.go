package services

import (
	"context"
	"errors"
	"testing"
)

func TestGetBatteryStatus(t *testing.T) {
	ctx := context.Background()

	t.Run("Success", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			output: `{"percentage": 85, "temperature": 32.5, "is_charging": false}`,
			err:    nil,
		}
		service := NewBatteryService(mockRunner)

		battery, err := service.GetBatteryStatus(ctx)
		if err != nil {
			t.Fatalf("expected no error, got %v", err)
		}

		if battery.Percentage != 85 {
			t.Errorf("expected percentage 85, got %d", battery.Percentage)
		}
		if battery.Temperature != 32.5 {
			t.Errorf("expected temperature 32.5, got %f", battery.Temperature)
		}
		if battery.IsCharging != false {
			t.Errorf("expected is_charging false, got %t", battery.IsCharging)
		}
	})

	t.Run("CommandError", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			output: "",
			err:    errors.New("command failed"),
		}
		service := NewBatteryService(mockRunner)

		_, err := service.GetBatteryStatus(ctx)
		if err == nil {
			t.Fatal("expected error, got nil")
		}
	})

	t.Run("ParsingError", func(t *testing.T) {
		mockRunner := &MockCommandRunner{
			output: `invalid json`,
			err:    nil,
		}
		service := NewBatteryService(mockRunner)

		_, err := service.GetBatteryStatus(ctx)
		if err == nil {
			t.Fatal("expected error, got nil")
		}
	})
}
