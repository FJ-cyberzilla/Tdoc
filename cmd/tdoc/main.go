package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/FJ-cyberzilla/Termux-Doctor/internal/ui"
	tea "github.com/charmbracelet/bubbletea"
)

const version = "v1.0.0"

func main() {
	showVersion := flag.Bool("version", false, "display version information")
	flag.Parse()

	if *showVersion {
		fmt.Printf("Termux-Doctor version %s\n", version)
		return
	}

	p := tea.NewProgram(ui.NewAppModel(), tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Alas, there's been an error: %v", err)
		os.Exit(1)
	}
}
