package com.cvplatform.identity.application;

import com.cvplatform.common.exception.BadRequestException;

public class InvalidResetTokenException extends BadRequestException {

    public InvalidResetTokenException() {
        super("INVALID_RESET_TOKEN", "Reset token is invalid, expired or already used");
    }
}
