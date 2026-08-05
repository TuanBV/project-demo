package com.cvplatform.resume.domain.section;

import java.util.List;

public record LinksContent(List<LinkItem> items) implements SectionContent {

    public record LinkItem(String label, String url) {
    }
}
