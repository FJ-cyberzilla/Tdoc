package cache

import (
	"sync"
	"time"
)

// Item represents a cached item with an expiration time.
type Item[T any] struct {
	Value      T
	Expiration int64
}

// Manager is a thread-safe in-memory cache.
type Manager[T any] struct {
	items map[string]Item[T]
	mu    sync.RWMutex
}

// NewManager creates a new cache manager.
func NewManager[T any]() *Manager[T] {
	return &Manager[T]{
		items: make(map[string]Item[T]),
	}
}

// Set adds an item to the cache with a duration.
func (c *Manager[T]) Set(key string, value T, duration time.Duration) {
	expiration := time.Now().Add(duration).UnixNano()
	c.mu.Lock()
	defer c.mu.Unlock()
	c.items[key] = Item[T]{
		Value:      value,
		Expiration: expiration,
	}
}

// Get retrieves an item from the cache.
func (c *Manager[T]) Get(key string) (T, bool) {
	c.mu.RLock()
	item, found := c.items[key]
	c.mu.RUnlock()

	if !found {
		var zero T
		return zero, false
	}

	if time.Now().UnixNano() > item.Expiration {
		c.mu.Lock()
		delete(c.items, key)
		c.mu.Unlock()
		var zero T
		return zero, false
	}

	return item.Value, true
}
