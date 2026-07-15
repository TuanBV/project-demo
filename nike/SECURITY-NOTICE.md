# Security Notice

The uploaded repository contained credentials and tokens in tracked files. This sanitized snapshot replaces the visible values, but the original `.git` history may still contain them.

Required actions before using or publishing the original repository:
1. Revoke and recreate the Gmail app password.
2. Revoke Facebook/Page access tokens.
3. Generate a new JWT secret with at least 32 random bytes.
4. Change database credentials.
5. Remove secrets from Git history with a reviewed `git filter-repo` procedure, then coordinate a force-push using `--force-with-lease` only after backups and team notification.
6. Store runtime secrets in local `.env`, CI secret storage, or a managed secret store—not in source control.

Never copy historical values back from Git commits, logs, notes, or chat transcripts.
