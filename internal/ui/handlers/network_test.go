package handlers

import (
	"testing"
)

func TestNetworkHandler_View(t *testing.T) {
	h := NewNetworkHandler()
	view := h.View(100, 20)
	if view == "" {
		t.Error("expected non-empty view")
	}
}
