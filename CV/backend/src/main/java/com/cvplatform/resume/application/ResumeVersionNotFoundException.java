package com.cvplatform.resume.application;

import com.cvplatform.common.exception.NotFoundException;

public class ResumeVersionNotFoundException extends NotFoundException {

    public ResumeVersionNotFoundException() {
        super("RESUME_VERSION_NOT_FOUND", "Resume version was not found");
    }
}
