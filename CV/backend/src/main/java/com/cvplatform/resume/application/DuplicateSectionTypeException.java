package com.cvplatform.resume.application;

import com.cvplatform.common.exception.ConflictException;

public class DuplicateSectionTypeException extends ConflictException {

    public DuplicateSectionTypeException() {
        super("DUPLICATE_SECTION_TYPE", "This resume already has a section of that type");
    }
}
