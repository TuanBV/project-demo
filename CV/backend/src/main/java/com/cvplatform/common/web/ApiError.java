package com.cvplatform.common.web;

import java.time.Instant;
import java.util.List;

/**
 * Uniform error payload returned by every failing endpoint.
 */
public record ApiError(
        String code,
        String message,
        List<FieldError> fieldErrors,
        String traceId,
        Instant timestamp) {

    public record FieldError(String field, String message) {
    }

    public static ApiError of(String code, String message, String traceId) {
        return new ApiError(code, message, List.of(), traceId, Instant.now());
    }

    public static ApiError ofFieldErrors(String code, String message, List<FieldError> fieldErrors, String traceId) {
        return new ApiError(code, message, fieldErrors, traceId, Instant.now());
    }
}
