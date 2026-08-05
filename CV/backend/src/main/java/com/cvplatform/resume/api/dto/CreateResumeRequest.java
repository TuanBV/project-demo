package com.cvplatform.resume.api.dto;

import com.cvplatform.resume.domain.ResumeType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record CreateResumeRequest(
        @NotBlank @Size(max = 150) String name,
        @NotNull ResumeType resumeType) {
}
