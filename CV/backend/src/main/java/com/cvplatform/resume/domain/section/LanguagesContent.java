package com.cvplatform.resume.domain.section;

import java.util.List;

public record LanguagesContent(List<LanguageItem> items) implements SectionContent {

    public record LanguageItem(String name, String proficiency) {
    }
}
