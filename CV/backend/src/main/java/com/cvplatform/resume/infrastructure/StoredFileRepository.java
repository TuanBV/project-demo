package com.cvplatform.resume.infrastructure;

import com.cvplatform.resume.domain.StoredFile;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StoredFileRepository extends JpaRepository<StoredFile, UUID> {
}
