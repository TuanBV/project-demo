package com.cvplatform.resume.api.dto;

import com.cvplatform.resume.domain.ResumeVersion;
import com.cvplatform.resume.domain.StoredFile;
import java.time.Instant;
import java.util.UUID;

public record ResumeVersionResponse(
        UUID id,
        int versionNumber,
        String sourceType,
        boolean active,
        String originalFilename,
        Long sizeBytes,
        String contentType,
        String checksum,
        Instant createdAt) {

    public static ResumeVersionResponse from(ResumeVersion version, StoredFile file, boolean active) {
        return new ResumeVersionResponse(
                version.getId(),
                version.getVersionNumber(),
                version.getSourceType().name(),
                active,
                file != null ? file.getOriginalFilename() : null,
                file != null ? file.getSizeBytes() : null,
                file != null ? file.getContentType() : null,
                file != null ? file.getChecksum() : null,
                version.getCreatedAt());
    }
}
