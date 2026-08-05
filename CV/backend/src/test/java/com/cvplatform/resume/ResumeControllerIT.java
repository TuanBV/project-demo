package com.cvplatform.resume;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.cvplatform.support.AbstractIntegrationTest;
import com.jayway.jsonpath.JsonPath;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;

class ResumeControllerIT extends AbstractIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    private String registerAndGetToken(String email) throws Exception {
        var result = mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"%s","password":"correct-password-1","displayName":"Test User"}
                                """.formatted(email)))
                .andExpect(status().isOk())
                .andReturn();
        return JsonPath.read(result.getResponse().getContentAsString(), "$.accessToken");
    }

    private String createPdfResume(String token) throws Exception {
        var result = mockMvc.perform(post("/api/v1/resumes")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"name":"My CV","resumeType":"PDF"}
                                """))
                .andExpect(status().isOk())
                .andReturn();
        return JsonPath.read(result.getResponse().getContentAsString(), "$.id");
    }

    @Test
    void uploadingAPdfCreatesAnActiveVersionAndKeepsThePublicIdStable() throws Exception {
        String token = registerAndGetToken("resume-owner+%d@example.com".formatted(System.nanoTime()));
        String resumeId = createPdfResume(token);

        String publicIdBefore = JsonPath.read(
                mockMvc.perform(get("/api/v1/resumes/" + resumeId).header("Authorization", "Bearer " + token))
                        .andReturn().getResponse().getContentAsString(),
                "$.publicId");

        var file = new MockMultipartFile("file", "resume.pdf", "application/pdf", "%PDF-1.4 first version".getBytes());
        mockMvc.perform(multipart("/api/v1/resumes/" + resumeId + "/versions/pdf")
                        .file(file)
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.versionNumber").value(1))
                .andExpect(jsonPath("$.active").value(true));

        // Uploading a second version must not change the resume's public id.
        var secondFile = new MockMultipartFile("file", "resume-v2.pdf", "application/pdf", "%PDF-1.4 second version".getBytes());
        mockMvc.perform(multipart("/api/v1/resumes/" + resumeId + "/versions/pdf")
                        .file(secondFile)
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.versionNumber").value(2))
                .andExpect(jsonPath("$.active").value(true));

        mockMvc.perform(get("/api/v1/resumes/" + resumeId).header("Authorization", "Bearer " + token))
                .andExpect(jsonPath("$.publicId").value(publicIdBefore));

        mockMvc.perform(get("/api/v1/resumes/" + resumeId + "/versions").header("Authorization", "Bearer " + token))
                .andExpect(jsonPath("$.length()").value(2));
    }

    @Test
    void rejectsANonPdfUpload() throws Exception {
        String token = registerAndGetToken("bad-upload+%d@example.com".formatted(System.nanoTime()));
        String resumeId = createPdfResume(token);

        var file = new MockMultipartFile("file", "resume.txt", "text/plain", "not a pdf".getBytes());
        mockMvc.perform(multipart("/api/v1/resumes/" + resumeId + "/versions/pdf")
                        .file(file)
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("INVALID_FILE"));
    }

    @Test
    void cannotDeleteTheActiveVersionThroughTheApi() throws Exception {
        String token = registerAndGetToken("active-version+%d@example.com".formatted(System.nanoTime()));
        String resumeId = createPdfResume(token);

        var file = new MockMultipartFile("file", "resume.pdf", "application/pdf", "%PDF-1.4 body".getBytes());
        var uploadResult = mockMvc.perform(multipart("/api/v1/resumes/" + resumeId + "/versions/pdf")
                        .file(file)
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andReturn();
        String versionId = JsonPath.read(uploadResult.getResponse().getContentAsString(), "$.id");

        mockMvc.perform(delete("/api/v1/resumes/" + resumeId + "/versions/" + versionId)
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.code").value("CANNOT_DELETE_ACTIVE_VERSION"));
    }

    @Test
    void aUserCannotReadOrModifyAnotherUsersResume() throws Exception {
        String ownerToken = registerAndGetToken("owner+%d@example.com".formatted(System.nanoTime()));
        String otherToken = registerAndGetToken("intruder+%d@example.com".formatted(System.nanoTime()));
        String resumeId = createPdfResume(ownerToken);

        mockMvc.perform(get("/api/v1/resumes/" + resumeId).header("Authorization", "Bearer " + otherToken))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value("RESUME_NOT_FOUND"));

        mockMvc.perform(delete("/api/v1/resumes/" + resumeId).header("Authorization", "Bearer " + otherToken))
                .andExpect(status().isNotFound());
    }

    @Test
    void softDeleteThenRestoreBringsTheResumeBack() throws Exception {
        String token = registerAndGetToken("restore+%d@example.com".formatted(System.nanoTime()));
        String resumeId = createPdfResume(token);

        mockMvc.perform(delete("/api/v1/resumes/" + resumeId).header("Authorization", "Bearer " + token))
                .andExpect(status().isNoContent());

        mockMvc.perform(get("/api/v1/resumes").header("Authorization", "Bearer " + token))
                .andExpect(jsonPath("$.length()").value(0));

        mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/restore").header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.deletedAt").doesNotExist());

        mockMvc.perform(get("/api/v1/resumes").header("Authorization", "Bearer " + token))
                .andExpect(jsonPath("$.length()").value(1));
    }
}
