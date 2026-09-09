package services

import (
	"context"
	"testing"
)

func BenchmarkSystemService(b *testing.B) {
	runner := &MockCommandRunner{
		responses: map[string]string{
			"df -h": "Filesystem Size Used Avail Use% Mounted on\n/dev/root 1G 500M 500M 50% /",
		},
	}
	svc := NewSystemService(runner)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = svc.GetSystemData(context.Background())
	}
}

func BenchmarkTermuxAPIService(b *testing.B) {
	runner := &MockCommandRunner{
		responses: map[string]string{
			"termux-battery-status":      `{"percentage": 80, "status": "discharging"}`,
			"termux-wifi-connectioninfo": `{"ssid": "test", "ip": "192.168.1.1"}`,
			"termux-telephony-deviceinfo": `{"imei": "123456"}`,
			"termux-location":             `{"latitude": 10.0, "longitude": 20.0}`,
		},
	}
	svc := NewTermuxAPIService(runner)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = svc.Run(context.Background())
	}
}
