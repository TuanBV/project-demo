package com.cvplatform.identity.application;

import com.cvplatform.common.config.AppProperties;
import com.cvplatform.common.security.TokenHasher;
import com.cvplatform.identity.api.dto.RegisterRequest;
import com.cvplatform.identity.domain.PasswordResetToken;
import com.cvplatform.identity.domain.RefreshToken;
import com.cvplatform.identity.domain.User;
import com.cvplatform.identity.domain.UserStatus;
import com.cvplatform.identity.infrastructure.PasswordResetTokenRepository;
import com.cvplatform.identity.infrastructure.RefreshTokenRepository;
import com.cvplatform.identity.infrastructure.UserRepository;
import java.time.Instant;
import java.util.Locale;
import java.util.UUID;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class AuthService {

    private static final int REFRESH_TOKEN_BYTES = 48;
    private static final int RESET_TOKEN_BYTES = 32;

    private final UserRepository userRepository;
    private final RefreshTokenRepository refreshTokenRepository;
    private final PasswordResetTokenRepository passwordResetTokenRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final NotificationMailer notificationMailer;
    private final AppProperties appProperties;

    public AuthService(UserRepository userRepository,
                        RefreshTokenRepository refreshTokenRepository,
                        PasswordResetTokenRepository passwordResetTokenRepository,
                        PasswordEncoder passwordEncoder,
                        JwtService jwtService,
                        NotificationMailer notificationMailer,
                        AppProperties appProperties) {
        this.userRepository = userRepository;
        this.refreshTokenRepository = refreshTokenRepository;
        this.passwordResetTokenRepository = passwordResetTokenRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
        this.notificationMailer = notificationMailer;
        this.appProperties = appProperties;
    }

    public User register(RegisterRequest request) {
        String normalizedEmail = normalizeEmail(request.email());
        if (userRepository.existsByEmailNormalized(normalizedEmail)) {
            throw new EmailAlreadyRegisteredException();
        }
        User user = User.builder()
                .email(request.email().trim())
                .emailNormalized(normalizedEmail)
                .passwordHash(passwordEncoder.encode(request.password()))
                .displayName(request.displayName().trim())
                .status(UserStatus.ACTIVE)
                .build();
        return userRepository.save(user);
    }

    private static final String INVALID_CREDENTIALS_MESSAGE = "Email or password is incorrect";

    public User authenticate(String email, String rawPassword) {
        User user = userRepository.findByEmailNormalized(normalizeEmail(email))
                .orElseThrow(() -> new BadCredentialsException(INVALID_CREDENTIALS_MESSAGE));
        if (!passwordEncoder.matches(rawPassword, user.getPasswordHash())) {
            throw new BadCredentialsException(INVALID_CREDENTIALS_MESSAGE);
        }
        if (!user.isActive()) {
            throw new BadCredentialsException(INVALID_CREDENTIALS_MESSAGE);
        }
        return user;
    }

    public TokenPair issueTokenPair(UUID userId) {
        String accessToken = jwtService.generateAccessToken(userId);
        String rawRefreshToken = TokenHasher.generateOpaqueToken(REFRESH_TOKEN_BYTES);
        Instant now = Instant.now();
        Instant expiresAt = now.plus(appProperties.getJwt().getRefreshTokenTtl());

        RefreshToken refreshToken = RefreshToken.builder()
                .userId(userId)
                .tokenHash(TokenHasher.sha256(rawRefreshToken))
                .expiresAt(expiresAt)
                .createdAt(now)
                .build();
        refreshTokenRepository.save(refreshToken);

        return new TokenPair(accessToken, appProperties.getJwt().getAccessTokenTtl().toSeconds(), rawRefreshToken, expiresAt);
    }

    /**
     * Rotates a refresh token: the presented token is revoked and a brand
     * new one is issued, regardless of whether it succeeds or fails, an
     * attacker replaying a stolen-but-already-used token cannot succeed.
     */
    public TokenPair rotateRefreshToken(String rawRefreshToken) {
        RefreshToken existing = refreshTokenRepository.findByTokenHash(TokenHasher.sha256(rawRefreshToken))
                .orElseThrow(InvalidRefreshTokenException::new);
        if (!existing.isActive(Instant.now())) {
            throw new InvalidRefreshTokenException();
        }
        existing.setRevokedAt(Instant.now());
        refreshTokenRepository.save(existing);
        return issueTokenPair(existing.getUserId());
    }

    public void revokeRefreshToken(String rawRefreshToken) {
        refreshTokenRepository.findByTokenHash(TokenHasher.sha256(rawRefreshToken))
                .ifPresent(token -> {
                    token.setRevokedAt(Instant.now());
                    refreshTokenRepository.save(token);
                });
    }

    public User getById(UUID userId) {
        return userRepository.findById(userId).orElseThrow(UserNotFoundException::new);
    }

    public void changePassword(UUID userId, String currentPassword, String newPassword) {
        User user = getById(userId);
        if (!passwordEncoder.matches(currentPassword, user.getPasswordHash())) {
            throw new InvalidCurrentPasswordException();
        }
        user.setPasswordHash(passwordEncoder.encode(newPassword));
        userRepository.save(user);
        refreshTokenRepository.revokeAllActiveForUser(userId);
    }

    public User updateDisplayName(UUID userId, String displayName) {
        User user = getById(userId);
        user.setDisplayName(displayName.trim());
        return userRepository.save(user);
    }

    /**
     * Always succeeds from the caller's point of view even when the email is
     * unknown, so this endpoint cannot be used to enumerate registered
     * accounts.
     */
    public void forgotPassword(String email) {
        userRepository.findByEmailNormalized(normalizeEmail(email)).ifPresent(user -> {
            String rawToken = TokenHasher.generateOpaqueToken(RESET_TOKEN_BYTES);
            Instant now = Instant.now();
            PasswordResetToken resetToken = PasswordResetToken.builder()
                    .userId(user.getId())
                    .tokenHash(TokenHasher.sha256(rawToken))
                    .expiresAt(now.plusSeconds(3600))
                    .createdAt(now)
                    .build();
            passwordResetTokenRepository.save(resetToken);
            String resetLink = appProperties.getPublicSite().getBaseUrl() + "/reset-password?token=" + rawToken;
            notificationMailer.sendPasswordResetEmail(user.getEmail(), resetLink);
        });
    }

    public void resetPassword(String rawToken, String newPassword) {
        PasswordResetToken resetToken = passwordResetTokenRepository.findByTokenHash(TokenHasher.sha256(rawToken))
                .orElseThrow(InvalidResetTokenException::new);
        if (!resetToken.isUsable(Instant.now())) {
            throw new InvalidResetTokenException();
        }
        User user = getById(resetToken.getUserId());
        user.setPasswordHash(passwordEncoder.encode(newPassword));
        userRepository.save(user);

        resetToken.setUsedAt(Instant.now());
        passwordResetTokenRepository.save(resetToken);
        refreshTokenRepository.revokeAllActiveForUser(user.getId());
    }

    private static String normalizeEmail(String email) {
        return email.trim().toLowerCase(Locale.ROOT);
    }
}
