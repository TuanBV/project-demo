package com.cvplatform.resume.application;

import com.cvplatform.common.exception.BadRequestException;

public class InvalidSectionContentException extends BadRequestException {

    public InvalidSectionContentException(String message) {
        super("INVALID_SECTION_CONTENT", message);
    }
}
