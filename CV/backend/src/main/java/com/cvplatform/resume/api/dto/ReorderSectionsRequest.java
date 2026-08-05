package com.cvplatform.resume.api.dto;

import jakarta.validation.constraints.NotEmpty;
import java.util.List;
import java.util.UUID;

/** Must contain every section id belonging to the resume, exactly once, in the desired order. */
public record ReorderSectionsRequest(@NotEmpty List<UUID> sectionIds) {
}
