package com.cvplatform.resume.application;

import com.cvplatform.common.exception.ConflictException;

public class CannotPublishException extends ConflictException {

    public CannotPublishException(String message) {
        super("CANNOT_PUBLISH", message);
    }
}
