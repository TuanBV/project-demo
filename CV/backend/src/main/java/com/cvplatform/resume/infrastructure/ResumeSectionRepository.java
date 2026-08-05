package com.cvplatform.resume.infrastructure;

import com.cvplatform.resume.domain.ResumeSection;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ResumeSectionRepository extends JpaRepository<ResumeSection, UUID> {

    List<ResumeSection> findByResumeIdOrderByPositionAsc(UUID resumeId);

    List<ResumeSection> findByResumeIdAndVisibleTrueOrderByPositionAsc(UUID resumeId);

    Optional<ResumeSection> findByIdAndResumeId(UUID id, UUID resumeId);

    Optional<ResumeSection> findTopByResumeIdOrderByPositionDesc(UUID resumeId);

    void deleteByIdAndResumeId(UUID id, UUID resumeId);
}
