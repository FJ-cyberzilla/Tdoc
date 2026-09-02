package cache

import (
	"sync"
	"time"
)

// Item represents a cached item with an expiration time.
type Item struct {
	Value      interface{}
	Expiration int64
}

// Manager is a thread-safe in-memory cache.
type Manager struct {
	items map[string]Item
	mu    sync.RWMutex
}

// NewManager creates a new cache manager.
func NewManager() *Manager {
	return &Manager{
		items: make(map[string]Item),
	}
}

// Set adds an item to the cache with a duration.
func (c *Manager) Set(key string, value interface{}, duration time.Duration) {
	expiration := time.Now().Add(duration).UnixNano()
	c.mu.Lock()
	defer c.mu.Unlock()
	c.items[key] = Item{
		Value:      value,
		Expiration: expiration,
	}
}

// Get retrieves an item from the cache.
func (c *Manager) Get(key string) (interface{}, bool) {
	c.mu.RLock()
	item, found := c.items[key]
	c.mu.RUnlock()

	if !found {
		return nil, false
	}

	if time.Now().UnixNano() > item.Expiration {
		c.mu.Lock()
		delete(c.items, key)
		c.mu.Unlock()
		return nil, false
	}

	return item.Value, true
}
