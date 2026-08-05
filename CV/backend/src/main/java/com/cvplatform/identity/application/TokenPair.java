package com.cvplatform.identity.application;

import java.time.Instant;

public record TokenPair(String accessToken, long accessTokenExpiresInSeconds, String rawRefreshToken, Instant refreshTokenExpiresAt) {
}
