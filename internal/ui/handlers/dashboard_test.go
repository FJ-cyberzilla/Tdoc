package handlers

import (
	"testing"
	"github.com/charmbracelet/bubbles/progress"
)

func TestDashboardHandler_View(t *testing.T) {
	p := progress.New()
	h := NewDashboardHandler(p)
	
	view := h.View(100, 20)
	if view == "" {
		t.Error("expected non-empty view")
	}
}
