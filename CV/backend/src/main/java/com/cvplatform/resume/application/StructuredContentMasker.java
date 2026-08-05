package com.cvplatform.resume.application;

import com.cvplatform.resume.domain.SectionType;
import com.cvplatform.resume.domain.section.PersonalInfoContent;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

/**
 * Applies the owner's per-field visibility choices (currently just the
 * PERSONAL_INFO contact fields) before content is ever shown publicly.
 * Used both by the real publish snapshot and by the owner-facing preview,
 * so preview always matches what publishing would actually produce.
 */
@Component
public class StructuredContentMasker {

    private final ObjectMapper objectMapper;

    public StructuredContentMasker(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public String maskForPublic(SectionType type, String contentJson) {
        if (type != SectionType.PERSONAL_INFO) {
            return contentJson;
        }
        try {
            PersonalInfoContent content = objectMapper.readValue(contentJson, PersonalInfoContent.class);
            PersonalInfoContent masked = new PersonalInfoContent(
                    content.fullName(),
                    content.headline(),
                    content.hideEmail() ? null : content.email(),
                    content.hidePhone() ? null : content.phone(),
                    content.hideLocation() ? null : content.location(),
                    content.website(),
                    content.hidePhone(),
                    content.hideEmail(),
                    content.hideLocation());
            return objectMapper.writeValueAsString(masked);
        } catch (Exception e) {
            throw new InvalidSectionContentException("Stored PERSONAL_INFO content could not be re-parsed for masking");
        }
    }
}
