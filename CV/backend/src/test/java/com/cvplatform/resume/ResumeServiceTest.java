package com.cvplatform.resume;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.Mockito.lenient;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.cvplatform.common.config.AppProperties;
import com.cvplatform.resume.api.dto.CreateResumeRequest;
import com.cvplatform.resume.api.dto.UpdateResumeRequest;
import com.cvplatform.resume.application.CannotDeleteActiveVersionException;
import com.cvplatform.resume.application.CannotPublishException;
import com.cvplatform.resume.application.PdfFileValidator;
import com.cvplatform.resume.application.ResumeNotFoundException;
import com.cvplatform.resume.application.ResumeService;
import com.cvplatform.resume.application.ResumeVersionNotFoundException;
import com.cvplatform.resume.application.RestoreWindowExpiredException;
import com.cvplatform.resume.application.StructuredSnapshotBuilder;
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
import java.time.temporal.ChronoUnit;
import java.util.Optional;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mock.web.MockMultipartFile;

@ExtendWith(MockitoExtension.class)
class ResumeServiceTest {

    @Mock
    private ResumeRepository resumeRepository;
    @Mock
    private ResumeVersionRepository resumeVersionRepository;
    @Mock
    private StoredFileRepository storedFileRepository;
    @Mock
    private FileStorage fileStorage;
    @Mock
    private StructuredSnapshotBuilder structuredSnapshotBuilder;

    private final AppProperties appProperties = new AppProperties();
    private ResumeService resumeService;

    private final UUID ownerId = UUID.randomUUID();
    private final UUID otherOwnerId = UUID.randomUUID();

    @BeforeEach
    void setUp() {
        resumeService = new ResumeService(resumeRepository, resumeVersionRepository, storedFileRepository,
                fileStorage, new PdfFileValidator(appProperties), structuredSnapshotBuilder, appProperties);
        lenient().when(resumeRepository.save(any(Resume.class))).thenAnswer(inv -> inv.getArgument(0));
        lenient().when(resumeRepository.saveAndFlush(any(Resume.class))).thenAnswer(inv -> inv.getArgument(0));
    }

    private Resume ownedResume(UUID id) {
        return Resume.builder()
                .id(id)
                .ownerId(ownerId)
                .name("My CV")
                .slug("my-cv")
                .resumeType(ResumeType.PDF)
                .status(ResumeStatus.DRAFT)
                .visibility(ResumeVisibility.PRIVATE)
                .build();
    }

    @Test
    void createPersistsWithPrivateDraftDefaults() {
        when(resumeRepository.save(any(Resume.class))).thenAnswer(inv -> inv.getArgument(0));

        Resume created = resumeService.create(ownerId, new CreateResumeRequest("My CV", ResumeType.PDF));

        assertThat(created.getStatus()).isEqualTo(ResumeStatus.DRAFT);
        assertThat(created.getVisibility()).isEqualTo(ResumeVisibility.PRIVATE);
        assertThat(created.getOwnerId()).isEqualTo(ownerId);
        assertThat(created.getPublicId()).isNotNull();
    }

    @Test
    void getOwnedThrowsWhenResumeBelongsToAnotherUser() {
        UUID resumeId = UUID.randomUUID();
        when(resumeRepository.findByIdAndOwnerId(resumeId, otherOwnerId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> resumeService.getOwned(resumeId, otherOwnerId))
                .isInstanceOf(ResumeNotFoundException.class);
    }

    @Test
    void updateMakingDefaultUnsetsThePreviousDefaultResume() {
        UUID resumeId = UUID.randomUUID();
        Resume target = ownedResume(resumeId);
        UUID previousDefaultId = UUID.randomUUID();
        Resume previousDefault = ownedResume(previousDefaultId);
        previousDefault.setDefault(true);

        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(target));
        when(resumeRepository.findByOwnerIdAndIsDefaultTrueAndDeletedAtIsNull(ownerId)).thenReturn(Optional.of(previousDefault));

        resumeService.update(resumeId, ownerId, new UpdateResumeRequest(null, true, null, null, null));

        assertThat(previousDefault.isDefault()).isFalse();
        assertThat(target.isDefault()).isTrue();
        verify(resumeRepository).saveAndFlush(previousDefault);
    }

    @Test
    void softDeleteClearsDefaultFlagAndSetsDeletedAt() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setDefault(true);
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));

        resumeService.softDelete(resumeId, ownerId);

        assertThat(resume.getDeletedAt()).isNotNull();
        assertThat(resume.isDefault()).isFalse();
    }

    @Test
    void restoreWithinRetentionWindowSucceeds() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setDeletedAt(Instant.now().minus(1, ChronoUnit.DAYS));
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));

        Resume restored = resumeService.restore(resumeId, ownerId);

        assertThat(restored.getDeletedAt()).isNull();
    }

    @Test
    void restoreAfterRetentionWindowExpiredThrows() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setDeletedAt(Instant.now().minus(40, ChronoUnit.DAYS));
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));

        assertThatThrownBy(() -> resumeService.restore(resumeId, ownerId))
                .isInstanceOf(RestoreWindowExpiredException.class);
    }

    @Test
    void uploadPdfVersionCreatesFirstVersionAndActivatesIt() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));
        when(resumeVersionRepository.findTopByResumeIdOrderByVersionNumberDesc(resumeId)).thenReturn(Optional.empty());
        when(fileStorage.store(any(StoreFileCommand.class)))
                .thenReturn(new StoredObjectMetadata("MINIO", "resumes/x/y.pdf", 20, "checksum"));
        when(storedFileRepository.save(any(StoredFile.class))).thenAnswer(inv -> {
            StoredFile f = inv.getArgument(0);
            f.setId(UUID.randomUUID());
            return f;
        });
        when(resumeVersionRepository.save(any(ResumeVersion.class))).thenAnswer(inv -> {
            ResumeVersion v = inv.getArgument(0);
            v.setId(UUID.randomUUID());
            return v;
        });

        var file = new MockMultipartFile("file", "resume.pdf", "application/pdf", "%PDF-1.4 body".getBytes());
        ResumeVersion version = resumeService.uploadPdfVersion(resumeId, ownerId, file);

        assertThat(version.getVersionNumber()).isEqualTo(1);
        assertThat(resume.getActiveVersionId()).isEqualTo(version.getId());
    }

    @Test
    void cannotDeleteTheActiveVersion() {
        UUID resumeId = UUID.randomUUID();
        UUID versionId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setActiveVersionId(versionId);
        ResumeVersion version = ResumeVersion.builder()
                .id(versionId).resumeId(resumeId).versionNumber(1)
                .sourceType(ResumeVersionSourceType.PDF).createdBy(ownerId).createdAt(Instant.now())
                .build();

        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));
        when(resumeVersionRepository.findByIdAndResumeId(versionId, resumeId)).thenReturn(Optional.of(version));

        assertThatThrownBy(() -> resumeService.deleteVersion(resumeId, ownerId, versionId))
                .isInstanceOf(CannotDeleteActiveVersionException.class);
    }

    @Test
    void activatingAVersionFromAnotherResumeIsRejected() {
        UUID resumeId = UUID.randomUUID();
        UUID versionId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);

        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));
        when(resumeVersionRepository.findByIdAndResumeId(versionId, resumeId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> resumeService.activateVersion(resumeId, ownerId, versionId))
                .isInstanceOf(ResumeVersionNotFoundException.class);
    }

    @Test
    void cannotPublishAResumeWithoutAnActiveVersion() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));

        assertThatThrownBy(() -> resumeService.publish(resumeId, ownerId))
                .isInstanceOf(CannotPublishException.class);
    }

    @Test
    void publishingSetsStatusAndPublishedAt() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setActiveVersionId(UUID.randomUUID());
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));

        Resume published = resumeService.publish(resumeId, ownerId);

        assertThat(published.getStatus()).isEqualTo(ResumeStatus.PUBLISHED);
        assertThat(published.getPublishedAt()).isNotNull();
    }

    @Test
    void unpublishingRevertsStatusToDraft() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setStatus(ResumeStatus.PUBLISHED);
        resume.setPublishedAt(Instant.now());
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));

        Resume unpublished = resumeService.unpublish(resumeId, ownerId);

        assertThat(unpublished.getStatus()).isEqualTo(ResumeStatus.DRAFT);
    }

    @Test
    void switchingToUnlistedGeneratesAFreshToken() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));

        var result = resumeService.update(resumeId, ownerId, new UpdateResumeRequest(null, null, ResumeVisibility.UNLISTED, null, null));

        assertThat(result.resume().getVisibility()).isEqualTo(ResumeVisibility.UNLISTED);
        assertThat(result.resume().getUnlistedTokenHash()).isNotNull();
        assertThat(result.rawUnlistedToken()).isNotNull();
    }

    @Test
    void switchingAwayFromUnlistedClearsTheStoredTokenHash() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setVisibility(ResumeVisibility.UNLISTED);
        resume.setUnlistedTokenHash("some-old-hash");
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));

        var result = resumeService.update(resumeId, ownerId, new UpdateResumeRequest(null, null, ResumeVisibility.PUBLIC, null, null));

        assertThat(result.resume().getVisibility()).isEqualTo(ResumeVisibility.PUBLIC);
        assertThat(result.resume().getUnlistedTokenHash()).isNull();
        assertThat(result.rawUnlistedToken()).isNull();
    }

    @Test
    void regenerateUnlistedTokenReplacesTheHashEachTime() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setVisibility(ResumeVisibility.UNLISTED);
        resume.setUnlistedTokenHash("old-hash");
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));

        var result = resumeService.regenerateUnlistedToken(resumeId, ownerId);

        assertThat(result.rawUnlistedToken()).isNotNull();
        assertThat(result.resume().getUnlistedTokenHash()).isNotEqualTo("old-hash");
    }

    @Test
    void cannotPublishAStructuredResumeWithNoVisibleSections() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setResumeType(ResumeType.STRUCTURED);
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));
        when(structuredSnapshotBuilder.buildVisibleSections(resumeId)).thenReturn(java.util.List.of());

        assertThatThrownBy(() -> resumeService.publish(resumeId, ownerId))
                .isInstanceOf(CannotPublishException.class);
    }

    @Test
    void publishingAStructuredResumeCreatesASnapshotVersion() {
        UUID resumeId = UUID.randomUUID();
        Resume resume = ownedResume(resumeId);
        resume.setResumeType(ResumeType.STRUCTURED);
        var section = new StructuredSnapshotBuilder.SnapshotSection("SUMMARY", "Summary", 0, null);
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(resume));
        when(structuredSnapshotBuilder.buildVisibleSections(resumeId)).thenReturn(java.util.List.of(section));
        when(structuredSnapshotBuilder.buildSnapshotJson(resumeId)).thenReturn("[{\"type\":\"SUMMARY\"}]");
        when(resumeVersionRepository.findTopByResumeIdOrderByVersionNumberDesc(resumeId)).thenReturn(Optional.empty());
        when(resumeVersionRepository.save(any(ResumeVersion.class))).thenAnswer(inv -> {
            ResumeVersion v = inv.getArgument(0);
            v.setId(UUID.randomUUID());
            return v;
        });

        Resume published = resumeService.publish(resumeId, ownerId);

        assertThat(published.getStatus()).isEqualTo(ResumeStatus.PUBLISHED);
        assertThat(published.getActiveVersionId()).isNotNull();
        verify(resumeVersionRepository).save(argThat(v -> v.getSourceType() == ResumeVersionSourceType.STRUCTURED_SNAPSHOT));
    }
}
