package com.cvplatform.storage;

import com.cvplatform.common.config.AppProperties;
import com.cvplatform.common.security.Checksums;
import io.minio.GetObjectArgs;
import io.minio.GetPresignedObjectUrlArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import io.minio.RemoveObjectArgs;
import io.minio.http.Method;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.net.URI;
import java.time.Duration;
import java.util.UUID;
import org.springframework.core.io.InputStreamResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

@Component
public class MinioFileStorage implements FileStorage {

    private static final String PROVIDER = "MINIO";

    private final MinioClient minioClient;
    private final String bucket;

    public MinioFileStorage(MinioClient minioClient, AppProperties appProperties) {
        this.minioClient = minioClient;
        this.bucket = appProperties.getMinio().getBucket();
    }

    @Override
    public StoredObjectMetadata store(StoreFileCommand command) {
        String extension = extensionFor(command.contentType());
        String storageKey = "resumes/%s/%s%s".formatted(command.ownerId(), UUID.randomUUID(), extension);
        String checksum = Checksums.sha256Hex(command.content());

        try (InputStream stream = new ByteArrayInputStream(command.content())) {
            minioClient.putObject(PutObjectArgs.builder()
                    .bucket(bucket)
                    .object(storageKey)
                    .stream(stream, command.content().length, -1)
                    .contentType(command.contentType())
                    .build());
        } catch (Exception e) {
            throw new StorageException("Failed to store file in object storage", e);
        }

        return new StoredObjectMetadata(PROVIDER, storageKey, command.content().length, checksum);
    }

    @Override
    public Resource loadPrivate(String storageKey) {
        try {
            InputStream stream = minioClient.getObject(GetObjectArgs.builder()
                    .bucket(bucket)
                    .object(storageKey)
                    .build());
            return new InputStreamResource(stream);
        } catch (Exception e) {
            throw new StorageException("Failed to read file from object storage", e);
        }
    }

    @Override
    public URI createTemporaryReadUrl(String storageKey, Duration ttl) {
        try {
            String url = minioClient.getPresignedObjectUrl(GetPresignedObjectUrlArgs.builder()
                    .method(Method.GET)
                    .bucket(bucket)
                    .object(storageKey)
                    .expiry((int) ttl.toSeconds())
                    .build());
            return URI.create(url);
        } catch (Exception e) {
            throw new StorageException("Failed to create a signed URL for the file", e);
        }
    }

    @Override
    public void delete(String storageKey) {
        try {
            minioClient.removeObject(RemoveObjectArgs.builder()
                    .bucket(bucket)
                    .object(storageKey)
                    .build());
        } catch (Exception e) {
            throw new StorageException("Failed to delete file from object storage", e);
        }
    }

    private static String extensionFor(String contentType) {
        return "application/pdf".equals(contentType) ? ".pdf" : "";
    }
}
