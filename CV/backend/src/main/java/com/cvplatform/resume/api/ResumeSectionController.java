package com.cvplatform.resume.api;

import com.cvplatform.identity.security.CurrentUserProvider;
import com.cvplatform.resume.api.dto.CreateSectionRequest;
import com.cvplatform.resume.api.dto.ReorderSectionsRequest;
import com.cvplatform.resume.api.dto.ResumeSectionResponse;
import com.cvplatform.resume.api.dto.UpdateSectionRequest;
import com.cvplatform.resume.application.ResumeSectionService;
import com.cvplatform.resume.application.StructuredSnapshotBuilder;
import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/resumes/{resumeId}/sections")
public class ResumeSectionController {

    private final ResumeSectionService resumeSectionService;
    private final CurrentUserProvider currentUserProvider;

    public ResumeSectionController(ResumeSectionService resumeSectionService, CurrentUserProvider currentUserProvider) {
        this.resumeSectionService = resumeSectionService;
        this.currentUserProvider = currentUserProvider;
    }

    @GetMapping
    public List<ResumeSectionResponse> list(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        return resumeSectionService.list(resumeId, ownerId).stream().map(ResumeSectionResponse::from).toList();
    }

    @PostMapping
    public ResumeSectionResponse create(@PathVariable UUID resumeId, @Valid @RequestBody CreateSectionRequest request) {
        UUID ownerId = currentUserProvider.requireUserId();
        return ResumeSectionResponse.from(resumeSectionService.create(resumeId, ownerId, request));
    }

    @PatchMapping("/{sectionId}")
    public ResumeSectionResponse update(@PathVariable UUID resumeId, @PathVariable UUID sectionId,
                                         @Valid @RequestBody UpdateSectionRequest request) {
        UUID ownerId = currentUserProvider.requireUserId();
        return ResumeSectionResponse.from(resumeSectionService.update(resumeId, ownerId, sectionId, request));
    }

    @DeleteMapping("/{sectionId}")
    public ResponseEntity<Void> delete(@PathVariable UUID resumeId, @PathVariable UUID sectionId) {
        UUID ownerId = currentUserProvider.requireUserId();
        resumeSectionService.delete(resumeId, ownerId, sectionId);
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/order")
    public List<ResumeSectionResponse> reorder(@PathVariable UUID resumeId, @Valid @RequestBody ReorderSectionsRequest request) {
        UUID ownerId = currentUserProvider.requireUserId();
        return resumeSectionService.reorder(resumeId, ownerId, request.sectionIds()).stream()
                .map(ResumeSectionResponse::from)
                .toList();
    }

    /** Not in the original endpoint sketch - lets the owner preview exactly what publishing would produce right now. */
    @GetMapping("/preview")
    public List<StructuredSnapshotBuilder.SnapshotSection> preview(@PathVariable UUID resumeId) {
        UUID ownerId = currentUserProvider.requireUserId();
        return resumeSectionService.preview(resumeId, ownerId);
    }
}
