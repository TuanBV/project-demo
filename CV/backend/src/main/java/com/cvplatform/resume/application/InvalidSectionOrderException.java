package com.cvplatform.resume.application;

import com.cvplatform.common.exception.BadRequestException;

public class InvalidSectionOrderException extends BadRequestException {

    public InvalidSectionOrderException() {
        super("INVALID_SECTION_ORDER", "The provided section order must contain exactly the resume's current sections, each once");
    }
}
