package com.cvplatform.resume.application;

import com.cvplatform.common.exception.NotFoundException;

/**
 * Thrown both when a resume truly doesn't exist AND when it belongs to a
 * different owner - callers must not be able to distinguish "not yours"
 * from "doesn't exist" (see docs/security.md).
 */
public class ResumeNotFoundException extends NotFoundException {

    public ResumeNotFoundException() {
        super("RESUME_NOT_FOUND", "Resume was not found");
    }
}
