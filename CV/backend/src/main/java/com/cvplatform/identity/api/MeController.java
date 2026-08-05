package com.cvplatform.identity.api;

import com.cvplatform.identity.api.dto.ChangePasswordRequest;
import com.cvplatform.identity.api.dto.UpdateMeRequest;
import com.cvplatform.identity.api.dto.UserResponse;
import com.cvplatform.identity.application.AuthService;
import com.cvplatform.identity.security.CurrentUserProvider;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/me")
public class MeController {

    private final AuthService authService;
    private final CurrentUserProvider currentUserProvider;

    public MeController(AuthService authService, CurrentUserProvider currentUserProvider) {
        this.authService = authService;
        this.currentUserProvider = currentUserProvider;
    }

    @GetMapping
    public UserResponse me() {
        return UserResponse.from(authService.getById(currentUserProvider.requireUserId()));
    }

    @PatchMapping
    public UserResponse updateMe(@Valid @RequestBody UpdateMeRequest request) {
        return UserResponse.from(authService.updateDisplayName(currentUserProvider.requireUserId(), request.displayName()));
    }

    @PostMapping("/change-password")
    public ResponseEntity<Void> changePassword(@Valid @RequestBody ChangePasswordRequest request) {
        authService.changePassword(currentUserProvider.requireUserId(), request.currentPassword(), request.newPassword());
        return ResponseEntity.noContent().build();
    }
}
