package com.cvplatform.analytics.infrastructure;

import com.cvplatform.analytics.domain.ResumeView;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ResumeViewRepository extends JpaRepository<ResumeView, Long> {

    long countByResumeId(UUID resumeId);

    long countByResumeIdAndViewedAtAfter(UUID resumeId, Instant since);

    boolean existsByResumeIdAndVisitorHashAndViewedAtAfter(UUID resumeId, String visitorHash, Instant since);

    List<ResumeView> findTop1ByResumeIdOrderByViewedAtDesc(UUID resumeId);
}
