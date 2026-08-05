package com.cvplatform.resume.domain.section;

import java.util.List;

public record ExperienceContent(List<ExperienceItem> items) implements SectionContent {

    public record ExperienceItem(
            String company,
            String title,
            String startDate,
            String endDate,
            boolean current,
            String location,
            String description) {
    }
}
