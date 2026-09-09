package handlers

import (
	"testing"
)

func TestSecurityHandler_View(t *testing.T) {
	h := NewSecurityHandler()
	view := h.View(100, 20)
	if view == "" {
		t.Error("expected non-empty view")
	}
}
