package com.cvplatform.resume.domain.section;

import java.util.List;

public record CertificationsContent(List<CertificationItem> items) implements SectionContent {

    public record CertificationItem(String name, String issuer, String issueDate, String credentialUrl) {
    }
}
