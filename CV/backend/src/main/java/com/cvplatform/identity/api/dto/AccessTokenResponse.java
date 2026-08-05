package com.cvplatform.identity.api.dto;

/**
 * Access token returned in the JSON body. The refresh token is never
 * included here - it travels only as an HttpOnly/Secure/SameSite cookie.
 */
public record AccessTokenResponse(String accessToken, long expiresInSeconds, UserResponse user) {
}
