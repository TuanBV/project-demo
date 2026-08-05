package com.cvplatform.resume;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.cvplatform.resume.application.InvalidSectionContentException;
import com.cvplatform.resume.application.SectionContentValidator;
import com.cvplatform.resume.domain.SectionType;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

class SectionContentValidatorTest {

    // Mirrors Spring Boot's auto-configured ObjectMapper, which disables this
    // by default - the real SectionContentValidator bean runs with that same
    // relaxed setting, so the test would misrepresent production behaviour
    // (rejecting unknown fields instead of dropping them) without this.
    private final ObjectMapper objectMapper = new ObjectMapper()
            .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
    private final SectionContentValidator validator = new SectionContentValidator(objectMapper);

    @Test
    void acceptsValidSummaryContent() throws Exception {
        var node = objectMapper.readTree("""
                {"text": "Experienced backend engineer."}
                """);

        String normalized = validator.validateAndNormalize(SectionType.SUMMARY, node);

        assertThat(normalized).contains("Experienced backend engineer.");
    }

    @Test
    void dropsUnknownFieldsWhenNormalizing() throws Exception {
        var node = objectMapper.readTree("""
                {"text": "Hello", "unexpectedField": "should be dropped"}
                """);

        String normalized = validator.validateAndNormalize(SectionType.SUMMARY, node);

        assertThat(normalized).doesNotContain("unexpectedField");
    }

    @Test
    void rejectsContentThatDoesNotMatchTheSectionType() throws Exception {
        // SKILLS expects {"skills": [...]}, not a bare string.
        var node = objectMapper.readTree("""
                "just a string"
                """);

        assertThatThrownBy(() -> validator.validateAndNormalize(SectionType.SKILLS, node))
                .isInstanceOf(InvalidSectionContentException.class);
    }

    @Test
    void rejectsNullContent() {
        assertThatThrownBy(() -> validator.validateAndNormalize(SectionType.SUMMARY, null))
                .isInstanceOf(InvalidSectionContentException.class);
    }

    @Test
    void acceptsExperienceContentWithMultipleItems() throws Exception {
        var node = objectMapper.readTree("""
                {"items": [
                    {"company": "Acme", "title": "Engineer", "startDate": "2020-01", "endDate": null, "current": true, "location": "Remote", "description": "Built things"}
                ]}
                """);

        String normalized = validator.validateAndNormalize(SectionType.EXPERIENCE, node);

        assertThat(normalized).contains("Acme");
    }
}
