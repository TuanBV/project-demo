package com.cvplatform.sharing.api.dto;

import com.cvplatform.resume.application.StructuredSnapshotBuilder;
import com.cvplatform.resume.domain.Resume;
import java.util.List;
import java.util.UUID;

/**
 * Deliberately minimal and explicitly whitelisted - never built by
 * serializing {@link Resume} directly. Any field the owner hasn't chosen to
 * expose (or that simply doesn't belong in a public response, like
 * {@code ownerId} or storage keys) is structurally impossible to leak here.
 */
public record PublicResumeResponse(
        UUID publicId,
        String name,
        String slug,
        String resumeType,
        boolean allowDownload,
        boolean searchEngineIndexable,
        String canonicalUrl,
        /** Only populated for STRUCTURED resumes - already masked/visible-only, taken verbatim from the published snapshot. */
        List<StructuredSnapshotBuilder.SnapshotSection> sections) {

    public static PublicResumeResponse from(Resume resume, String canonicalUrl, List<StructuredSnapshotBuilder.SnapshotSection> sections) {
        return new PublicResumeResponse(
                resume.getPublicId(),
                resume.getName(),
                resume.getSlug(),
                resume.getResumeType().name(),
                resume.isAllowDownload(),
                resume.isSearchEngineIndexable(),
                canonicalUrl,
                sections);
    }
}
