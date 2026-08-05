package com.cvplatform.resume.application;

import com.cvplatform.resume.domain.ResumeSection;
import com.cvplatform.resume.infrastructure.ResumeSectionRepository;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Component;

/**
 * Builds the render-ready section list for a STRUCTURED resume: only
 * {@code visible} sections, in position order, with public-facing masking
 * already applied. Used for both the real publish snapshot
 * ({@code resume_versions.snapshot_json}) and the owner's "preview" -
 * the same code path guarantees preview never lies about what publishing
 * would actually produce.
 */
@Component
public class StructuredSnapshotBuilder {

    private final ResumeSectionRepository resumeSectionRepository;
    private final StructuredContentMasker structuredContentMasker;
    private final ObjectMapper objectMapper;

    public StructuredSnapshotBuilder(ResumeSectionRepository resumeSectionRepository,
                                      StructuredContentMasker structuredContentMasker,
                                      ObjectMapper objectMapper) {
        this.resumeSectionRepository = resumeSectionRepository;
        this.structuredContentMasker = structuredContentMasker;
        this.objectMapper = objectMapper;
    }

    public record SnapshotSection(String type, String title, int position, JsonNode content) {
    }

    public List<SnapshotSection> buildVisibleSections(UUID resumeId) {
        return resumeSectionRepository.findByResumeIdAndVisibleTrueOrderByPositionAsc(resumeId).stream()
                .map(this::toSnapshotSection)
                .toList();
    }

    public String buildSnapshotJson(UUID resumeId) {
        try {
            return objectMapper.writeValueAsString(buildVisibleSections(resumeId));
        } catch (Exception e) {
            throw new InvalidSectionContentException("Could not build a publish snapshot from the current sections");
        }
    }

    private SnapshotSection toSnapshotSection(ResumeSection section) {
        String masked = structuredContentMasker.maskForPublic(section.getSectionType(), section.getContentJson());
        try {
            JsonNode contentNode = objectMapper.readTree(masked);
            return new SnapshotSection(section.getSectionType().name(), section.getTitle(), section.getPosition(), contentNode);
        } catch (Exception e) {
            throw new InvalidSectionContentException("Stored section content is not valid JSON");
        }
    }
}
