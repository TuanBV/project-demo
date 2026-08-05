package com.cvplatform.storage;

/** What {@link FileStorage#store} hands back so the caller can persist a {@code stored_files} row. */
public record StoredObjectMetadata(
        String storageProvider,
        String storageKey,
        long sizeBytes,
        String checksum) {
}
