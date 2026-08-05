package com.cvplatform.resume.application;

import com.cvplatform.common.exception.ConflictException;

public class RestoreWindowExpiredException extends ConflictException {

    public RestoreWindowExpiredException() {
        super("RESTORE_WINDOW_EXPIRED", "This resume was deleted too long ago to be restored");
    }
}
