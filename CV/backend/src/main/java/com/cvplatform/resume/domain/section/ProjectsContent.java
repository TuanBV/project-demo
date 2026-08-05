package com.cvplatform.resume.domain.section;

import java.util.List;

public record ProjectsContent(List<ProjectItem> items) implements SectionContent {

    public record ProjectItem(
            String name,
            String description,
            String url,
            List<String> technologies,
            String startDate,
            String endDate) {
    }
}
