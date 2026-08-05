package com.cvplatform.resume;

import static org.assertj.core.api.Assertions.assertThatCode;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.cvplatform.common.config.AppProperties;
import com.cvplatform.resume.application.InvalidFileException;
import com.cvplatform.resume.application.PdfFileValidator;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockMultipartFile;

class PdfFileValidatorTest {

    private final PdfFileValidator validator = new PdfFileValidator(new AppProperties());

    private static byte[] validPdfBytes() {
        return ("%PDF-1.7\n%%EOF").getBytes(StandardCharsets.US_ASCII);
    }

    @Test
    void acceptsAValidPdf() {
        var file = new MockMultipartFile("file", "resume.pdf", "application/pdf", validPdfBytes());

        assertThatCode(() -> validator.validate(file)).doesNotThrowAnyException();
    }

    @Test
    void rejectsNonPdfExtension() {
        var file = new MockMultipartFile("file", "resume.docx", "application/pdf", validPdfBytes());

        assertThatThrownBy(() -> validator.validate(file)).isInstanceOf(InvalidFileException.class);
    }

    @Test
    void rejectsWrongDeclaredContentType() {
        var file = new MockMultipartFile("file", "resume.pdf", "application/octet-stream", validPdfBytes());

        assertThatThrownBy(() -> validator.validate(file)).isInstanceOf(InvalidFileException.class);
    }

    @Test
    void rejectsFileWithoutPdfMagicBytes() {
        // Renamed .pdf with the right declared content type, but not actually a PDF.
        var file = new MockMultipartFile("file", "resume.pdf", "application/pdf", "not a real pdf".getBytes(StandardCharsets.US_ASCII));

        assertThatThrownBy(() -> validator.validate(file)).isInstanceOf(InvalidFileException.class);
    }

    @Test
    void rejectsFileLargerThanConfiguredLimit() {
        AppProperties props = new AppProperties();
        props.getUpload().setMaxPdfSizeBytes(10);
        PdfFileValidator strictValidator = new PdfFileValidator(props);
        var file = new MockMultipartFile("file", "resume.pdf", "application/pdf", validPdfBytes());

        assertThatThrownBy(() -> strictValidator.validate(file)).isInstanceOf(InvalidFileException.class);
    }

    @Test
    void rejectsEmptyFile() {
        var file = new MockMultipartFile("file", "resume.pdf", "application/pdf", new byte[0]);

        assertThatThrownBy(() -> validator.validate(file)).isInstanceOf(InvalidFileException.class);
    }
}
