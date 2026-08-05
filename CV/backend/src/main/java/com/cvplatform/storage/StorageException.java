package com.cvplatform.storage;

import com.cvplatform.common.exception.ApiException;
import org.springframework.http.HttpStatus;

/** Wraps any storage-provider failure (MinIO/S3 I/O, auth, network) behind one error code. */
public class StorageException extends ApiException {

    public StorageException(String message, Throwable cause) {
        super("STORAGE_UNAVAILABLE", HttpStatus.SERVICE_UNAVAILABLE, message);
        initCause(cause);
    }
}
