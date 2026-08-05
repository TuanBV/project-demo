package com.cvplatform.resume.application;

import com.cvplatform.common.exception.ConflictException;

public class CannotDeleteActiveVersionException extends ConflictException {

    public CannotDeleteActiveVersionException() {
        super("CANNOT_DELETE_ACTIVE_VERSION", "The active version cannot be deleted - activate a different version first");
    }
}
