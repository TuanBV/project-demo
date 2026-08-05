package com.cvplatform.identity.application;

import com.cvplatform.common.exception.NotFoundException;

public class UserNotFoundException extends NotFoundException {

    public UserNotFoundException() {
        super("USER_NOT_FOUND", "User was not found");
    }
}
