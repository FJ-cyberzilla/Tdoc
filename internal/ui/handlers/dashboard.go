package handlers

import (
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/bubbles/progress"
)

type DashboardHandler struct {
	Progress progress.Model
}

func NewDashboardHandler(p progress.Model) *DashboardHandler {
	return &DashboardHandler{
		Progress: p,
	}
}

func (h *DashboardHandler) Update(msg tea.Msg) tea.Cmd {
	var cmd tea.Cmd
	newModel, cmd := h.Progress.Update(msg)
	h.Progress = newModel.(progress.Model)
	return cmd
}

func (h *DashboardHandler) View(width int, height int) string {
	return "Dashboard Panel\n\nLive Telemetry...\n" + h.Progress.ViewAs(0.5)
}
