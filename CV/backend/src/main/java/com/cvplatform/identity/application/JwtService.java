package com.cvplatform.identity.application;

import com.cvplatform.common.config.AppProperties;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Date;
import java.util.UUID;
import javax.crypto.SecretKey;
import org.springframework.stereotype.Service;

/**
 * Issues and verifies short-lived JWT access tokens. Refresh tokens are a
 * separate opaque, server-side-tracked mechanism (see {@link AuthService})
 * so they can be individually revoked - a capability plain JWTs don't offer.
 */
@Service
public class JwtService {

    private final AppProperties appProperties;
    private final SecretKey signingKey;

    public JwtService(AppProperties appProperties) {
        this.appProperties = appProperties;
        this.signingKey = Keys.hmacShaKeyFor(appProperties.getJwt().getSecret().getBytes(StandardCharsets.UTF_8));
    }

    public String generateAccessToken(UUID userId) {
        Instant now = Instant.now();
        return Jwts.builder()
                .subject(userId.toString())
                .issuedAt(Date.from(now))
                .expiration(Date.from(now.plus(appProperties.getJwt().getAccessTokenTtl())))
                .signWith(signingKey)
                .compact();
    }

    /**
     * @return the authenticated user id, or empty if the token is missing, expired or tampered with.
     */
    public UUID parseUserId(String token) {
        try {
            Claims claims = Jwts.parser()
                    .verifyWith(signingKey)
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
            return UUID.fromString(claims.getSubject());
        } catch (JwtException | IllegalArgumentException ex) {
            throw new InvalidAccessTokenException();
        }
    }

    public static class InvalidAccessTokenException extends RuntimeException {
    }
}
