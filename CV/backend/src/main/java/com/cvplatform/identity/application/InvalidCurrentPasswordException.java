package com.cvplatform.identity.application;

import com.cvplatform.common.exception.BadRequestException;

public class InvalidCurrentPasswordException extends BadRequestException {

    public InvalidCurrentPasswordException() {
        super("INVALID_CURRENT_PASSWORD", "Current password is incorrect");
    }
}
