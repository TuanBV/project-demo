package com.cvplatform.common.security;

import jakarta.servlet.http.HttpServletRequest;

/** Best-effort client IP, preferring a reverse proxy's X-Forwarded-For over the raw socket address. */
public final class ClientIpResolver {

    private ClientIpResolver() {
    }

    public static String resolve(HttpServletRequest request) {
        String forwardedFor = request.getHeader("X-Forwarded-For");
        if (forwardedFor != null && !forwardedFor.isBlank()) {
            return forwardedFor.split(",")[0].trim();
        }
        return request.getRemoteAddr();
    }
}
