-- Phase 3: view analytics. `resumes.visibility` / `allow_download` /
-- `unlisted_token_hash` / `published_at` already exist from V2 - this phase
-- only adds the tracking table, plus the API/service logic that lights up
-- those already-modeled columns.

CREATE TABLE resume_views (
    id             BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    resume_id      UUID NOT NULL REFERENCES resumes (id) ON DELETE CASCADE,
    viewed_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    visitor_hash   VARCHAR(64) NOT NULL,
    referrer_host  VARCHAR(255),
    device_type    VARCHAR(20) NOT NULL
);

CREATE INDEX ix_resume_views_resume_id_viewed_at ON resume_views (resume_id, viewed_at);
-- Backs the "collapse repeated requests from the same visitor into one page view" dedup check.
CREATE INDEX ix_resume_views_dedup ON resume_views (resume_id, visitor_hash, viewed_at);
