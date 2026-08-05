package com.cvplatform.identity.security;

import com.cvplatform.common.exception.UnauthorizedException;
import java.util.Optional;
import java.util.UUID;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

/**
 * Reads the authenticated user id set by {@link JwtAuthenticationFilter}.
 * Controllers depend on this instead of the raw {@code Authentication}
 * object so the JWT/principal representation stays an implementation detail.
 */
@Component
public class CurrentUserProvider {

    public UUID requireUserId() {
        return optionalUserId().orElseThrow(() -> new UnauthorizedException("NOT_AUTHENTICATED", "Authentication is required"));
    }

    /**
     * For endpoints that are public but still want to special-case the
     * resource owner when they happen to be logged in - e.g. not counting
     * the owner's own visits to their public CV page.
     */
    public Optional<UUID> optionalUserId() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated() || !(authentication.getPrincipal() instanceof UUID userId)) {
            return Optional.empty();
        }
        return Optional.of(userId);
    }
}
