package com.cvplatform.common.web;

import com.cvplatform.common.config.AppProperties;
import com.cvplatform.common.security.ClientIpResolver;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.time.Duration;
import java.util.Set;
import java.util.UUID;
import org.springframework.http.MediaType;
import org.springframework.web.filter.OncePerRequestFilter;

/**
 * Per-client-IP throttling for the two categories of endpoint the product
 * brief calls out: auth (login/register/forgot-password - brute-force and
 * account-enumeration targets) and public resume view/file/data endpoints
 * (scraping targets). Everything else is unthrottled here - normal
 * authenticated traffic doesn't need it, and adding it blindly would just
 * risk locking out a legitimate power user.
 */
public class RateLimitFilter extends OncePerRequestFilter {

    private static final Set<String> AUTH_PATHS = Set.of(
            "/api/v1/auth/login", "/api/v1/auth/register", "/api/v1/auth/forgot-password");

    private final RateLimiter rateLimiter;
    private final AppProperties appProperties;
    private final ObjectMapper objectMapper;

    public RateLimitFilter(RateLimiter rateLimiter, AppProperties appProperties, ObjectMapper objectMapper) {
        this.rateLimiter = rateLimiter;
        this.appProperties = appProperties;
        this.objectMapper = objectMapper;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        AppProperties.RateLimit config = appProperties.getRateLimit();
        if (!config.isEnabled()) {
            filterChain.doFilter(request, response);
            return;
        }

        String bucketName = resolveBucketName(request);
        if (bucketName == null) {
            filterChain.doFilter(request, response);
            return;
        }

        int capacity = "auth".equals(bucketName) ? config.getAuthCapacityPerWindow() : config.getPublicCapacityPerWindow();
        Duration window = "auth".equals(bucketName) ? config.getAuthWindow() : config.getPublicWindow();
        String key = bucketName + ":" + ClientIpResolver.resolve(request);

        if (rateLimiter.tryConsume(key, capacity, window)) {
            filterChain.doFilter(request, response);
        } else {
            writeTooManyRequests(response);
        }
    }

    private static String resolveBucketName(HttpServletRequest request) {
        String path = request.getRequestURI();
        if ("POST".equalsIgnoreCase(request.getMethod()) && AUTH_PATHS.contains(path)) {
            return "auth";
        }
        if (path.startsWith("/api/v1/public/")) {
            return "public";
        }
        return null;
    }

    private void writeTooManyRequests(HttpServletResponse response) throws IOException {
        response.setStatus(429);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        var error = ApiError.of("RATE_LIMIT_EXCEEDED", "Too many requests - please slow down and try again shortly", UUID.randomUUID().toString());
        objectMapper.writeValue(response.getWriter(), error);
    }
}
