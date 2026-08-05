package com.cvplatform.analytics.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * One row per de-duplicated page view. Never stores a raw IP - only
 * {@code visitorHash}, a salted hash computed from IP + User-Agent (see
 * {@link com.cvplatform.analytics.application.VisitorHasher}).
 */
@Entity
@Table(name = "resume_views")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ResumeView {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "resume_id", nullable = false)
    private UUID resumeId;

    @Column(name = "viewed_at", nullable = false)
    private Instant viewedAt;

    @Column(name = "visitor_hash", nullable = false)
    private String visitorHash;

    @Column(name = "referrer_host")
    private String referrerHost;

    @Enumerated(EnumType.STRING)
    @Column(name = "device_type", nullable = false)
    private DeviceType deviceType;
}
