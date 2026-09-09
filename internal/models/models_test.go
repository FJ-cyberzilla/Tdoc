package models

import (
	"testing"
)

func TestBatteryModel(t *testing.T) {
	b := Battery{
		Percentage:  80,
		Temperature: 35.5,
		IsCharging:  true,
	}

	if b.Percentage != 80 {
		t.Errorf("expected percentage 80, got %d", b.Percentage)
	}
	if b.Temperature != 35.5 {
		t.Errorf("expected temperature 35.5, got %f", b.Temperature)
	}
	if !b.IsCharging {
		t.Error("expected charging to be true, got false")
	}
}
