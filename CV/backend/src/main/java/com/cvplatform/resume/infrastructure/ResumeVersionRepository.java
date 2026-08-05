package com.cvplatform.resume.infrastructure;

import com.cvplatform.resume.domain.ResumeVersion;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ResumeVersionRepository extends JpaRepository<ResumeVersion, UUID> {

    List<ResumeVersion> findByResumeIdOrderByVersionNumberDesc(UUID resumeId);

    Optional<ResumeVersion> findByIdAndResumeId(UUID id, UUID resumeId);

    Optional<ResumeVersion> findTopByResumeIdOrderByVersionNumberDesc(UUID resumeId);
}
