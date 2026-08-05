package com.cvplatform.analytics.application;

import com.cvplatform.analytics.api.dto.AnalyticsSummaryResponse;
import com.cvplatform.analytics.domain.DeviceType;
import com.cvplatform.analytics.domain.ResumeView;
import com.cvplatform.analytics.infrastructure.ResumeViewRepository;
import com.cvplatform.common.config.AppProperties;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class AnalyticsService {

    private final ResumeViewRepository resumeViewRepository;
    private final AppProperties appProperties;

    public AnalyticsService(ResumeViewRepository resumeViewRepository, AppProperties appProperties) {
        this.resumeViewRepository = resumeViewRepository;
        this.appProperties = appProperties;
    }

    /**
     * Collapses repeated requests from the same visitor within the
     * dedup window into a single page view. Callers are responsible for
     * deciding whether a view should be recorded at all (e.g. the resume
     * owner's own visits are filtered out before this is ever called).
     */
    public void recordView(UUID resumeId, String visitorHash, String referrerHost, DeviceType deviceType) {
        Instant windowStart = Instant.now().minus(appProperties.getAnalytics().getViewDedupWindow());
        boolean alreadyCountedRecently = resumeViewRepository
                .existsByResumeIdAndVisitorHashAndViewedAtAfter(resumeId, visitorHash, windowStart);
        if (alreadyCountedRecently) {
            return;
        }
        resumeViewRepository.save(ResumeView.builder()
                .resumeId(resumeId)
                .viewedAt(Instant.now())
                .visitorHash(visitorHash)
                .referrerHost(referrerHost)
                .deviceType(deviceType)
                .build());
    }

    @Transactional(readOnly = true)
    public long countTotalViews(UUID resumeId) {
        return resumeViewRepository.countByResumeId(resumeId);
    }

    @Transactional(readOnly = true)
    public AnalyticsSummaryResponse summary(UUID resumeId) {
        Instant now = Instant.now();
        long total = resumeViewRepository.countByResumeId(resumeId);
        long last7d = resumeViewRepository.countByResumeIdAndViewedAtAfter(resumeId, now.minus(7, ChronoUnit.DAYS));
        long last30d = resumeViewRepository.countByResumeIdAndViewedAtAfter(resumeId, now.minus(30, ChronoUnit.DAYS));
        Instant lastViewedAt = resumeViewRepository.findTop1ByResumeIdOrderByViewedAtDesc(resumeId).stream()
                .findFirst()
                .map(ResumeView::getViewedAt)
                .orElse(null);
        return new AnalyticsSummaryResponse(total, last7d, last30d, lastViewedAt);
    }
}
