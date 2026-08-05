package com.cvplatform.common.config;

import java.time.Duration;
import java.util.List;
import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * Environment-driven settings. Kept in one place so every profile
 * (local/test/prod) overrides the same well-known keys instead of
 * scattering {@code @Value} across modules.
 */
@Getter
@Setter
@Configuration
@ConfigurationProperties(prefix = "app")
public class AppProperties {

    private final Cors cors = new Cors();
    private final Jwt jwt = new Jwt();
    private final PublicSite publicSite = new PublicSite();
    private final Minio minio = new Minio();
    private final Upload upload = new Upload();
    private final Resume resume = new Resume();
    private final Analytics analytics = new Analytics();
    private final RateLimit rateLimit = new RateLimit();

    @Getter
    @Setter
    public static class Cors {
        private List<String> allowedOrigins = List.of();
    }

    @Getter
    @Setter
    public static class Jwt {
        /** Base64 or plain secret used to sign access + refresh tokens. Must be overridden outside local/test. */
        private String secret = "change-me-change-me-change-me-change-me-32bytes";
        private Duration accessTokenTtl = Duration.ofMinutes(15);
        private Duration refreshTokenTtl = Duration.ofDays(30);
        /** Cookie Secure flag; disabled only for plain-HTTP local dev. */
        private boolean cookieSecure = true;
    }

    @Getter
    @Setter
    public static class PublicSite {
        /** Base URL of the frontend, used to build shareable public CV links. */
        private String baseUrl = "http://localhost:5174";
    }

    @Getter
    @Setter
    public static class Minio {
        private String endpoint = "http://localhost:9012";
        private String accessKey = "cvplatform";
        private String secretKey = "cvplatform-secret";
        private String bucket = "cv-platform-local";
    }

    @Getter
    @Setter
    public static class Upload {
        private long maxPdfSizeBytes = 10L * 1024 * 1024;
    }

    @Getter
    @Setter
    public static class Resume {
        /** How long a soft-deleted resume can still be restored. */
        private Duration trashRetention = Duration.ofDays(30);
    }

    @Getter
    @Setter
    public static class Analytics {
        /** Repeated requests from the same visitor within this window collapse into one page view. */
        private Duration viewDedupWindow = Duration.ofMinutes(30);
    }

    @Getter
    @Setter
    public static class RateLimit {
        private boolean enabled = true;
        /** Applies to login, register, forgot-password - keyed by client IP + endpoint. */
        private int authCapacityPerWindow = 10;
        private Duration authWindow = Duration.ofMinutes(1);
        /** Applies to public resume data/file/view endpoints - keyed by client IP. */
        private int publicCapacityPerWindow = 60;
        private Duration publicWindow = Duration.ofMinutes(1);
    }
}
