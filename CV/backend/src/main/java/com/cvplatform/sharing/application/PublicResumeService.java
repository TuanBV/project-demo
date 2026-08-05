package com.cvplatform.sharing.application;

import com.cvplatform.analytics.application.AnalyticsService;
import com.cvplatform.analytics.application.ReferrerNormalizer;
import com.cvplatform.analytics.application.UserAgentClassifier;
import com.cvplatform.analytics.application.VisitorHasher;
import com.cvplatform.common.config.AppProperties;
import com.cvplatform.common.security.TokenHasher;
import com.cvplatform.resume.application.StructuredSnapshotBuilder;
import com.cvplatform.resume.domain.Resume;
import com.cvplatform.resume.domain.ResumeStatus;
import com.cvplatform.resume.domain.ResumeType;
import com.cvplatform.resume.domain.ResumeVersion;
import com.cvplatform.resume.domain.ResumeVisibility;
import com.cvplatform.resume.domain.StoredFile;
import com.cvplatform.resume.infrastructure.ResumeRepository;
import com.cvplatform.resume.infrastructure.ResumeVersionRepository;
import com.cvplatform.resume.infrastructure.StoredFileRepository;
import com.cvplatform.sharing.api.dto.PublicResumeResponse;
import com.cvplatform.storage.FileStorage;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class PublicResumeService {

    private final ResumeRepository resumeRepository;
    private final ResumeVersionRepository resumeVersionRepository;
    private final StoredFileRepository storedFileRepository;
    private final FileStorage fileStorage;
    private final AnalyticsService analyticsService;
    private final VisitorHasher visitorHasher;
    private final UserAgentClassifier userAgentClassifier;
    private final ReferrerNormalizer referrerNormalizer;
    private final AppProperties appProperties;
    private final ObjectMapper objectMapper;

    public PublicResumeService(ResumeRepository resumeRepository,
                                ResumeVersionRepository resumeVersionRepository,
                                StoredFileRepository storedFileRepository,
                                FileStorage fileStorage,
                                AnalyticsService analyticsService,
                                VisitorHasher visitorHasher,
                                UserAgentClassifier userAgentClassifier,
                                ReferrerNormalizer referrerNormalizer,
                                AppProperties appProperties,
                                ObjectMapper objectMapper) {
        this.resumeRepository = resumeRepository;
        this.resumeVersionRepository = resumeVersionRepository;
        this.storedFileRepository = storedFileRepository;
        this.fileStorage = fileStorage;
        this.analyticsService = analyticsService;
        this.visitorHasher = visitorHasher;
        this.userAgentClassifier = userAgentClassifier;
        this.referrerNormalizer = referrerNormalizer;
        this.appProperties = appProperties;
        this.objectMapper = objectMapper;
    }

    @Transactional(readOnly = true)
    public PublicResumeResponse getPublicData(UUID publicId, String slugOrToken) {
        Resume resume = resolvePublic(publicId, slugOrToken);
        String canonicalUrl = "%s/cv/%s/%s".formatted(appProperties.getPublicSite().getBaseUrl(), resume.getPublicId(), resume.getSlug());
        List<StructuredSnapshotBuilder.SnapshotSection> sections = resume.getResumeType() == ResumeType.STRUCTURED
                ? loadPublishedSections(resume)
                : List.of();
        return PublicResumeResponse.from(resume, canonicalUrl, sections);
    }

    private List<StructuredSnapshotBuilder.SnapshotSection> loadPublishedSections(Resume resume) {
        if (resume.getActiveVersionId() == null) {
            throw new PublicResumeGoneException();
        }
        ResumeVersion version = resumeVersionRepository.findById(resume.getActiveVersionId())
                .orElseThrow(PublicResumeGoneException::new);
        if (version.getSnapshotJson() == null) {
            throw new PublicResumeGoneException();
        }
        try {
            return List.of(objectMapper.readValue(version.getSnapshotJson(), StructuredSnapshotBuilder.SnapshotSection[].class));
        } catch (Exception e) {
            throw new PublicResumeGoneException();
        }
    }

    @Transactional(readOnly = true)
    public Resource loadPublicFile(UUID publicId, String slugOrToken, boolean download) {
        Resume resume = resolvePublic(publicId, slugOrToken);
        if (download && !resume.isAllowDownload()) {
            throw new DownloadNotAllowedException();
        }
        if (resume.getActiveVersionId() == null) {
            throw new PublicResumeGoneException();
        }
        ResumeVersion version = resumeVersionRepository.findById(resume.getActiveVersionId())
                .orElseThrow(PublicResumeGoneException::new);
        if (version.getFileId() == null) {
            throw new PublicResumeGoneException();
        }
        StoredFile file = storedFileRepository.findById(version.getFileId())
                .orElseThrow(PublicResumeGoneException::new);
        return fileStorage.loadPrivate(file.getStorageKey());
    }

    /**
     * Never counts the resume owner's own visits while they're logged in
     * (checked by comparing {@code viewerUserId} against the resume's
     * owner - the caller resolves this optimistically from the bearer
     * token, since this whole endpoint stays public/unauthenticated).
     */
    public void recordView(UUID publicId, String slugOrToken, String ipAddress, String userAgent, String referrerHeader, Optional<UUID> viewerUserId) {
        Resume resume = resolvePublic(publicId, slugOrToken);
        if (viewerUserId.isPresent() && viewerUserId.get().equals(resume.getOwnerId())) {
            return;
        }
        String visitorHash = visitorHasher.hash(ipAddress, userAgent);
        String referrerHost = referrerNormalizer.normalizeHost(referrerHeader);
        var deviceType = userAgentClassifier.classify(userAgent);
        analyticsService.recordView(resume.getId(), visitorHash, referrerHost, deviceType);
    }

    private Resume resolvePublic(UUID publicId, String slugOrToken) {
        Resume resume = resumeRepository.findByPublicId(publicId)
                .orElseThrow(PublicResumeNotFoundException::new);

        if (resume.getVisibility() == ResumeVisibility.UNLISTED) {
            if (resume.getUnlistedTokenHash() == null || !resume.getUnlistedTokenHash().equals(TokenHasher.sha256(slugOrToken))) {
                // Wrong/missing token: treat identically to "doesn't exist" so
                // this endpoint can't be used to confirm a publicId is valid.
                throw new PublicResumeNotFoundException();
            }
        }

        if (resume.isDeleted() || resume.getStatus() != ResumeStatus.PUBLISHED || resume.getVisibility() == ResumeVisibility.PRIVATE) {
            throw new PublicResumeGoneException();
        }

        return resume;
    }
}
