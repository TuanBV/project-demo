package com.cvplatform.common.exception;

import org.springframework.http.HttpStatus;

/** The resource existed but is no longer publicly reachable (unpublished, made private, link revoked). */
public class GoneException extends ApiException {

    public GoneException(String code, String message) {
        super(code, HttpStatus.GONE, message);
    }
}
