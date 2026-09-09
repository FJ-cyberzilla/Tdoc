package handlers

import (
	"fmt"
	"github.com/FJ-cyberzilla/Termux-Doctor/internal/models"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/bubbles/progress"
)

type DashboardHandler struct {
	Progress    progress.Model
	DumpsysData models.DumpsysData
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
	return fmt.Sprintf("Dashboard Panel\n\nLive Telemetry...\n%s\n\nSystem Diagnostics (Dumpsys):\nCPU: %s\nMEM: %s",
		h.Progress.ViewAs(0.5), h.DumpsysData.CPUInfo, h.DumpsysData.MemInfo)
}
