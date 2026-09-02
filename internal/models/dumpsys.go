package models

// DumpsysData holds parsed results from Android dumpsys commands.
type DumpsysData struct {
	CPUInfo string
	MemInfo string
}
