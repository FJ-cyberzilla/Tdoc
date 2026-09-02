package models

// CPU represents CPU usage information.
type CPU struct {
	UsagePercent float64 `json:"usage_percent"`
	FrequencyMHz int     `json:"frequency_mhz"`
}

// RAM represents RAM usage information.
type RAM struct {
	TotalMB    int `json:"total_mb"`
	UsedMB     int `json:"used_mb"`
	Percentage int `json:"percentage"`
}
