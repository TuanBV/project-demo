package com.cvplatform.common.web;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.UUID;
import org.slf4j.MDC;
import org.springframework.web.filter.OncePerRequestFilter;

/**
 * Stamps every request with a correlation id in MDC before anything else
 * runs, so every log line for a request (including ones logged by Spring
 * Security, JPA, etc.) can be grepped together. {@link GlobalExceptionHandler}
 * reuses this same id as {@code ApiError.traceId}, so a user-reported
 * traceId maps directly to server-side log lines for that request - no
 * separate correlation step needed.
 */
public class RequestCorrelationFilter extends OncePerRequestFilter {

    public static final String MDC_KEY = "traceId";
    private static final String RESPONSE_HEADER = "X-Trace-Id";

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        String traceId = UUID.randomUUID().toString();
        MDC.put(MDC_KEY, traceId);
        response.setHeader(RESPONSE_HEADER, traceId);
        try {
            filterChain.doFilter(request, response);
        } finally {
            MDC.remove(MDC_KEY);
        }
    }
}
