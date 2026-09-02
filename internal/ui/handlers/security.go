package handlers

import (
	tea "github.com/charmbracelet/bubbletea"
)

type SecurityHandler struct{}

func NewSecurityHandler() *SecurityHandler {
	return &SecurityHandler{}
}

func (h *SecurityHandler) Update(msg tea.Msg) tea.Cmd {
	return nil
}

func (h *SecurityHandler) View(width int, height int) string {
	return "Security Panel\n\nSecurity Audit..."
}
