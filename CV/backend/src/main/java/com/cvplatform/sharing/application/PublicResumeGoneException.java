package com.cvplatform.sharing.application;

import com.cvplatform.common.exception.GoneException;

/** The publicId is real, but the resume is deleted, unpublished, or private. */
public class PublicResumeGoneException extends GoneException {

    public PublicResumeGoneException() {
        super("RESUME_LINK_GONE", "This CV is no longer publicly available");
    }
}
