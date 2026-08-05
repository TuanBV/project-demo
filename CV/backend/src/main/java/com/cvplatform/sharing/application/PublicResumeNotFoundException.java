package com.cvplatform.sharing.application;

import com.cvplatform.common.exception.NotFoundException;

/** Unknown publicId, or an UNLISTED resume whose token didn't match - both must look identical to a caller. */
public class PublicResumeNotFoundException extends NotFoundException {

    public PublicResumeNotFoundException() {
        super("RESUME_LINK_NOT_FOUND", "This link does not exist");
    }
}
