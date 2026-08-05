package com.cvplatform.analytics.api.dto;

import java.time.Instant;

public record AnalyticsSummaryResponse(long totalViews, long views7d, long views30d, Instant lastViewedAt) {
}
