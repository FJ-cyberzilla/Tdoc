package models

// Battery represents the battery status information in a type-safe way.
type Battery struct {
	Percentage int     `json:"percentage"`
	Temperature float64 `json:"temperature"`
	IsCharging  bool    `json:"is_charging"`
}
