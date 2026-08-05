package com.cvplatform.analytics.application;

import com.cvplatform.common.security.Checksums;
import java.nio.charset.StandardCharsets;
import org.springframework.stereotype.Component;

/**
 * Anonymizes a visitor for dedup purposes. The raw IP is never persisted -
 * only this hash, computed on the fly from request data that is itself
 * discarded once the hash is taken.
 */
@Component
public class VisitorHasher {

    public String hash(String ipAddress, String userAgent) {
        String raw = (ipAddress == null ? "" : ipAddress) + '|' + (userAgent == null ? "" : userAgent);
        return Checksums.sha256Hex(raw.getBytes(StandardCharsets.UTF_8));
    }
}
