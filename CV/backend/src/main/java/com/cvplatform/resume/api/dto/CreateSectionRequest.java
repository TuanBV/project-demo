package com.cvplatform.resume.api.dto;

import com.cvplatform.resume.domain.SectionType;
import com.fasterxml.jackson.databind.JsonNode;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record CreateSectionRequest(
        @NotNull SectionType sectionType,
        @NotBlank @Size(max = 150) String title,
        @NotNull JsonNode content) {
}
