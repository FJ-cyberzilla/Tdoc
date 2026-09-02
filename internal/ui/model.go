package ui

import (
	"context"
	"fmt"

	"github.com/FJ-cyberzilla/Tdoc/internal/services"
	"github.com/FJ-cyberzilla/Tdoc/internal/ui/handlers"
	"github.com/charmbracelet/bubbles/progress"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// ViewState represents the current screen being displayed.
type ViewState int

const (
	Dashboard ViewState = iota
	Network
	Security
	Sensor
	DNSLeak
)

// Styling constants
var (
	headerStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FAFAFA")).
			Background(lipgloss.Color("#7D56F4")).
			Padding(0, 1).
			Bold(true)

	panelStyle = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#7D56F4")).
			Padding(1, 2)

	errorStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FF5F5F")).
			Bold(true)
)

// AppModel holds the global UI state.
type AppModel struct {
	CurrentView  ViewState
	Handlers     map[ViewState]handlers.Handler
	Width        int
	Height       int
	ErrorMessage string
	Progress     progress.Model
}

// NewAppModel initializes the UI model.
func NewAppModel() *AppModel {
	p := progress.New(progress.WithDefaultGradient())

	// Initialize services with a real runner
	runner := &services.OSCommandRunner{}
	dumpsysSvc := services.NewDumpsysService(runner)

	// Fetch initial data
	dumpsysData, _ := dumpsysSvc.GetDumpsysData(context.Background())

	dashboardHandler := handlers.NewDashboardHandler(p)
	dashboardHandler.DumpsysData = dumpsysData

	return &AppModel{
		CurrentView: Dashboard,
		Progress:    p,
		Handlers: map[ViewState]handlers.Handler{
			Dashboard: dashboardHandler,
			Network:   handlers.NewNetworkHandler(),
			Security:  handlers.NewSecurityHandler(),
			Sensor:    handlers.NewSensorHandler(),
			DNSLeak:   handlers.NewDNSLeakHandler(),
		},
	}
}

// Init initializes the bubbletea model.
func (m *AppModel) Init() tea.Cmd {
	return nil
}

// Update handles messages and updates the state.
func (m *AppModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit
		case "1":
			m.CurrentView = Dashboard
		case "2":
			m.CurrentView = Network
		case "3":
			m.CurrentView = Security
		case "4":
			m.CurrentView = Sensor
		case "5":
			m.CurrentView = DNSLeak
		}
	case tea.WindowSizeMsg:
		m.Width = msg.Width
		m.Height = msg.Height
	case progress.FrameMsg:
		newModel, c := m.Progress.Update(msg)
		cmd = c
		m.Progress = newModel.(progress.Model)
		return m, cmd
	}

	if handler, ok := m.Handlers[m.CurrentView]; ok {
		cmds = append(cmds, handler.Update(msg))
	}
	return m, tea.Batch(cmds...)
}

// View renders the current state.
func (m *AppModel) View() string {
	header := renderHeader()

	var content string

	// Error handling display
	if m.ErrorMessage != "" {
		content = errorStyle.Render(fmt.Sprintf("✘ Error: %s", m.ErrorMessage)) + "\n\n"
	}

	if handler, ok := m.Handlers[m.CurrentView]; ok {
		content += handler.View(m.Width, m.Height)
	} else {
		content += "Unknown View"
	}

	panel := panelStyle.Width(m.Width - 6).Render(content)
	nav := renderNavigation()

	return lipgloss.JoinVertical(lipgloss.Left,
		header,
		"",
		panel,
		"",
		nav,
	)
}

func renderHeader() string {
	return headerStyle.Render("⚡ T-DOC :: FJ™ Cybertronic")
}

func renderNavigation() string {
	return "Navigate: [1]Dash [2]Net [3]Sec [4]Sens [5]DNS | [q]Quit"
}
