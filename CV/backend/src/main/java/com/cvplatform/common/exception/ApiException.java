package com.cvplatform.common.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

/**
 * Base type for all business exceptions the {@code GlobalExceptionHandler}
 * knows how to translate into a stable {@code ApiError} code.
 */
@Getter
public abstract class ApiException extends RuntimeException {

    private final String code;
    private final HttpStatus status;

    protected ApiException(String code, HttpStatus status, String message) {
        super(message);
        this.code = code;
        this.status = status;
    }
}
