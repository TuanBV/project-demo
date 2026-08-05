package com.cvplatform.resume;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.lenient;
import static org.mockito.Mockito.when;

import com.cvplatform.resume.api.dto.CreateSectionRequest;
import com.cvplatform.resume.api.dto.UpdateSectionRequest;
import com.cvplatform.resume.application.DuplicateSectionTypeException;
import com.cvplatform.resume.application.InvalidSectionOrderException;
import com.cvplatform.resume.application.NotAStructuredResumeException;
import com.cvplatform.resume.application.ResumeNotFoundException;
import com.cvplatform.resume.application.ResumeSectionNotFoundException;
import com.cvplatform.resume.application.ResumeSectionService;
import com.cvplatform.resume.application.SectionContentValidator;
import com.cvplatform.resume.application.StructuredSnapshotBuilder;
import com.cvplatform.resume.domain.Resume;
import com.cvplatform.resume.domain.ResumeSection;
import com.cvplatform.resume.domain.ResumeType;
import com.cvplatform.resume.domain.SectionType;
import com.cvplatform.resume.infrastructure.ResumeRepository;
import com.cvplatform.resume.infrastructure.ResumeSectionRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class ResumeSectionServiceTest {

    @Mock
    private ResumeRepository resumeRepository;
    @Mock
    private ResumeSectionRepository resumeSectionRepository;
    @Mock
    private StructuredSnapshotBuilder structuredSnapshotBuilder;

    private ResumeSectionService service;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final UUID ownerId = UUID.randomUUID();
    private final UUID resumeId = UUID.randomUUID();

    @BeforeEach
    void setUp() {
        service = new ResumeSectionService(resumeRepository, resumeSectionRepository,
                new SectionContentValidator(objectMapper), structuredSnapshotBuilder);
        lenient().when(resumeSectionRepository.save(any(ResumeSection.class))).thenAnswer(inv -> inv.getArgument(0));
    }

    private Resume structuredResume() {
        return Resume.builder().id(resumeId).ownerId(ownerId).name("Web CV").slug("web-cv").resumeType(ResumeType.STRUCTURED).build();
    }

    private ResumeSection section(SectionType type, int position, String content) {
        return ResumeSection.builder()
                .id(UUID.randomUUID()).resumeId(resumeId).sectionType(type).title(type.name())
                .position(position).visible(true).contentJson(content)
                .createdAt(Instant.now()).updatedAt(Instant.now())
                .build();
    }

    @Test
    void rejectsOperatingOnSectionsOfAPdfResume() {
        Resume pdfResume = Resume.builder().id(resumeId).ownerId(ownerId).resumeType(ResumeType.PDF).build();
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(pdfResume));

        assertThatThrownBy(() -> service.list(resumeId, ownerId)).isInstanceOf(NotAStructuredResumeException.class);
    }

    @Test
    void createAssignsIncrementingPositions() throws Exception {
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(structuredResume()));
        when(resumeSectionRepository.findByResumeIdOrderByPositionAsc(resumeId)).thenReturn(List.of());
        when(resumeSectionRepository.findTopByResumeIdOrderByPositionDesc(resumeId))
                .thenReturn(Optional.of(section(SectionType.SUMMARY, 0, "{}")));

        var content = objectMapper.readTree("{\"text\":\"hi\"}");
        ResumeSection created = service.create(resumeId, ownerId, new CreateSectionRequest(SectionType.ADDITIONAL, "Extra", content));

        assertThat(created.getPosition()).isEqualTo(1);
    }

    @Test
    void rejectsCreatingASecondSectionOfTheSameType() throws Exception {
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(structuredResume()));
        when(resumeSectionRepository.findByResumeIdOrderByPositionAsc(resumeId))
                .thenReturn(List.of(section(SectionType.SUMMARY, 0, "{}")));

        var content = objectMapper.readTree("{\"text\":\"hi\"}");
        assertThatThrownBy(() -> service.create(resumeId, ownerId, new CreateSectionRequest(SectionType.SUMMARY, "Summary", content)))
                .isInstanceOf(DuplicateSectionTypeException.class);
    }

    @Test
    void updateAppliesOnlyProvidedFields() {
        ResumeSection existing = section(SectionType.SUMMARY, 0, "{\"text\":\"old\"}");
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(structuredResume()));
        when(resumeSectionRepository.findByIdAndResumeId(existing.getId(), resumeId)).thenReturn(Optional.of(existing));

        ResumeSection updated = service.update(resumeId, ownerId, existing.getId(), new UpdateSectionRequest(null, null, false));

        assertThat(updated.isVisible()).isFalse();
        assertThat(updated.getContentJson()).isEqualTo("{\"text\":\"old\"}");
    }

    @Test
    void updateThrowsWhenSectionDoesNotBelongToResume() {
        UUID sectionId = UUID.randomUUID();
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(structuredResume()));
        when(resumeSectionRepository.findByIdAndResumeId(sectionId, resumeId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> service.update(resumeId, ownerId, sectionId, new UpdateSectionRequest("x", null, null)))
                .isInstanceOf(ResumeSectionNotFoundException.class);
    }

    @Test
    void reorderRejectsAMismatchedIdSet() {
        ResumeSection s1 = section(SectionType.SUMMARY, 0, "{}");
        ResumeSection s2 = section(SectionType.SKILLS, 1, "{}");
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(structuredResume()));
        when(resumeSectionRepository.findByResumeIdOrderByPositionAsc(resumeId)).thenReturn(List.of(s1, s2));

        assertThatThrownBy(() -> service.reorder(resumeId, ownerId, List.of(s1.getId(), UUID.randomUUID())))
                .isInstanceOf(InvalidSectionOrderException.class);
    }

    @Test
    void reorderAppliesNewPositions() {
        ResumeSection s1 = section(SectionType.SUMMARY, 0, "{}");
        ResumeSection s2 = section(SectionType.SKILLS, 1, "{}");
        when(resumeRepository.findByIdAndOwnerId(resumeId, ownerId)).thenReturn(Optional.of(structuredResume()));
        when(resumeSectionRepository.findByResumeIdOrderByPositionAsc(resumeId)).thenReturn(List.of(s1, s2));
        when(resumeSectionRepository.saveAll(any())).thenAnswer(inv -> inv.getArgument(0));

        service.reorder(resumeId, ownerId, List.of(s2.getId(), s1.getId()));

        assertThat(s2.getPosition()).isEqualTo(0);
        assertThat(s1.getPosition()).isEqualTo(1);
    }

    @Test
    void aUserCannotListSectionsOfAnotherUsersResume() {
        UUID otherOwnerId = UUID.randomUUID();
        when(resumeRepository.findByIdAndOwnerId(resumeId, otherOwnerId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> service.list(resumeId, otherOwnerId))
                .isInstanceOf(ResumeNotFoundException.class);
    }

    @Test
    void aUserCannotCreateASectionOnAnotherUsersResume() throws Exception {
        UUID otherOwnerId = UUID.randomUUID();
        when(resumeRepository.findByIdAndOwnerId(resumeId, otherOwnerId)).thenReturn(Optional.empty());

        var content = objectMapper.readTree("{\"text\":\"hi\"}");
        assertThatThrownBy(() -> service.create(resumeId, otherOwnerId, new CreateSectionRequest(SectionType.SUMMARY, "Summary", content)))
                .isInstanceOf(ResumeNotFoundException.class);
    }

    @Test
    void aUserCannotDeleteASectionOnAnotherUsersResume() {
        UUID otherOwnerId = UUID.randomUUID();
        UUID sectionId = UUID.randomUUID();
        when(resumeRepository.findByIdAndOwnerId(resumeId, otherOwnerId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> service.delete(resumeId, otherOwnerId, sectionId))
                .isInstanceOf(ResumeNotFoundException.class);
    }
}
