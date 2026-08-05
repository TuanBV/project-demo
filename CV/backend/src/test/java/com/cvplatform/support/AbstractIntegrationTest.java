package com.cvplatform.support;

import com.cvplatform.TestcontainersConfiguration;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.MinIOContainer;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.DockerImageName;

/**
 * Base for full-stack integration tests: real Spring context, real
 * PostgreSQL (via {@link TestcontainersConfiguration}'s {@code @ServiceConnection})
 * and a real MinIO container so resume/file-upload tests exercise the
 * actual {@code MinioFileStorage} implementation, not a mock. Unit tests
 * that don't need any of that should use Mockito instead - reserve this
 * for behaviour that only shows up end-to-end (auth flow, authorization,
 * HTTP status codes, real object storage round-trips).
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Import(TestcontainersConfiguration.class)
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Testcontainers
public abstract class AbstractIntegrationTest {

    private static final String BUCKET = "cv-platform-test";

    static final MinIOContainer MINIO_CONTAINER = new MinIOContainer(DockerImageName.parse("minio/minio:latest"));

    static {
        MINIO_CONTAINER.start();
    }

    @DynamicPropertySource
    static void minioProperties(DynamicPropertyRegistry registry) {
        registry.add("app.minio.endpoint", MINIO_CONTAINER::getS3URL);
        registry.add("app.minio.access-key", MINIO_CONTAINER::getUserName);
        registry.add("app.minio.secret-key", MINIO_CONTAINER::getPassword);
        registry.add("app.minio.bucket", () -> BUCKET);
    }
}
