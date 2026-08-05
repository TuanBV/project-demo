package com.cvplatform.storage;

import java.net.URI;
import java.time.Duration;
import org.springframework.core.io.Resource;

/**
 * Abstraction over private object storage. {@link MinioFileStorage} backs
 * local development; a production S3 implementation can be added later by
 * implementing this same interface - resume/version business logic never
 * talks to a storage SDK directly.
 */
public interface FileStorage {

    StoredObjectMetadata store(StoreFileCommand command);

    Resource loadPrivate(String storageKey);

    URI createTemporaryReadUrl(String storageKey, Duration ttl);

    void delete(String storageKey);
}
