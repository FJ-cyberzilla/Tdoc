package handlers

import (
	tea "github.com/charmbracelet/bubbletea"
)

type NetworkHandler struct{}

func NewNetworkHandler() *NetworkHandler {
	return &NetworkHandler{}
}

func (h *NetworkHandler) Update(msg tea.Msg) tea.Cmd {
	return nil
}

func (h *NetworkHandler) View(width int, height int) string {
	return "Network Panel\n\nNetwork Fabric..."
}
