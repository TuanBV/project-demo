package com.cvplatform.identity.application;

import com.cvplatform.common.exception.ConflictException;

public class EmailAlreadyRegisteredException extends ConflictException {

    public EmailAlreadyRegisteredException() {
        super("EMAIL_ALREADY_REGISTERED", "An account with this email already exists");
    }
}
