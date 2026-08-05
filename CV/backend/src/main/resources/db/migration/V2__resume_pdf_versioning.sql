-- Phase 2: resume CRUD, PDF upload & versioning, storage metadata.
--
-- The `resumes` table is created with its full target shape from the
-- product ERD (including visibility/allow_download/search_engine_indexable/
-- published_at, which the sharing module doesn't expose via API until
-- Phase 3) rather than being split across two ALTER migrations - it's one
-- aggregate root, so we model it once and let later phases light up
-- behavior on columns that already exist. `resume_sections` (Phase 4) and
-- `resume_views` (Phase 3) stay separate tables added in their own phase's
-- migration, since those are genuinely new features, not new columns on
-- an existing one.

CREATE TABLE stored_files (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id           UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    storage_provider   VARCHAR(20)  NOT NULL,
    storage_key        VARCHAR(512) NOT NULL,
    original_filename  VARCHAR(255) NOT NULL,
    content_type       VARCHAR(100) NOT NULL,
    size_bytes         BIGINT       NOT NULL,
    checksum           VARCHAR(64)  NOT NULL,
    created_at         TIMESTAMPTZ  NOT NULL DEFAULT now(),
    deleted_at         TIMESTAMPTZ
);

CREATE UNIQUE INDEX uk_stored_files_storage_key ON stored_files (storage_key);
CREATE INDEX ix_stored_files_owner_id ON stored_files (owner_id);
CREATE INDEX ix_stored_files_checksum ON stored_files (checksum);

CREATE TABLE resumes (
    id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id                  UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    public_id                 UUID NOT NULL DEFAULT gen_random_uuid(),
    name                      VARCHAR(150) NOT NULL,
    slug                      VARCHAR(180) NOT NULL,
    resume_type               VARCHAR(20)  NOT NULL,
    status                    VARCHAR(20)  NOT NULL DEFAULT 'DRAFT',
    visibility                VARCHAR(20)  NOT NULL DEFAULT 'PRIVATE',
    unlisted_token_hash       VARCHAR(255),
    allow_download            BOOLEAN      NOT NULL DEFAULT false,
    search_engine_indexable   BOOLEAN      NOT NULL DEFAULT false,
    is_default                BOOLEAN      NOT NULL DEFAULT false,
    active_version_id         UUID,
    published_at              TIMESTAMPTZ,
    created_at                TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at                TIMESTAMPTZ  NOT NULL DEFAULT now(),
    deleted_at                TIMESTAMPTZ,
    version                   BIGINT       NOT NULL DEFAULT 0,
    CONSTRAINT chk_resumes_resume_type CHECK (resume_type IN ('PDF', 'STRUCTURED')),
    CONSTRAINT chk_resumes_status CHECK (status IN ('DRAFT', 'PUBLISHED', 'ARCHIVED')),
    CONSTRAINT chk_resumes_visibility CHECK (visibility IN ('PRIVATE', 'UNLISTED', 'PUBLIC'))
);

CREATE UNIQUE INDEX uk_resumes_public_id ON resumes (public_id);
CREATE INDEX ix_resumes_owner_id ON resumes (owner_id);
CREATE INDEX ix_resumes_status ON resumes (status);
CREATE INDEX ix_resumes_deleted_at ON resumes (deleted_at);
-- Only one non-deleted default resume per owner.
CREATE UNIQUE INDEX uk_resumes_owner_default ON resumes (owner_id) WHERE is_default AND deleted_at IS NULL;

CREATE TABLE resume_versions (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id        UUID NOT NULL REFERENCES resumes (id) ON DELETE CASCADE,
    version_number   INTEGER      NOT NULL,
    source_type      VARCHAR(30)  NOT NULL,
    file_id          UUID REFERENCES stored_files (id),
    snapshot_json    JSONB,
    created_by       UUID NOT NULL REFERENCES users (id),
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT chk_resume_versions_source_type CHECK (source_type IN ('PDF', 'STRUCTURED_SNAPSHOT'))
);

CREATE UNIQUE INDEX uk_resume_versions_resume_number ON resume_versions (resume_id, version_number);
CREATE INDEX ix_resume_versions_resume_id ON resume_versions (resume_id);

ALTER TABLE resumes
    ADD CONSTRAINT fk_resumes_active_version FOREIGN KEY (active_version_id) REFERENCES resume_versions (id);
