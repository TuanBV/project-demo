package com.cvplatform.resume.domain.section;

import java.util.List;

public record SkillsContent(List<SkillItem> skills) implements SectionContent {

    public record SkillItem(String name, String level) {
    }
}
