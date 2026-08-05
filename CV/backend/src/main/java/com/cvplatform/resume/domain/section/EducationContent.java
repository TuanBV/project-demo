package com.cvplatform.resume.domain.section;

import java.util.List;

public record EducationContent(List<EducationItem> items) implements SectionContent {

    public record EducationItem(
            String school,
            String degree,
            String fieldOfStudy,
            String startDate,
            String endDate,
            String description) {
    }
}
