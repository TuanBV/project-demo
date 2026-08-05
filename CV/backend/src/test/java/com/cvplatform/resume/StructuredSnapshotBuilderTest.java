package com.cvplatform.resume;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

import com.cvplatform.resume.application.StructuredContentMasker;
import com.cvplatform.resume.application.StructuredSnapshotBuilder;
import com.cvplatform.resume.domain.ResumeSection;
import com.cvplatform.resume.domain.SectionType;
import com.cvplatform.resume.infrastructure.ResumeSectionRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class StructuredSnapshotBuilderTest {

    @Mock
    private ResumeSectionRepository resumeSectionRepository;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private StructuredSnapshotBuilder builder;
    private final UUID resumeId = UUID.randomUUID();

    @BeforeEach
    void setUp() {
        builder = new StructuredSnapshotBuilder(resumeSectionRepository, new StructuredContentMasker(objectMapper), objectMapper);
    }

    private ResumeSection section(SectionType type, int position, String content) {
        return ResumeSection.builder()
                .id(UUID.randomUUID()).resumeId(resumeId).sectionType(type).title(type.name())
                .position(position).visible(true).contentJson(content)
                .createdAt(Instant.now()).updatedAt(Instant.now())
                .build();
    }

    @Test
    void onlyIncludesVisibleSectionsInPositionOrder() {
        when(resumeSectionRepository.findByResumeIdAndVisibleTrueOrderByPositionAsc(resumeId))
                .thenReturn(List.of(
                        section(SectionType.SUMMARY, 0, "{\"text\":\"hi\"}"),
                        section(SectionType.SKILLS, 1, "{\"skills\":[]}")));

        var sections = builder.buildVisibleSections(resumeId);

        assertThat(sections).hasSize(2);
        assertThat(sections.get(0).type()).isEqualTo("SUMMARY");
        assertThat(sections.get(1).type()).isEqualTo("SKILLS");
    }

    @Test
    void masksPersonalInfoContactFieldsInTheSnapshot() {
        String personalInfoJson = "{\"fullName\":\"Jane\",\"headline\":\"Eng\",\"email\":\"jane@example.com\","
                + "\"phone\":\"0123456789\",\"location\":\"Hanoi\",\"website\":null,"
                + "\"hidePhone\":true,\"hideEmail\":false,\"hideLocation\":false}";
        when(resumeSectionRepository.findByResumeIdAndVisibleTrueOrderByPositionAsc(resumeId))
                .thenReturn(List.of(section(SectionType.PERSONAL_INFO, 0, personalInfoJson)));

        var sections = builder.buildVisibleSections(resumeId);

        assertThat(sections.get(0).content().get("phone").isNull()).isTrue();
        assertThat(sections.get(0).content().get("email").asText()).isEqualTo("jane@example.com");
    }

    @Test
    void buildSnapshotJsonProducesParseableJson() {
        when(resumeSectionRepository.findByResumeIdAndVisibleTrueOrderByPositionAsc(resumeId))
                .thenReturn(List.of(section(SectionType.SUMMARY, 0, "{\"text\":\"hi\"}")));

        String json = builder.buildSnapshotJson(resumeId);

        assertThat(json).contains("SUMMARY").contains("hi");
    }
}
