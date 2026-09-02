package ui

import (
	"testing"

	tea "github.com/charmbracelet/bubbletea"
)

func TestAppModelUpdate(t *testing.T) {
	model := NewAppModel()

	// Test navigation
	msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("2")}
	newModel, _ := model.Update(msg)
	
	if newModel.(*AppModel).CurrentView != Network {
		t.Errorf("Expected Network view, got %v", newModel.(*AppModel).CurrentView)
	}
}
