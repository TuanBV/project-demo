package com.cvplatform.common.web;

import io.github.bucket4j.Bandwidth;
import io.github.bucket4j.Bucket;
import java.time.Duration;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Component;

/**
 * Plain in-memory token buckets, one per key (e.g. "auth:1.2.3.4"). No TTL
 * eviction - fine at MVP scale/uptime; a long-lived deployment with very
 * high visitor/IP cardinality would want a bounded cache (e.g. Caffeine)
 * instead of this unbounded map. No Redis needed for a single-instance
 * monolith - see docs/architecture.md.
 */
@Component
public class RateLimiter {

    private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();

    public boolean tryConsume(String key, int capacityPerWindow, Duration window) {
        Bucket bucket = buckets.computeIfAbsent(key, k -> newBucket(capacityPerWindow, window));
        return bucket.tryConsume(1);
    }

    private static Bucket newBucket(int capacity, Duration window) {
        Bandwidth limit = Bandwidth.builder().capacity(capacity).refillGreedy(capacity, window).build();
        return Bucket.builder().addLimit(limit).build();
    }
}
