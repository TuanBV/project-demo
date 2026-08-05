package com.cvplatform.resume.application;

import com.cvplatform.resume.api.dto.CreateSectionRequest;
import com.cvplatform.resume.api.dto.UpdateSectionRequest;
import com.cvplatform.resume.domain.Resume;
import com.cvplatform.resume.domain.ResumeSection;
import com.cvplatform.resume.domain.ResumeType;
import com.cvplatform.resume.infrastructure.ResumeRepository;
import com.cvplatform.resume.infrastructure.ResumeSectionRepository;
import java.time.Instant;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class ResumeSectionService {

    private final ResumeRepository resumeRepository;
    private final ResumeSectionRepository resumeSectionRepository;
    private final SectionContentValidator sectionContentValidator;
    private final StructuredSnapshotBuilder structuredSnapshotBuilder;

    public ResumeSectionService(ResumeRepository resumeRepository,
                                 ResumeSectionRepository resumeSectionRepository,
                                 SectionContentValidator sectionContentValidator,
                                 StructuredSnapshotBuilder structuredSnapshotBuilder) {
        this.resumeRepository = resumeRepository;
        this.resumeSectionRepository = resumeSectionRepository;
        this.sectionContentValidator = sectionContentValidator;
        this.structuredSnapshotBuilder = structuredSnapshotBuilder;
    }

    @Transactional(readOnly = true)
    public List<ResumeSection> list(UUID resumeId, UUID ownerId) {
        requireStructuredResume(resumeId, ownerId);
        return resumeSectionRepository.findByResumeIdOrderByPositionAsc(resumeId);
    }

    public ResumeSection create(UUID resumeId, UUID ownerId, CreateSectionRequest request) {
        requireStructuredResume(resumeId, ownerId);

        boolean alreadyExists = resumeSectionRepository.findByResumeIdOrderByPositionAsc(resumeId).stream()
                .anyMatch(s -> s.getSectionType() == request.sectionType());
        if (alreadyExists) {
            throw new DuplicateSectionTypeException();
        }

        String normalizedContent = sectionContentValidator.validateAndNormalize(request.sectionType(), request.content());
        int nextPosition = resumeSectionRepository.findTopByResumeIdOrderByPositionDesc(resumeId)
                .map(s -> s.getPosition() + 1)
                .orElse(0);

        Instant now = Instant.now();
        return resumeSectionRepository.save(ResumeSection.builder()
                .resumeId(resumeId)
                .sectionType(request.sectionType())
                .title(request.title().trim())
                .position(nextPosition)
                .visible(true)
                .contentJson(normalizedContent)
                .createdAt(now)
                .updatedAt(now)
                .build());
    }

    public ResumeSection update(UUID resumeId, UUID ownerId, UUID sectionId, UpdateSectionRequest request) {
        requireStructuredResume(resumeId, ownerId);
        ResumeSection section = resumeSectionRepository.findByIdAndResumeId(sectionId, resumeId)
                .orElseThrow(ResumeSectionNotFoundException::new);

        if (request.title() != null && !request.title().isBlank()) {
            section.setTitle(request.title().trim());
        }
        if (request.content() != null) {
            section.setContentJson(sectionContentValidator.validateAndNormalize(section.getSectionType(), request.content()));
        }
        if (request.visible() != null) {
            section.setVisible(request.visible());
        }
        section.setUpdatedAt(Instant.now());
        return resumeSectionRepository.save(section);
    }

    public void delete(UUID resumeId, UUID ownerId, UUID sectionId) {
        requireStructuredResume(resumeId, ownerId);
        resumeSectionRepository.findByIdAndResumeId(sectionId, resumeId)
                .orElseThrow(ResumeSectionNotFoundException::new);
        resumeSectionRepository.deleteByIdAndResumeId(sectionId, resumeId);
    }

    public List<ResumeSection> reorder(UUID resumeId, UUID ownerId, List<UUID> orderedSectionIds) {
        requireStructuredResume(resumeId, ownerId);
        List<ResumeSection> current = resumeSectionRepository.findByResumeIdOrderByPositionAsc(resumeId);

        Set<UUID> currentIds = new HashSet<>();
        current.forEach(s -> currentIds.add(s.getId()));
        Set<UUID> requestedIds = new HashSet<>(orderedSectionIds);
        if (!currentIds.equals(requestedIds) || orderedSectionIds.size() != current.size()) {
            throw new InvalidSectionOrderException();
        }

        var byId = current.stream().collect(java.util.stream.Collectors.toMap(ResumeSection::getId, s -> s));
        for (int i = 0; i < orderedSectionIds.size(); i++) {
            ResumeSection section = byId.get(orderedSectionIds.get(i));
            section.setPosition(i);
            section.setUpdatedAt(Instant.now());
        }
        return resumeSectionRepository.saveAll(current);
    }

    @Transactional(readOnly = true)
    public List<StructuredSnapshotBuilder.SnapshotSection> preview(UUID resumeId, UUID ownerId) {
        requireStructuredResume(resumeId, ownerId);
        return structuredSnapshotBuilder.buildVisibleSections(resumeId);
    }

    private Resume requireStructuredResume(UUID resumeId, UUID ownerId) {
        Resume resume = resumeRepository.findByIdAndOwnerId(resumeId, ownerId).orElseThrow(ResumeNotFoundException::new);
        if (resume.getResumeType() != ResumeType.STRUCTURED) {
            throw new NotAStructuredResumeException();
        }
        return resume;
    }
}
