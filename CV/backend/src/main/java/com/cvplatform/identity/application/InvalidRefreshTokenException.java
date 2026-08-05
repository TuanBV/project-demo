package com.cvplatform.identity.application;

import com.cvplatform.common.exception.UnauthorizedException;

public class InvalidRefreshTokenException extends UnauthorizedException {

    public InvalidRefreshTokenException() {
        super("INVALID_REFRESH_TOKEN", "Refresh token is missing, expired or has been revoked");
    }
}
