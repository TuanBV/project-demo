package com.cvplatform.identity;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.cvplatform.common.config.AppProperties;
import com.cvplatform.identity.api.dto.RegisterRequest;
import com.cvplatform.identity.application.AuthService;
import com.cvplatform.identity.application.EmailAlreadyRegisteredException;
import com.cvplatform.identity.application.InvalidCurrentPasswordException;
import com.cvplatform.identity.application.JwtService;
import com.cvplatform.identity.application.NotificationMailer;
import com.cvplatform.identity.domain.User;
import com.cvplatform.identity.domain.UserStatus;
import com.cvplatform.identity.infrastructure.PasswordResetTokenRepository;
import com.cvplatform.identity.infrastructure.RefreshTokenRepository;
import com.cvplatform.identity.infrastructure.UserRepository;
import java.util.Optional;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

/**
 * Pure business-logic tests (no Spring context, no database) - fast
 * feedback on branching that's awkward to exercise through the full HTTP
 * stack. {@link AuthControllerIT} covers the same flows end-to-end.
 */
@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;
    @Mock
    private RefreshTokenRepository refreshTokenRepository;
    @Mock
    private PasswordResetTokenRepository passwordResetTokenRepository;
    @Mock
    private JwtService jwtService;
    @Mock
    private NotificationMailer notificationMailer;

    private final PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    private AuthService authService;

    @BeforeEach
    void setUp() {
        authService = new AuthService(userRepository, refreshTokenRepository, passwordResetTokenRepository,
                passwordEncoder, jwtService, notificationMailer, new AppProperties());
    }

    @Test
    void registerRejectsDuplicateEmailCaseInsensitively() {
        when(userRepository.existsByEmailNormalized("jane@example.com")).thenReturn(true);

        assertThatThrownBy(() -> authService.register(new RegisterRequest("Jane@Example.com", "password123", "Jane")))
                .isInstanceOf(EmailAlreadyRegisteredException.class);
    }

    @Test
    void registerHashesThePasswordBeforePersisting() {
        when(userRepository.existsByEmailNormalized(any())).thenReturn(false);
        when(userRepository.save(any())).thenAnswer(invocation -> invocation.getArgument(0));

        User saved = authService.register(new RegisterRequest("new@example.com", "super-secret-1", "New User"));

        assertThat(saved.getPasswordHash()).isNotEqualTo("super-secret-1");
        assertThat(passwordEncoder.matches("super-secret-1", saved.getPasswordHash())).isTrue();
    }

    @Test
    void authenticateRejectsWrongPassword() {
        User existing = User.builder()
                .id(UUID.randomUUID())
                .email("user@example.com")
                .emailNormalized("user@example.com")
                .passwordHash(passwordEncoder.encode("correct-password"))
                .displayName("User")
                .status(UserStatus.ACTIVE)
                .build();
        when(userRepository.findByEmailNormalized("user@example.com")).thenReturn(Optional.of(existing));

        assertThatThrownBy(() -> authService.authenticate("user@example.com", "wrong-password"))
                .isInstanceOf(BadCredentialsException.class);
    }

    @Test
    void authenticateRejectsDisabledAccountEvenWithCorrectPassword() {
        User disabled = User.builder()
                .id(UUID.randomUUID())
                .email("disabled@example.com")
                .emailNormalized("disabled@example.com")
                .passwordHash(passwordEncoder.encode("correct-password"))
                .displayName("Disabled")
                .status(UserStatus.DISABLED)
                .build();
        when(userRepository.findByEmailNormalized("disabled@example.com")).thenReturn(Optional.of(disabled));

        assertThatThrownBy(() -> authService.authenticate("disabled@example.com", "correct-password"))
                .isInstanceOf(BadCredentialsException.class);
    }

    @Test
    void changePasswordRejectsWrongCurrentPassword() {
        UUID userId = UUID.randomUUID();
        User existing = User.builder()
                .id(userId)
                .email("user@example.com")
                .emailNormalized("user@example.com")
                .passwordHash(passwordEncoder.encode("correct-password"))
                .displayName("User")
                .status(UserStatus.ACTIVE)
                .build();
        when(userRepository.findById(userId)).thenReturn(Optional.of(existing));

        assertThatThrownBy(() -> authService.changePassword(userId, "wrong-current", "brand-new-password"))
                .isInstanceOf(InvalidCurrentPasswordException.class);
    }
}
