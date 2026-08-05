package com.cvplatform.resume;

import static org.assertj.core.api.Assertions.assertThat;

import com.cvplatform.resume.application.StructuredContentMasker;
import com.cvplatform.resume.domain.SectionType;
import com.cvplatform.resume.domain.section.PersonalInfoContent;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

class StructuredContentMaskerTest {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final StructuredContentMasker masker = new StructuredContentMasker(objectMapper);

    @Test
    void hidesOnlyTheFieldsTheOwnerMarkedHidden() throws Exception {
        var content = new PersonalInfoContent("Jane Doe", "Engineer", "jane@example.com", "0123456789", "Hanoi", "https://jane.dev",
                true, false, true); // hide phone + location, keep email
        String json = objectMapper.writeValueAsString(content);

        String masked = masker.maskForPublic(SectionType.PERSONAL_INFO, json);
        var result = objectMapper.readValue(masked, PersonalInfoContent.class);

        assertThat(result.phone()).isNull();
        assertThat(result.location()).isNull();
        assertThat(result.email()).isEqualTo("jane@example.com");
        assertThat(result.fullName()).isEqualTo("Jane Doe");
    }

    @Test
    void leavesNonPersonalInfoSectionsUnchanged() {
        String summaryJson = "{\"text\":\"hello\"}";

        String result = masker.maskForPublic(SectionType.SUMMARY, summaryJson);

        assertThat(result).isEqualTo(summaryJson);
    }
}
