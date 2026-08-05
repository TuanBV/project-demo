package com.cvplatform.resume.api.dto;

import com.cvplatform.resume.domain.ResumeVisibility;
import jakarta.validation.constraints.Size;

/** PATCH semantics: a {@code null} field means "leave unchanged". */
public record UpdateResumeRequest(
        @Size(max = 150) String name,
        Boolean isDefault,
        ResumeVisibility visibility,
        Boolean allowDownload,
        Boolean searchEngineIndexable) {
}
