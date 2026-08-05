package com.cvplatform.storage;

import java.util.UUID;

/**
 * MVP loads the whole file into memory (bounded by the upload size cap,
 * default 10MB) rather than streaming - simplifies checksum computation and
 * is fine at this size. Revisit if the max upload size grows substantially.
 */
public record StoreFileCommand(UUID ownerId, String originalFilename, String contentType, byte[] content) {
}
