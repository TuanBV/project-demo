package com.cvplatform.sharing;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.cvplatform.analytics.application.AnalyticsService;
import com.cvplatform.analytics.application.ReferrerNormalizer;
import com.cvplatform.analytics.application.UserAgentClassifier;
import com.cvplatform.analytics.application.VisitorHasher;
import com.cvplatform.analytics.domain.DeviceType;
import com.cvplatform.common.config.AppProperties;
import com.cvplatform.common.security.TokenHasher;
import com.cvplatform.resume.domain.Resume;
import com.cvplatform.resume.domain.ResumeStatus;
import com.cvplatform.resume.domain.ResumeType;
import com.cvplatform.resume.domain.ResumeVisibility;
import com.cvplatform.resume.infrastructure.ResumeRepository;
import com.cvplatform.resume.infrastructure.ResumeVersionRepository;
import com.cvplatform.resume.infrastructure.StoredFileRepository;
import com.cvplatform.sharing.application.DownloadNotAllowedException;
import com.cvplatform.sharing.application.PublicResumeGoneException;
import com.cvplatform.sharing.application.PublicResumeNotFoundException;
import com.cvplatform.sharing.application.PublicResumeService;
import com.cvplatform.storage.FileStorage;
import java.time.Instant;
import java.util.Optional;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class PublicResumeServiceTest {

    @Mock
    private ResumeRepository resumeRepository;
    @Mock
    private ResumeVersionRepository resumeVersionRepository;
    @Mock
    private StoredFileRepository storedFileRepository;
    @Mock
    private FileStorage fileStorage;
    @Mock
    private AnalyticsService analyticsService;

    private PublicResumeService publicResumeService;
    private final UUID publicId = UUID.randomUUID();
    private final UUID ownerId = UUID.randomUUID();

    @BeforeEach
    void setUp() {
        publicResumeService = new PublicResumeService(resumeRepository, resumeVersionRepository, storedFileRepository,
                fileStorage, analyticsService, new VisitorHasher(), new UserAgentClassifier(), new ReferrerNormalizer(),
                new AppProperties(), new com.fasterxml.jackson.databind.ObjectMapper());
    }

    private Resume.ResumeBuilder publishedPublicResume() {
        return Resume.builder()
                .id(UUID.randomUUID())
                .ownerId(ownerId)
                .publicId(publicId)
                .name("My CV")
                .slug("my-cv")
                .resumeType(ResumeType.PDF)
                .status(ResumeStatus.PUBLISHED)
                .visibility(ResumeVisibility.PUBLIC);
    }

    @Test
    void unknownPublicIdIsNotFound() {
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> publicResumeService.getPublicData(publicId, "anything"))
                .isInstanceOf(PublicResumeNotFoundException.class);
    }

    @Test
    void privateResumeIsGoneNotNotFound() {
        Resume resume = publishedPublicResume().visibility(ResumeVisibility.PRIVATE).build();
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.of(resume));

        assertThatThrownBy(() -> publicResumeService.getPublicData(publicId, "my-cv"))
                .isInstanceOf(PublicResumeGoneException.class);
    }

    @Test
    void unpublishedResumeIsGone() {
        Resume resume = publishedPublicResume().status(ResumeStatus.DRAFT).build();
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.of(resume));

        assertThatThrownBy(() -> publicResumeService.getPublicData(publicId, "my-cv"))
                .isInstanceOf(PublicResumeGoneException.class);
    }

    @Test
    void deletedResumeIsGone() {
        Resume resume = publishedPublicResume().deletedAt(Instant.now()).build();
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.of(resume));

        assertThatThrownBy(() -> publicResumeService.getPublicData(publicId, "my-cv"))
                .isInstanceOf(PublicResumeGoneException.class);
    }

    @Test
    void publicResumeIsServedRegardlessOfTheExactSlugValue() {
        Resume resume = publishedPublicResume().build();
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.of(resume));

        var response = publicResumeService.getPublicData(publicId, "totally-wrong-slug");

        assertThat(response.publicId()).isEqualTo(publicId);
    }

    @Test
    void unlistedResumeWithCorrectTokenIsServed() {
        String rawToken = "correct-token";
        Resume resume = publishedPublicResume()
                .visibility(ResumeVisibility.UNLISTED)
                .unlistedTokenHash(TokenHasher.sha256(rawToken))
                .build();
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.of(resume));

        var response = publicResumeService.getPublicData(publicId, rawToken);

        assertThat(response.publicId()).isEqualTo(publicId);
    }

    @Test
    void unlistedResumeWithWrongTokenIsNotFoundNotGone() {
        Resume resume = publishedPublicResume()
                .visibility(ResumeVisibility.UNLISTED)
                .unlistedTokenHash(TokenHasher.sha256("correct-token"))
                .build();
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.of(resume));

        assertThatThrownBy(() -> publicResumeService.getPublicData(publicId, "wrong-token"))
                .isInstanceOf(PublicResumeNotFoundException.class);
    }

    @Test
    void downloadIsRejectedWhenNotAllowed() {
        Resume resume = publishedPublicResume().allowDownload(false).build();
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.of(resume));

        assertThatThrownBy(() -> publicResumeService.loadPublicFile(publicId, "my-cv", true))
                .isInstanceOf(DownloadNotAllowedException.class);
    }

    @Test
    void viewIsNotRecordedWhenTheViewerIsTheOwner() {
        Resume resume = publishedPublicResume().build();
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.of(resume));

        publicResumeService.recordView(publicId, "my-cv", "1.2.3.4", "some-agent", null, Optional.of(ownerId));

        verify(analyticsService, never()).recordView(any(), anyString(), any(), any(DeviceType.class));
    }

    @Test
    void viewIsRecordedForAnAnonymousVisitor() {
        Resume resume = publishedPublicResume().build();
        when(resumeRepository.findByPublicId(publicId)).thenReturn(Optional.of(resume));

        publicResumeService.recordView(publicId, "my-cv", "1.2.3.4", "some-agent", "https://www.linkedin.com/feed", Optional.empty());

        verify(analyticsService).recordView(org.mockito.ArgumentMatchers.eq(resume.getId()), anyString(),
                org.mockito.ArgumentMatchers.eq("linkedin.com"), any(DeviceType.class));
    }
}
