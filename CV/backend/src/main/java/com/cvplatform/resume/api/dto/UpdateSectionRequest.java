package com.cvplatform.resume.api.dto;

import com.fasterxml.jackson.databind.JsonNode;
import jakarta.validation.constraints.Size;

/** PATCH semantics: a {@code null} field means "leave unchanged". */
public record UpdateSectionRequest(
        @Size(max = 150) String title,
        JsonNode content,
        Boolean visible) {
}
