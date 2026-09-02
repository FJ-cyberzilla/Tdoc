package handlers

import (
	tea "github.com/charmbracelet/bubbletea"
)

type SensorHandler struct{}

func NewSensorHandler() *SensorHandler {
	return &SensorHandler{}
}

func (h *SensorHandler) Update(msg tea.Msg) tea.Cmd {
	return nil
}

func (h *SensorHandler) View(width int, height int) string {
	return "Sensor Panel\n\nSensor Hub..."
}
