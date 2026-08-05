package com.cvplatform.resume.application;

import com.cvplatform.common.config.AppProperties;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

/**
 * Defense in depth against a renamed/mislabeled upload: extension, declared
 * MIME type, and the actual PDF magic bytes must all agree. Relying on any
 * one of these alone is not enough - a browser-reported Content-Type is
 * fully attacker-controlled, and so is the filename.
 */
@Component
public class PdfFileValidator {

    private static final String PDF_MAGIC_BYTES = "%PDF-";
    private static final String PDF_CONTENT_TYPE = "application/pdf";

    private final AppProperties appProperties;

    public PdfFileValidator(AppProperties appProperties) {
        this.appProperties = appProperties;
    }

    public void validate(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new InvalidFileException("No file was uploaded");
        }
        if (file.getSize() > appProperties.getUpload().getMaxPdfSizeBytes()) {
            throw new InvalidFileException("File exceeds the maximum allowed size");
        }

        String filename = file.getOriginalFilename();
        if (filename == null || !filename.toLowerCase(Locale.ROOT).endsWith(".pdf")) {
            throw new InvalidFileException("Only .pdf files are accepted");
        }
        if (!PDF_CONTENT_TYPE.equals(file.getContentType())) {
            throw new InvalidFileException("File content type must be application/pdf");
        }

        byte[] content = readBytes(file);
        if (content.length < PDF_MAGIC_BYTES.length()
                || !new String(content, 0, PDF_MAGIC_BYTES.length(), StandardCharsets.US_ASCII).equals(PDF_MAGIC_BYTES)) {
            throw new InvalidFileException("File does not look like a valid PDF");
        }
    }

    private static byte[] readBytes(MultipartFile file) {
        try {
            return file.getBytes();
        } catch (Exception e) {
            throw new InvalidFileException("Could not read the uploaded file");
        }
    }
}
