package com.cvplatform.identity;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.cvplatform.common.config.AppProperties;
import com.cvplatform.identity.application.JwtService;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class JwtServiceTest {

    private final JwtService jwtService = new JwtService(new AppProperties());

    @Test
    void generatedTokenRoundTripsToTheSameUserId() {
        UUID userId = UUID.randomUUID();
        String token = jwtService.generateAccessToken(userId);

        assertThat(jwtService.parseUserId(token)).isEqualTo(userId);
    }

    @Test
    void tamperedTokenIsRejected() {
        UUID userId = UUID.randomUUID();
        String token = jwtService.generateAccessToken(userId);
        String tampered = token.substring(0, token.length() - 1) + (token.endsWith("a") ? "b" : "a");

        assertThatThrownBy(() -> jwtService.parseUserId(tampered))
                .isInstanceOf(JwtService.InvalidAccessTokenException.class);
    }

    @Test
    void garbageTokenIsRejected() {
        assertThatThrownBy(() -> jwtService.parseUserId("not-a-jwt"))
                .isInstanceOf(JwtService.InvalidAccessTokenException.class);
    }
}
