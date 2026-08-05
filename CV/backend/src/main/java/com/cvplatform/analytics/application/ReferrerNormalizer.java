package com.cvplatform.analytics.application;

import java.net.URI;
import java.util.Locale;
import org.springframework.stereotype.Component;

/** Keeps only the referring host - never the full URL (which could carry query-string tracking ids or paths). */
@Component
public class ReferrerNormalizer {

    public String normalizeHost(String referrerHeader) {
        if (referrerHeader == null || referrerHeader.isBlank()) {
            return null;
        }
        try {
            String host = URI.create(referrerHeader).getHost();
            if (host == null) {
                return null;
            }
            host = host.toLowerCase(Locale.ROOT);
            return host.startsWith("www.") ? host.substring(4) : host;
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}
