package services

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"

	"github.com/FJ-cyberzilla/Termux-Doctor/internal/models"
)

// DNSLeakProvider defines the interface for DNS leak diagnostics.
type DNSLeakProvider interface {
	CheckDNSLeak(ctx context.Context) ([]models.NetworkInfo, error)
}

// DNSLeakService implements DNSLeakProvider.
type DNSLeakService struct {
	httpClient *http.Client
	apiDomain  string
}

// NewDNSLeakService creates a new instance of DNSLeakService.
func NewDNSLeakService() *DNSLeakService {
	return &DNSLeakService{
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
		apiDomain: "bash.ws",
	}
}

// CheckDNSLeak performs a DNS leak test and returns the results.
func (s *DNSLeakService) CheckDNSLeak(ctx context.Context) ([]models.NetworkInfo, error) {
	testID, err := s.getTestID(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get test ID: %w", err)
	}

	if err := s.performFakePings(ctx, testID); err != nil {
		return nil, fmt.Errorf("failed to perform pings: %w", err)
	}

	// Wait for results to propagate
	select {
	case <-time.After(2 * time.Second):
	case <-ctx.Done():
		return nil, ctx.Err()
	}

	return s.getResults(ctx, testID)
}

func (s *DNSLeakService) getTestID(ctx context.Context) (string, error) {
	url := fmt.Sprintf("https://%s/id", s.apiDomain)
	req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
	resp, err := s.httpClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func (s *DNSLeakService) performFakePings(ctx context.Context, testID string) error {
	var wg sync.WaitGroup
	for i := 0; i <= 10; i++ {
		url := fmt.Sprintf("https://%d.%s.%s", i, testID, s.apiDomain)
		wg.Add(1)
		go func(url string) {
			defer wg.Done()
			req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
			resp, err := s.httpClient.Do(req)
			if err == nil {
				resp.Body.Close()
			}
		}(url)
	}
	wg.Wait()
	return nil
}

func (s *DNSLeakService) getResults(ctx context.Context, testID string) ([]models.NetworkInfo, error) {
	url := fmt.Sprintf("https://%s/dnsleak/test/%s?json", s.apiDomain, testID)
	req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
	resp, err := s.httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var networkInfos []models.NetworkInfo
	err = json.NewDecoder(resp.Body).Decode(&networkInfos)
	if err != nil {
		return nil, err
	}
	return networkInfos, nil
}
