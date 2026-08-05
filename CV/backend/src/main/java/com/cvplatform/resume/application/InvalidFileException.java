package com.cvplatform.resume.application;

import com.cvplatform.common.exception.BadRequestException;

public class InvalidFileException extends BadRequestException {

    public InvalidFileException(String message) {
        super("INVALID_FILE", message);
    }
}
