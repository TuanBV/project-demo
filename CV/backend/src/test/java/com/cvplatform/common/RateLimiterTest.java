package com.cvplatform.common;

import static org.assertj.core.api.Assertions.assertThat;

import com.cvplatform.common.web.RateLimiter;
import java.time.Duration;
import org.junit.jupiter.api.Test;

class RateLimiterTest {

    private final RateLimiter rateLimiter = new RateLimiter();

    @Test
    void allowsRequestsUpToCapacityThenRejects() {
        String key = "auth:1.2.3.4";
        for (int i = 0; i < 5; i++) {
            assertThat(rateLimiter.tryConsume(key, 5, Duration.ofMinutes(1))).isTrue();
        }

        assertThat(rateLimiter.tryConsume(key, 5, Duration.ofMinutes(1))).isFalse();
    }

    @Test
    void tracksDifferentKeysIndependently() {
        for (int i = 0; i < 3; i++) {
            assertThat(rateLimiter.tryConsume("auth:1.1.1.1", 3, Duration.ofMinutes(1))).isTrue();
        }
        assertThat(rateLimiter.tryConsume("auth:1.1.1.1", 3, Duration.ofMinutes(1))).isFalse();

        // A different key must not be affected by the first key's exhausted bucket.
        assertThat(rateLimiter.tryConsume("auth:2.2.2.2", 3, Duration.ofMinutes(1))).isTrue();
    }
}
