package models

// NetworkInfo represents parsed results from DNS leak tests.
type NetworkInfo struct {
	IP          string `json:"ip"`
	Country     string `json:"country"`
	CountryName string `json:"country_name"`
	ASN         string `json:"asn"`
	Type        string `json:"type"`
}
