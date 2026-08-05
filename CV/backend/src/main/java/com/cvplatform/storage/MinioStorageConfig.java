package com.cvplatform.storage;

import com.cvplatform.common.config.AppProperties;
import io.minio.BucketExistsArgs;
import io.minio.MakeBucketArgs;
import io.minio.MinioClient;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MinioStorageConfig {

    private final AppProperties appProperties;

    public MinioStorageConfig(AppProperties appProperties) {
        this.appProperties = appProperties;
    }

    @Bean
    public MinioClient minioClient() {
        AppProperties.Minio minio = appProperties.getMinio();
        return MinioClient.builder()
                .endpoint(minio.getEndpoint())
                .credentials(minio.getAccessKey(), minio.getSecretKey())
                .build();
    }

    @Bean
    public MinioBucketInitializer minioBucketInitializer(MinioClient minioClient) {
        return new MinioBucketInitializer(minioClient, appProperties.getMinio().getBucket());
    }

    /** Creates the configured bucket on startup if it doesn't exist yet, so a fresh local/CI environment just works. */
    public static class MinioBucketInitializer {

        private static final Logger log = LoggerFactory.getLogger(MinioBucketInitializer.class);

        private final MinioClient minioClient;
        private final String bucket;

        public MinioBucketInitializer(MinioClient minioClient, String bucket) {
            this.minioClient = minioClient;
            this.bucket = bucket;
        }

        @PostConstruct
        public void ensureBucketExists() {
            try {
                boolean exists = minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucket).build());
                if (!exists) {
                    minioClient.makeBucket(MakeBucketArgs.builder().bucket(bucket).build());
                    log.info("Created MinIO bucket '{}'", bucket);
                }
            } catch (Exception e) {
                log.warn("Could not verify/create MinIO bucket '{}' on startup - will retry on first upload: {}", bucket, e.getMessage());
            }
        }
    }
}
