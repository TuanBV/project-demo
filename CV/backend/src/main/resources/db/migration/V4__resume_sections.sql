-- Phase 4: structured (web) CV sections. Content shape varies per
-- section_type (personal info vs. a list of work-experience entries, etc.)
-- so it's stored as JSONB and validated at the application layer - see
-- docs/architecture.md's JSONB-vs-relational note (written in Phase 2,
-- applying now that this table actually exists).

CREATE TABLE resume_sections (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id     UUID NOT NULL REFERENCES resumes (id) ON DELETE CASCADE,
    section_type  VARCHAR(30)  NOT NULL,
    title         VARCHAR(150) NOT NULL,
    position      INTEGER      NOT NULL,
    visible       BOOLEAN      NOT NULL DEFAULT true,
    content_json  JSONB        NOT NULL,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT chk_resume_sections_type CHECK (section_type IN (
        'PERSONAL_INFO', 'SUMMARY', 'SKILLS', 'EXPERIENCE', 'PROJECTS',
        'EDUCATION', 'LANGUAGES', 'CERTIFICATIONS', 'LINKS', 'ADDITIONAL'
    ))
);

CREATE INDEX ix_resume_sections_resume_id ON resume_sections (resume_id);
-- One section per type per resume (e.g. a single "Experience" section that
-- holds a list of jobs, not several standalone "Experience" sections).
CREATE UNIQUE INDEX uk_resume_sections_resume_type ON resume_sections (resume_id, section_type);
CREATE UNIQUE INDEX uk_resume_sections_resume_position ON resume_sections (resume_id, position);
