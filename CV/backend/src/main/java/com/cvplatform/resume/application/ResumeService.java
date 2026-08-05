package com.cvplatform.resume.application;

import com.cvplatform.common.config.AppProperties;
import com.cvplatform.common.security.TokenHasher;
import com.cvplatform.resume.api.dto.CreateResumeRequest;
import com.cvplatform.resume.api.dto.UpdateResumeRequest;
import com.cvplatform.resume.domain.Resume;
import com.cvplatform.resume.domain.ResumeStatus;
import com.cvplatform.resume.domain.ResumeType;
import com.cvplatform.resume.domain.ResumeVersion;
import com.cvplatform.resume.domain.ResumeVersionSourceType;
import com.cvplatform.resume.domain.ResumeVisibility;
import com.cvplatform.resume.domain.StoredFile;
import com.cvplatform.resume.infrastructure.ResumeRepository;
import com.cvplatform.resume.infrastructure.ResumeVersionRepository;
import com.cvplatform.resume.infrastructure.StoredFileRepository;
import com.cvplatform.storage.FileStorage;
import com.cvplatform.storage.StoreFileCommand;
import com.cvplatform.storage.StoredObjectMetadata;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

@Service
@Transactional
public class ResumeService {

    private final ResumeRepository resumeRepository;
    private final ResumeVersionRepository resumeVersionRepository;
    private final StoredFileRepository storedFileRepository;
    private final FileStorage fileStorage;
    private final PdfFileValidator pdfFileValidator;
    private final StructuredSnapshotBuilder structuredSnapshotBuilder;
    private final AppProperties appProperties;

    public ResumeService(ResumeRepository resumeRepository,
                          ResumeVersionRepository resumeVersionRepository,
                          StoredFileRepository storedFileRepository,
                          FileStorage fileStorage,
                          PdfFileValidator pdfFileValidator,
                          StructuredSnapshotBuilder structuredSnapshotBuilder,
                          AppProperties appProperties) {
        this.resumeRepository = resumeRepository;
        this.resumeVersionRepository = resumeVersionRepository;
        this.storedFileRepository = storedFileRepository;
        this.fileStorage = fileStorage;
        this.pdfFileValidator = pdfFileValidator;
        this.structuredSnapshotBuilder = structuredSnapshotBuilder;
        this.appProperties = appProperties;
    }

    @Transactional(readOnly = true)
    public List<Resume> list(UUID ownerId, boolean includeDeleted) {
        return includeDeleted
                ? resumeRepository.findByOwnerIdOrderByUpdatedAtDesc(ownerId)
                : resumeRepository.findByOwnerIdAndDeletedAtIsNullOrderByUpdatedAtDesc(ownerId);
    }

    @Transactional(readOnly = true)
    public Resume getOwned(UUID resumeId, UUID ownerId) {
        return requireOwned(resumeId, ownerId);
    }

    public Resume create(UUID ownerId, CreateResumeRequest request) {
        Resume resume = Resume.builder()
                .ownerId(ownerId)
                .name(request.name().trim())
                .slug(Slugs.slugify(request.name()))
                .resumeType(request.resumeType())
                .status(ResumeStatus.DRAFT)
                .visibility(ResumeVisibility.PRIVATE)
                .build();
        return resumeRepository.save(resume);
    }

    public ResumeMutationResult update(UUID resumeId, UUID ownerId, UpdateResumeRequest request) {
        Resume resume = requireOwned(resumeId, ownerId);

        if (request.name() != null && !request.name().isBlank()) {
            resume.setName(request.name().trim());
            resume.setSlug(Slugs.slugify(request.name()));
        }

        if (request.isDefault() != null) {
            applyDefaultFlag(resume, request.isDefault());
        }

        if (request.allowDownload() != null) {
            resume.setAllowDownload(request.allowDownload());
        }
        if (request.searchEngineIndexable() != null) {
            resume.setSearchEngineIndexable(request.searchEngineIndexable());
        }

        String rawUnlistedToken = null;
        if (request.visibility() != null && request.visibility() != resume.getVisibility()) {
            rawUnlistedToken = applyVisibilityChange(resume, request.visibility());
        }

        resume = resumeRepository.save(resume);
        return new ResumeMutationResult(resume, rawUnlistedToken);
    }

    /**
     * Switching TO unlisted always mints a fresh token (never reuses one
     * that might have leaked from a previous unlisted period); switching
     * AWAY from unlisted clears the stored hash so an old leaked link stops
     * working immediately even if visibility is switched back later.
     */
    private String applyVisibilityChange(Resume resume, ResumeVisibility newVisibility) {
        resume.setVisibility(newVisibility);
        if (newVisibility == ResumeVisibility.UNLISTED) {
            String rawToken = TokenHasher.generateOpaqueToken(24);
            resume.setUnlistedTokenHash(TokenHasher.sha256(rawToken));
            return rawToken;
        }
        resume.setUnlistedTokenHash(null);
        return null;
    }

    public ResumeMutationResult regenerateUnlistedToken(UUID resumeId, UUID ownerId) {
        Resume resume = requireOwned(resumeId, ownerId);
        String rawToken = TokenHasher.generateOpaqueToken(24);
        resume.setUnlistedTokenHash(TokenHasher.sha256(rawToken));
        resume = resumeRepository.save(resume);
        return new ResumeMutationResult(resume, rawToken);
    }

    public Resume publish(UUID resumeId, UUID ownerId) {
        Resume resume = requireOwned(resumeId, ownerId);

        if (resume.getResumeType() == ResumeType.STRUCTURED) {
            publishStructuredSnapshot(resume);
        } else if (resume.getActiveVersionId() == null) {
            throw new CannotPublishException("Upload a file before publishing this CV");
        }

        resume.setStatus(ResumeStatus.PUBLISHED);
        resume.setPublishedAt(Instant.now());
        return resumeRepository.save(resume);
    }

    /**
     * Every publish of a STRUCTURED resume freezes a brand new immutable
     * snapshot version from the current sections (visible-only, contact
     * fields masked) - the public page always serves this snapshot, never
     * live draft data, exactly like PDF versions already work.
     */
    private void publishStructuredSnapshot(Resume resume) {
        List<StructuredSnapshotBuilder.SnapshotSection> sections = structuredSnapshotBuilder.buildVisibleSections(resume.getId());
        if (sections.isEmpty()) {
            throw new CannotPublishException("Add at least one visible section before publishing this CV");
        }
        String snapshotJson = structuredSnapshotBuilder.buildSnapshotJson(resume.getId());

        int nextVersionNumber = resumeVersionRepository.findTopByResumeIdOrderByVersionNumberDesc(resume.getId())
                .map(v -> v.getVersionNumber() + 1)
                .orElse(1);

        ResumeVersion version = resumeVersionRepository.save(ResumeVersion.builder()
                .resumeId(resume.getId())
                .versionNumber(nextVersionNumber)
                .sourceType(ResumeVersionSourceType.STRUCTURED_SNAPSHOT)
                .snapshotJson(snapshotJson)
                .createdBy(resume.getOwnerId())
                .createdAt(Instant.now())
                .build());

        resume.setActiveVersionId(version.getId());
    }

    public Resume unpublish(UUID resumeId, UUID ownerId) {
        Resume resume = requireOwned(resumeId, ownerId);
        resume.setStatus(ResumeStatus.DRAFT);
        return resumeRepository.save(resume);
    }

    private void applyDefaultFlag(Resume resume, boolean makeDefault) {
        if (makeDefault && !resume.isDefault()) {
            resumeRepository.findByOwnerIdAndIsDefaultTrueAndDeletedAtIsNull(resume.getOwnerId())
                    .filter(current -> !current.getId().equals(resume.getId()))
                    .ifPresent(current -> {
                        current.setDefault(false);
                        resumeRepository.saveAndFlush(current);
                    });
        }
        resume.setDefault(makeDefault);
    }

    public void softDelete(UUID resumeId, UUID ownerId) {
        Resume resume = requireOwned(resumeId, ownerId);
        resume.setDeletedAt(Instant.now());
        resume.setDefault(false);
        resumeRepository.save(resume);
    }

    public Resume restore(UUID resumeId, UUID ownerId) {
        Resume resume = requireOwned(resumeId, ownerId);
        if (resume.getDeletedAt() == null) {
            return resume;
        }
        Instant restorableUntil = resume.getDeletedAt().plus(appProperties.getResume().getTrashRetention());
        if (Instant.now().isAfter(restorableUntil)) {
            throw new RestoreWindowExpiredException();
        }
        resume.setDeletedAt(null);
        return resumeRepository.save(resume);
    }

    public Resume duplicate(UUID resumeId, UUID ownerId) {
        Resume source = requireOwned(resumeId, ownerId);

        Resume copy = Resume.builder()
                .ownerId(ownerId)
                .name(source.getName() + " (Copy)")
                .slug(Slugs.slugify(source.getName() + " copy"))
                .resumeType(source.getResumeType())
                .status(ResumeStatus.DRAFT)
                .visibility(ResumeVisibility.PRIVATE)
                .build();
        copy = resumeRepository.save(copy);

        if (source.getActiveVersionId() != null) {
            ResumeVersion sourceVersion = resumeVersionRepository.findById(source.getActiveVersionId()).orElse(null);
            if (sourceVersion != null) {
                ResumeVersion newVersion = ResumeVersion.builder()
                        .resumeId(copy.getId())
                        .versionNumber(1)
                        .sourceType(sourceVersion.getSourceType())
                        .fileId(sourceVersion.getFileId())
                        .snapshotJson(sourceVersion.getSnapshotJson())
                        .createdBy(ownerId)
                        .createdAt(Instant.now())
                        .build();
                newVersion = resumeVersionRepository.save(newVersion);
                copy.setActiveVersionId(newVersion.getId());
                copy = resumeRepository.save(copy);
            }
        }

        return copy;
    }

    @Transactional(readOnly = true)
    public List<ResumeVersion> listVersions(UUID resumeId, UUID ownerId) {
        requireOwned(resumeId, ownerId);
        return resumeVersionRepository.findByResumeIdOrderByVersionNumberDesc(resumeId);
    }

    public ResumeVersion uploadPdfVersion(UUID resumeId, UUID ownerId, MultipartFile file) {
        Resume resume = requireOwned(resumeId, ownerId);
        if (resume.getResumeType() != ResumeType.PDF) {
            throw new InvalidFileException("This resume is not a PDF resume");
        }

        pdfFileValidator.validate(file);
        byte[] content = readBytes(file);

        StoredObjectMetadata stored = fileStorage.store(new StoreFileCommand(ownerId, file.getOriginalFilename(), file.getContentType(), content));
        StoredFile storedFile = storedFileRepository.save(StoredFile.builder()
                .ownerId(ownerId)
                .storageProvider(stored.storageProvider())
                .storageKey(stored.storageKey())
                .originalFilename(file.getOriginalFilename())
                .contentType(file.getContentType())
                .sizeBytes(stored.sizeBytes())
                .checksum(stored.checksum())
                .createdAt(Instant.now())
                .build());

        int nextVersionNumber = resumeVersionRepository.findTopByResumeIdOrderByVersionNumberDesc(resumeId)
                .map(v -> v.getVersionNumber() + 1)
                .orElse(1);

        ResumeVersion version = resumeVersionRepository.save(ResumeVersion.builder()
                .resumeId(resumeId)
                .versionNumber(nextVersionNumber)
                .sourceType(ResumeVersionSourceType.PDF)
                .fileId(storedFile.getId())
                .createdBy(ownerId)
                .createdAt(Instant.now())
                .build());

        // A fresh upload becomes the active version immediately - the public
        // link (once published, Phase 3) always shows the latest upload; an
        // older version stays available for explicit rollback via activate().
        resume.setActiveVersionId(version.getId());
        resumeRepository.save(resume);

        return version;
    }

    public Resume activateVersion(UUID resumeId, UUID ownerId, UUID versionId) {
        Resume resume = requireOwned(resumeId, ownerId);
        ResumeVersion version = resumeVersionRepository.findByIdAndResumeId(versionId, resumeId)
                .orElseThrow(ResumeVersionNotFoundException::new);

        resume.setActiveVersionId(version.getId());
        return resumeRepository.save(resume);
    }

    public void deleteVersion(UUID resumeId, UUID ownerId, UUID versionId) {
        Resume resume = requireOwned(resumeId, ownerId);
        ResumeVersion version = resumeVersionRepository.findByIdAndResumeId(versionId, resumeId)
                .orElseThrow(ResumeVersionNotFoundException::new);

        if (version.getId().equals(resume.getActiveVersionId())) {
            throw new CannotDeleteActiveVersionException();
        }

        resumeVersionRepository.delete(version);

        if (version.getFileId() != null) {
            storedFileRepository.findById(version.getFileId()).ifPresent(file -> {
                fileStorage.delete(file.getStorageKey());
                file.setDeletedAt(Instant.now());
                storedFileRepository.save(file);
            });
        }
    }

    @Transactional(readOnly = true)
    public Resource previewActiveFile(UUID resumeId, UUID ownerId) {
        Resume resume = requireOwned(resumeId, ownerId);
        if (resume.getActiveVersionId() == null) {
            throw new ResumeVersionNotFoundException();
        }
        ResumeVersion version = resumeVersionRepository.findById(resume.getActiveVersionId())
                .orElseThrow(ResumeVersionNotFoundException::new);
        if (version.getFileId() == null) {
            throw new ResumeVersionNotFoundException();
        }
        StoredFile file = storedFileRepository.findById(version.getFileId())
                .orElseThrow(ResumeVersionNotFoundException::new);
        return fileStorage.loadPrivate(file.getStorageKey());
    }

    private Resume requireOwned(UUID resumeId, UUID ownerId) {
        return resumeRepository.findByIdAndOwnerId(resumeId, ownerId)
                .orElseThrow(ResumeNotFoundException::new);
    }

    private static byte[] readBytes(MultipartFile file) {
        try {
            return file.getBytes();
        } catch (Exception e) {
            throw new InvalidFileException("Could not read the uploaded file");
        }
    }
}
