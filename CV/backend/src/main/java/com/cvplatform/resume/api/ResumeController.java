package com.cvplatform.resume.api;

import com.cvplatform.analytics.api.dto.AnalyticsSummaryResponse;
import com.cvplatform.analytics.application.AnalyticsService;
import com.cvplatform.common.config.AppProperties;
import com.cvplatform.identity.security.CurrentUserProvider;
import com.cvplatform.resume.api.dto.CreateResumeRequest;
import com.cvplatform.resume.api.dto.ResumeResponse;
import com.cvplatform.resume.api.dto.ResumeVersionResponse;
import com.cvplatform.resume.api.dto.UpdateResumeRequest;
import com.cvplatform.resume.application.ResumeMutationResult;
import com.cvplatform.resume.application.ResumeService;
import com.cvplatform.resume.domain.Resume;
import com.cvplatform.resume.domain.ResumeVersion;
import com.cvplatform.resume.infrastructure.StoredFileRepository;
import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/v1/resumes")
public class ResumeController {

    private final ResumeService resumeService;
    private final AnalyticsService analyticsService;
    private final CurrentUserProvider currentUserProvider;
    private final StoredFileRepository storedFileRepository;
    private final AppProperties appProperties;

    public ResumeController(ResumeService resumeService,
                             AnalyticsService analyticsService,
                             CurrentUserProvider currentUserProvider,
                             StoredFileRepository storedFileRepository,
                             AppProperties appProperties) {
        this.resumeService = resumeService;
        this.analyticsService = analyticsService;
        this.currentUserProvider = currentUserProvider;
        this.storedFileRepository = storedFileRepository;
        this.appProperties = appProperties;
    }

    @GetMapping
    public List<ResumeResponse> list(@RequestParam(defaultValue = "false") boolean includeDeleted) {
        UUID ownerId = currentUserProvider.requireUserId();
        return resumeService.list(ownerId, includeDeleted).stream()
                .map(this::toResponse)
                .toList();
    }

    @PostMapping
    public ResumeResponse create(@Valid @RequestBody CreateResumeRequest request) {
        UUID ownerId = currentUserProvider.requireUserId();
        return toResponse(resumeService.create(ownerId, request));
    }

    @GetMapping("/{resumeId}")
    public ResumeResponse get(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        return toResponse(resumeService.getOwned(resumeId, ownerId));
    }

    @PatchMapping("/{resumeId}")
    public ResumeResponse update(@PathVariable UUID resumeId, @Valid @RequestBody UpdateResumeRequest request) {
        UUID ownerId = currentUserProvider.requireUserId();
        return toResponse(resumeService.update(resumeId, ownerId, request));
    }

    @DeleteMapping("/{resumeId}")
    public ResponseEntity<Void> softDelete(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        resumeService.softDelete(resumeId, ownerId);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{resumeId}/restore")
    public ResumeResponse restore(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        return toResponse(resumeService.restore(resumeId, ownerId));
    }

    @PostMapping("/{resumeId}/duplicate")
    public ResumeResponse duplicate(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        return toResponse(resumeService.duplicate(resumeId, ownerId));
    }

    @PostMapping("/{resumeId}/publish")
    public ResumeResponse publish(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        return toResponse(resumeService.publish(resumeId, ownerId));
    }

    @PostMapping("/{resumeId}/unpublish")
    public ResumeResponse unpublish(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        return toResponse(resumeService.unpublish(resumeId, ownerId));
    }

    @PostMapping("/{resumeId}/regenerate-link")
    public ResumeResponse regenerateLink(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        return toResponse(resumeService.regenerateUnlistedToken(resumeId, ownerId));
    }

    @PostMapping(value = "/{resumeId}/versions/pdf", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResumeVersionResponse uploadPdfVersion(@PathVariable UUID resumeId, @RequestPart("file") MultipartFile file) {
        UUID ownerId = currentUserProvider.requireUserId();
        ResumeVersion version = resumeService.uploadPdfVersion(resumeId, ownerId, file);
        Resume resume = resumeService.getOwned(resumeId, ownerId);
        return toVersionResponse(version, resume);
    }

    @GetMapping("/{resumeId}/versions")
    public List<ResumeVersionResponse> listVersions(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        Resume resume = resumeService.getOwned(resumeId, ownerId);
        return resumeService.listVersions(resumeId, ownerId).stream()
                .map(v -> toVersionResponse(v, resume))
                .toList();
    }

    @PostMapping("/{resumeId}/versions/{versionId}/activate")
    public ResumeResponse activateVersion(@PathVariable UUID resumeId, @PathVariable UUID versionId) {
        UUID ownerId = currentUserProvider.requireUserId();
        return toResponse(resumeService.activateVersion(resumeId, ownerId, versionId));
    }

    @DeleteMapping("/{resumeId}/versions/{versionId}")
    public ResponseEntity<Void> deleteVersion(@PathVariable UUID resumeId, @PathVariable UUID versionId) {
        UUID ownerId = currentUserProvider.requireUserId();
        resumeService.deleteVersion(resumeId, ownerId, versionId);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/{resumeId}/preview/file")
    public ResponseEntity<Resource> previewFile(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        Resource resource = resumeService.previewActiveFile(resumeId, ownerId);
        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_PDF)
                .header(HttpHeaders.CONTENT_DISPOSITION, "inline")
                .body(resource);
    }

    @GetMapping("/{resumeId}/analytics/summary")
    public AnalyticsSummaryResponse analyticsSummary(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        resumeService.getOwned(resumeId, ownerId);
        return analyticsService.summary(resumeId);
    }

    private ResumeResponse toResponse(Resume resume) {
        long viewCount = analyticsService.countTotalViews(resume.getId());
        return ResumeResponse.from(resume, appProperties.getResume().getTrashRetention(), viewCount, appProperties.getPublicSite().getBaseUrl());
    }

    private ResumeResponse toResponse(ResumeMutationResult result) {
        long viewCount = analyticsService.countTotalViews(result.resume().getId());
        return ResumeResponse.from(result.resume(), appProperties.getResume().getTrashRetention(), viewCount,
                appProperties.getPublicSite().getBaseUrl(), result.rawUnlistedToken());
    }

    private ResumeVersionResponse toVersionResponse(ResumeVersion version, Resume resume) {
        var file = version.getFileId() != null ? storedFileRepository.findById(version.getFileId()).orElse(null) : null;
        boolean active = version.getId().equals(resume.getActiveVersionId());
        return ResumeVersionResponse.from(version, file, active);
    }
}
