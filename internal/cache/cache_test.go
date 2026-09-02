package cache

import (
	"testing"
	"time"
)

func TestCacheManager(t *testing.T) {
	cm := NewManager()

	// Test Set and Get
	cm.Set("key1", "value1", 100*time.Millisecond)
	val, found := cm.Get("key1")
	if !found || val != "value1" {
		t.Errorf("expected value1, got %v", val)
	}

	// Test Expiration
	time.Sleep(150 * time.Millisecond)
	_, found = cm.Get("key1")
	if found {
		t.Error("expected item to be expired")
	}

	// Test not found
	_, found = cm.Get("key2")
	if found {
		t.Error("expected item to not be found")
	}
}
