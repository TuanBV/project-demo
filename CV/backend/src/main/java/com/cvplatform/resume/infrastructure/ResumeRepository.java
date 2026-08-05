package com.cvplatform.resume.infrastructure;

import com.cvplatform.resume.domain.Resume;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ResumeRepository extends JpaRepository<Resume, UUID> {

    Optional<Resume> findByIdAndOwnerId(UUID id, UUID ownerId);

    List<Resume> findByOwnerIdAndDeletedAtIsNullOrderByUpdatedAtDesc(UUID ownerId);

    List<Resume> findByOwnerIdOrderByUpdatedAtDesc(UUID ownerId);

    Optional<Resume> findByOwnerIdAndIsDefaultTrueAndDeletedAtIsNull(UUID ownerId);

    Optional<Resume> findByPublicId(UUID publicId);
}
