package com.cvplatform.resume.application;

import com.cvplatform.resume.domain.SectionType;
import com.cvplatform.resume.domain.section.SectionContent;
import com.cvplatform.resume.domain.section.SectionContentType;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

/**
 * Content shape isn't enforced by a DB constraint (see docs/architecture.md's
 * JSONB-vs-relational note) - it's enforced here, once per section type,
 * before anything is persisted. Deserializing into the typed record and
 * re-serializing also normalizes the stored JSON (drops unknown fields,
 * applies the record's defaults).
 */
@Component
public class SectionContentValidator {

    private final ObjectMapper objectMapper;

    public SectionContentValidator(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public String validateAndNormalize(SectionType type, JsonNode content) {
        if (content == null || content.isNull()) {
            throw new InvalidSectionContentException("Section content is required");
        }
        Class<? extends SectionContent> targetType = SectionContentType.classFor(type);
        try {
            SectionContent parsed = objectMapper.treeToValue(content, targetType);
            return objectMapper.writeValueAsString(parsed);
        } catch (Exception e) {
            throw new InvalidSectionContentException("Content does not match the expected shape for " + type);
        }
    }
}
