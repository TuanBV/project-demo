package com.cvplatform.resume.application;

import com.cvplatform.common.exception.BadRequestException;

public class NotAStructuredResumeException extends BadRequestException {

    public NotAStructuredResumeException() {
        super("NOT_A_STRUCTURED_RESUME", "Sections only apply to STRUCTURED resumes");
    }
}
