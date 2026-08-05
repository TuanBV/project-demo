package com.cvplatform.identity.api;

import com.cvplatform.identity.api.dto.AccessTokenResponse;
import com.cvplatform.identity.api.dto.ForgotPasswordRequest;
import com.cvplatform.identity.api.dto.LoginRequest;
import com.cvplatform.identity.api.dto.RegisterRequest;
import com.cvplatform.identity.api.dto.ResetPasswordRequest;
import com.cvplatform.identity.api.dto.UserResponse;
import com.cvplatform.identity.application.AuthService;
import com.cvplatform.identity.application.InvalidRefreshTokenException;
import com.cvplatform.identity.application.JwtService;
import com.cvplatform.identity.application.TokenPair;
import com.cvplatform.identity.domain.User;
import jakarta.validation.Valid;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    private final AuthService authService;
    private final RefreshCookieFactory refreshCookieFactory;
    private final JwtService jwtService;

    public AuthController(AuthService authService, RefreshCookieFactory refreshCookieFactory, JwtService jwtService) {
        this.authService = authService;
        this.refreshCookieFactory = refreshCookieFactory;
        this.jwtService = jwtService;
    }

    @PostMapping("/register")
    public ResponseEntity<AccessTokenResponse> register(@Valid @RequestBody RegisterRequest request) {
        User user = authService.register(request);
        return issueTokens(user);
    }

    @PostMapping("/login")
    public ResponseEntity<AccessTokenResponse> login(@Valid @RequestBody LoginRequest request) {
        User user = authService.authenticate(request.email(), request.password());
        return issueTokens(user);
    }

    @PostMapping("/refresh")
    public ResponseEntity<AccessTokenResponse> refresh(
            @CookieValue(name = RefreshCookieFactory.COOKIE_NAME, required = false) String refreshCookie) {
        if (refreshCookie == null || refreshCookie.isBlank()) {
            throw new InvalidRefreshTokenException();
        }
        TokenPair tokenPair = authService.rotateRefreshToken(refreshCookie);
        User user = authService.getById(jwtService.parseUserId(tokenPair.accessToken()));
        return ResponseEntity.ok()
                .header(HttpHeaders.SET_COOKIE, refreshCookieFactory.create(tokenPair.rawRefreshToken(), tokenPair.refreshTokenExpiresAt()).toString())
                .body(new AccessTokenResponse(tokenPair.accessToken(), tokenPair.accessTokenExpiresInSeconds(), UserResponse.from(user)));
    }

    @PostMapping("/logout")
    public ResponseEntity<Void> logout(
            @CookieValue(name = RefreshCookieFactory.COOKIE_NAME, required = false) String refreshCookie) {
        if (refreshCookie != null && !refreshCookie.isBlank()) {
            authService.revokeRefreshToken(refreshCookie);
        }
        return ResponseEntity.noContent()
                .header(HttpHeaders.SET_COOKIE, refreshCookieFactory.clear().toString())
                .build();
    }

    @PostMapping("/forgot-password")
    public ResponseEntity<Void> forgotPassword(@Valid @RequestBody ForgotPasswordRequest request) {
        authService.forgotPassword(request.email());
        return ResponseEntity.status(HttpStatus.ACCEPTED).build();
    }

    @PostMapping("/reset-password")
    public ResponseEntity<Void> resetPassword(@Valid @RequestBody ResetPasswordRequest request) {
        authService.resetPassword(request.token(), request.newPassword());
        return ResponseEntity.noContent().build();
    }

    private ResponseEntity<AccessTokenResponse> issueTokens(User user) {
        TokenPair tokenPair = authService.issueTokenPair(user.getId());
        return ResponseEntity.ok()
                .header(HttpHeaders.SET_COOKIE, refreshCookieFactory.create(tokenPair.rawRefreshToken(), tokenPair.refreshTokenExpiresAt()).toString())
                .body(new AccessTokenResponse(tokenPair.accessToken(), tokenPair.accessTokenExpiresInSeconds(), UserResponse.from(user)));
    }
}
