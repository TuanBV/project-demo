package com.cvplatform.resume.application;

import com.cvplatform.resume.domain.Resume;

/**
 * {@code rawUnlistedToken} is non-null only immediately after a mutation
 * that generated a fresh unlisted share token (switching visibility to
 * UNLISTED, or an explicit regenerate) - see {@link com.cvplatform.resume.api.dto.ResumeResponse}.
 */
public record ResumeMutationResult(Resume resume, String rawUnlistedToken) {

    public static ResumeMutationResult withoutToken(Resume resume) {
        return new ResumeMutationResult(resume, null);
    }
}
