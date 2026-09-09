package models

// APIResult is a generic wrapper for Termux API responses.
type APIResult[T any] struct {
	Status  string `json:"status"`
	Data    T      `json:"data,omitempty"`
	Message string `json:"message,omitempty"`
}

// BatteryStatus represents the battery state.
type BatteryStatus struct {
	Percentage int    `json:"percentage"`
	Status     string `json:"status"`
}

// WiFiInfo represents WiFi connection info.
type WiFiInfo struct {
	SSID string `json:"ssid"`
	IP   string `json:"ip"`
}

// TelephonyInfo represents device telephony info.
type TelephonyInfo struct {
	IMEI string `json:"imei"`
}

// LocationInfo represents device location.
type LocationInfo struct {
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
}

// TermuxAPIResults aggregates typed results.
type TermuxAPIResults struct {
	Battery   APIResult[BatteryStatus]
	WiFi      APIResult[WiFiInfo]
	Telephony APIResult[TelephonyInfo]
	Location  APIResult[LocationInfo]
}
