package com.cvplatform.analytics;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.cvplatform.analytics.application.AnalyticsService;
import com.cvplatform.analytics.domain.DeviceType;
import com.cvplatform.analytics.domain.ResumeView;
import com.cvplatform.analytics.infrastructure.ResumeViewRepository;
import com.cvplatform.common.config.AppProperties;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class AnalyticsServiceTest {

    @Mock
    private ResumeViewRepository resumeViewRepository;

    private AnalyticsService analyticsService;
    private final UUID resumeId = UUID.randomUUID();

    @BeforeEach
    void setUp() {
        analyticsService = new AnalyticsService(resumeViewRepository, new AppProperties());
    }

    @Test
    void recordsANewViewWhenNoRecentViewFromTheSameVisitorExists() {
        when(resumeViewRepository.existsByResumeIdAndVisitorHashAndViewedAtAfter(eq(resumeId), anyString(), any(Instant.class)))
                .thenReturn(false);

        analyticsService.recordView(resumeId, "visitor-hash", "linkedin.com", DeviceType.DESKTOP);

        verify(resumeViewRepository, times(1)).save(any(ResumeView.class));
    }

    @Test
    void collapsesARepeatedViewFromTheSameVisitorWithinTheDedupWindow() {
        when(resumeViewRepository.existsByResumeIdAndVisitorHashAndViewedAtAfter(eq(resumeId), anyString(), any(Instant.class)))
                .thenReturn(true);

        analyticsService.recordView(resumeId, "visitor-hash", "linkedin.com", DeviceType.DESKTOP);

        verify(resumeViewRepository, never()).save(any(ResumeView.class));
    }

    @Test
    void summaryAggregatesCountsAndLastViewedAt() {
        Instant lastViewed = Instant.now();
        when(resumeViewRepository.countByResumeId(resumeId)).thenReturn(42L);
        when(resumeViewRepository.countByResumeIdAndViewedAtAfter(eq(resumeId), any(Instant.class))).thenReturn(5L);
        when(resumeViewRepository.findTop1ByResumeIdOrderByViewedAtDesc(resumeId))
                .thenReturn(List.of(ResumeView.builder().resumeId(resumeId).viewedAt(lastViewed).visitorHash("x").deviceType(DeviceType.DESKTOP).build()));

        var summary = analyticsService.summary(resumeId);

        assertThat(summary.totalViews()).isEqualTo(42L);
        assertThat(summary.views7d()).isEqualTo(5L);
        assertThat(summary.views30d()).isEqualTo(5L);
        assertThat(summary.lastViewedAt()).isEqualTo(lastViewed);
    }
}
