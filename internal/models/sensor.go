package models

// SensorData holds the results from Termux sensor commands.
type SensorData struct {
	Light       float64 `json:"light"`
	Proximity   float64 `json:"proximity"`
	Orientation []float64 `json:"orientation"`
}
