package handlers

import (
	"testing"
)

func TestDNSLeakHandler_View(t *testing.T) {
	h := NewDNSLeakHandler()
	
	// Test empty view
	view := h.View(100, 20)
	if view == "" {
		t.Error("expected non-empty view")
	}
	
	// Test loading view
	h.Loading = true
	view = h.View(100, 20)
	if view != "DNS Leak Test: Testing..." {
		t.Errorf("expected testing view, got %s", view)
	}
}
