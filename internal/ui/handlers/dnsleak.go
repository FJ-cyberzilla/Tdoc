package handlers

import (
	"fmt"
	"github.com/FJ-cyberzilla/Tdoc/internal/models"
	tea "github.com/charmbracelet/bubbletea"
)

type DNSLeakHandler struct {
	Results []models.NetworkInfo
	Loading bool
}

func NewDNSLeakHandler() *DNSLeakHandler {
	return &DNSLeakHandler{}
}

func (h *DNSLeakHandler) Update(msg tea.Msg) tea.Cmd {
	return nil
}

func (h *DNSLeakHandler) View(width int, height int) string {
	if h.Loading {
		return "DNS Leak Test: Testing..."
	}
	
	if len(h.Results) == 0 {
		return "DNS Leak Test: No results. Press 'r' to run."
	}

	content := "DNS Leak Test Results:\n"
	for _, res := range h.Results {
		content += fmt.Sprintf("- IP: %s (%s)\n", res.IP, res.CountryName)
	}
	return content
}
