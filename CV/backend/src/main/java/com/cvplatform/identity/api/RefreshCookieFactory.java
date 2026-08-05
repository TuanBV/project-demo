package com.cvplatform.identity.api;

import com.cvplatform.common.config.AppProperties;
import java.time.Duration;
import java.time.Instant;
import org.springframework.http.ResponseCookie;
import org.springframework.stereotype.Component;

/**
 * Builds the HttpOnly/Secure/SameSite cookie that carries the refresh token.
 * The token itself never appears in a JSON response body.
 */
@Component
public class RefreshCookieFactory {

    /** Compile-time constant so controllers can reference it in {@code @CookieValue(name = ...)}. */
    public static final String COOKIE_NAME = "cv_refresh_token";

    private final AppProperties appProperties;

    public RefreshCookieFactory(AppProperties appProperties) {
        this.appProperties = appProperties;
    }

    public ResponseCookie create(String rawRefreshToken, Instant expiresAt) {
        AppProperties.Jwt jwtProps = appProperties.getJwt();
        return ResponseCookie.from(COOKIE_NAME, rawRefreshToken)
                .httpOnly(true)
                .secure(jwtProps.isCookieSecure())
                .sameSite("Strict")
                .path("/api/v1/auth")
                .maxAge(Duration.between(Instant.now(), expiresAt))
                .build();
    }

    public ResponseCookie clear() {
        AppProperties.Jwt jwtProps = appProperties.getJwt();
        return ResponseCookie.from(COOKIE_NAME, "")
                .httpOnly(true)
                .secure(jwtProps.isCookieSecure())
                .sameSite("Strict")
                .path("/api/v1/auth")
                .maxAge(0)
                .build();
    }
}
