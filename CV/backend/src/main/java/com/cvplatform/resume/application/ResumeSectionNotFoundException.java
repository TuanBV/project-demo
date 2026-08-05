package com.cvplatform.resume.application;

import com.cvplatform.common.exception.NotFoundException;

public class ResumeSectionNotFoundException extends NotFoundException {

    public ResumeSectionNotFoundException() {
        super("RESUME_SECTION_NOT_FOUND", "Section was not found");
    }
}
