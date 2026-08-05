package com.cvplatform.sharing.api;

import com.cvplatform.common.security.ClientIpResolver;
import com.cvplatform.identity.security.CurrentUserProvider;
import com.cvplatform.sharing.api.dto.PublicResumeResponse;
import com.cvplatform.sharing.application.PublicResumeService;
import jakarta.servlet.http.HttpServletRequest;
import java.util.UUID;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/public/resumes")
public class PublicResumeController {

    private final PublicResumeService publicResumeService;
    private final CurrentUserProvider currentUserProvider;

    public PublicResumeController(PublicResumeService publicResumeService, CurrentUserProvider currentUserProvider) {
        this.publicResumeService = publicResumeService;
        this.currentUserProvider = currentUserProvider;
    }

    @GetMapping("/{publicId}/{slugOrToken}")
    public PublicResumeResponse get(@PathVariable UUID publicId, @PathVariable String slugOrToken) {
        return publicResumeService.getPublicData(publicId, slugOrToken);
    }

    @GetMapping("/{publicId}/{slugOrToken}/file")
    public ResponseEntity<Resource> file(@PathVariable UUID publicId,
                                          @PathVariable String slugOrToken,
                                          @RequestParam(defaultValue = "false") boolean download) {
        Resource resource = publicResumeService.loadPublicFile(publicId, slugOrToken, download);
        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_PDF)
                .header(HttpHeaders.CONTENT_DISPOSITION, download ? "attachment" : "inline")
                .body(resource);
    }

    @PostMapping("/{publicId}/{slugOrToken}/view")
    public ResponseEntity<Void> recordView(@PathVariable UUID publicId,
                                            @PathVariable String slugOrToken,
                                            HttpServletRequest request) {
        publicResumeService.recordView(
                publicId,
                slugOrToken,
                ClientIpResolver.resolve(request),
                request.getHeader(HttpHeaders.USER_AGENT),
                request.getHeader(HttpHeaders.REFERER),
                currentUserProvider.optionalUserId());
        return ResponseEntity.accepted().build();
    }
}
