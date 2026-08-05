package com.cvplatform.identity.api.dto;

import com.cvplatform.identity.domain.User;
import java.util.UUID;

public record UserResponse(
        UUID id,
        String email,
        String displayName,
        String status) {

    public static UserResponse from(User user) {
        return new UserResponse(user.getId(), user.getEmail(), user.getDisplayName(), user.getStatus().name());
    }
}
