package com.cvplatform.resume.api.dto;

import com.cvplatform.resume.domain.Resume;
import com.cvplatform.resume.domain.ResumeStatus;
import com.cvplatform.resume.domain.ResumeVisibility;
import java.time.Duration;
import java.time.Instant;
import java.util.UUID;

public record ResumeResponse(
        UUID id,
        UUID publicId,
        String name,
        String slug,
        String resumeType,
        String status,
        String visibility,
        boolean allowDownload,
        boolean searchEngineIndexable,
        boolean isDefault,
        UUID activeVersionId,
        long viewCount,
        Instant publishedAt,
        String publicUrl,
        /**
         * The raw unlisted share token - populated ONLY in the response of
         * the call that just generated it (switching visibility to
         * UNLISTED, or regenerate-link). Never re-derivable afterwards since
         * only its hash is persisted; the frontend must show/copy it
         * immediately and tell the user to save it.
         */
        String unlistedShareToken,
        Instant createdAt,
        Instant updatedAt,
        Instant deletedAt,
        Instant restorableUntil) {

    public static ResumeResponse from(Resume resume, Duration trashRetention, long viewCount, String publicSiteBaseUrl) {
        return from(resume, trashRetention, viewCount, publicSiteBaseUrl, null);
    }

    public static ResumeResponse from(Resume resume, Duration trashRetention, long viewCount, String publicSiteBaseUrl, String unlistedShareToken) {
        Instant restorableUntil = resume.getDeletedAt() != null ? resume.getDeletedAt().plus(trashRetention) : null;
        String publicUrl = resume.getStatus() == ResumeStatus.PUBLISHED && resume.getVisibility() == ResumeVisibility.PUBLIC
                ? "%s/cv/%s/%s".formatted(publicSiteBaseUrl, resume.getPublicId(), resume.getSlug())
                : null;
        return new ResumeResponse(
                resume.getId(),
                resume.getPublicId(),
                resume.getName(),
                resume.getSlug(),
                resume.getResumeType().name(),
                resume.getStatus().name(),
                resume.getVisibility().name(),
                resume.isAllowDownload(),
                resume.isSearchEngineIndexable(),
                resume.isDefault(),
                resume.getActiveVersionId(),
                viewCount,
                resume.getPublishedAt(),
                publicUrl,
                unlistedShareToken,
                resume.getCreatedAt(),
                resume.getUpdatedAt(),
                resume.getDeletedAt(),
                restorableUntil);
    }
}
