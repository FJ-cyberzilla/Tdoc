package handlers

import (
	"testing"
)

func TestSensorHandler_View(t *testing.T) {
	h := NewSensorHandler()
	view := h.View(100, 20)
	if view == "" {
		t.Error("expected non-empty view")
	}
}
