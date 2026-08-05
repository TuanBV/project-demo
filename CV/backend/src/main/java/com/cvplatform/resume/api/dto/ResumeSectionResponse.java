package com.cvplatform.resume.api.dto;

import com.cvplatform.resume.domain.ResumeSection;
import com.fasterxml.jackson.annotation.JsonRawValue;
import java.util.UUID;

public record ResumeSectionResponse(
        UUID id,
        String sectionType,
        String title,
        int position,
        boolean visible,
        @JsonRawValue String content) {

    public static ResumeSectionResponse from(ResumeSection section) {
        return new ResumeSectionResponse(
                section.getId(),
                section.getSectionType().name(),
                section.getTitle(),
                section.getPosition(),
                section.isVisible(),
                section.getContentJson());
    }
}
