package handlers

import (
	tea "github.com/charmbracelet/bubbletea"
)

type Handler interface {
	Update(msg tea.Msg) tea.Cmd
	View(width int, height int) string
}
