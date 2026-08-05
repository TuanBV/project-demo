package com.cvplatform.sharing;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
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

class PublicResumeControllerIT extends AbstractIntegrationTest {

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

    /** Creates a PDF resume, uploads a file, and publishes it as PUBLIC. Returns [resumeId, publicId, slug]. */
    private String[] createPublishedPublicResume(String token) throws Exception {
        var createResult = mockMvc.perform(post("/api/v1/resumes")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"name":"My CV","resumeType":"PDF"}
                                """))
                .andExpect(status().isOk())
                .andReturn();
        String resumeId = JsonPath.read(createResult.getResponse().getContentAsString(), "$.id");
        String slug = JsonPath.read(createResult.getResponse().getContentAsString(), "$.slug");

        var file = new MockMultipartFile("file", "resume.pdf", "application/pdf", "%PDF-1.4 body".getBytes());
        mockMvc.perform(multipart("/api/v1/resumes/" + resumeId + "/versions/pdf")
                        .file(file)
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk());

        mockMvc.perform(patch("/api/v1/resumes/" + resumeId)
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"visibility":"PUBLIC"}
                                """))
                .andExpect(status().isOk());

        var publishResult = mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/publish")
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andReturn();
        String publicId = JsonPath.read(publishResult.getResponse().getContentAsString(), "$.publicId");

        return new String[] { resumeId, publicId, slug };
    }

    @Test
    void publicResumeIsVisibleOnceItIsPublicAndPublished() throws Exception {
        String token = registerAndGetToken("public-ok+%d@example.com".formatted(System.nanoTime()));
        String[] ids = createPublishedPublicResume(token);

        mockMvc.perform(get("/api/v1/public/resumes/" + ids[1] + "/" + ids[2]))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.publicId").value(ids[1]));
    }

    @Test
    void draftResumeIsNotVisibleThroughThePublicEndpoint() throws Exception {
        String token = registerAndGetToken("draft-hidden+%d@example.com".formatted(System.nanoTime()));
        var createResult = mockMvc.perform(post("/api/v1/resumes")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"name":"Draft CV","resumeType":"PDF"}
                                """))
                .andExpect(status().isOk())
                .andReturn();
        String publicId = JsonPath.read(createResult.getResponse().getContentAsString(), "$.publicId");
        String slug = JsonPath.read(createResult.getResponse().getContentAsString(), "$.slug");

        mockMvc.perform(get("/api/v1/public/resumes/" + publicId + "/" + slug))
                .andExpect(status().isGone())
                .andExpect(jsonPath("$.code").value("RESUME_LINK_GONE"));
    }

    @Test
    void privateResumeIsNeverVisibleThroughThePublicEndpointEvenIfPublished() throws Exception {
        String token = registerAndGetToken("private-hidden+%d@example.com".formatted(System.nanoTime()));
        String[] ids = createPublishedPublicResume(token);
        String resumeId = ids[0];

        mockMvc.perform(patch("/api/v1/resumes/" + resumeId)
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"visibility":"PRIVATE"}
                                """))
                .andExpect(status().isOk());

        mockMvc.perform(get("/api/v1/public/resumes/" + ids[1] + "/" + ids[2]))
                .andExpect(status().isGone());
    }

    @Test
    void unknownPublicIdReturnsNotFound() throws Exception {
        mockMvc.perform(get("/api/v1/public/resumes/" + java.util.UUID.randomUUID() + "/whatever"))
                .andExpect(status().isNotFound());
    }

    @Test
    void unlistedResumeRequiresTheCorrectToken() throws Exception {
        String token = registerAndGetToken("unlisted+%d@example.com".formatted(System.nanoTime()));
        String[] ids = createPublishedPublicResume(token);
        String resumeId = ids[0];
        String publicId = ids[1];

        var patchResult = mockMvc.perform(patch("/api/v1/resumes/" + resumeId)
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"visibility":"UNLISTED"}
                                """))
                .andExpect(status().isOk())
                .andReturn();
        String rawToken = JsonPath.read(patchResult.getResponse().getContentAsString(), "$.unlistedShareToken");

        mockMvc.perform(get("/api/v1/public/resumes/" + publicId + "/wrong-token"))
                .andExpect(status().isNotFound());

        mockMvc.perform(get("/api/v1/public/resumes/" + publicId + "/" + rawToken))
                .andExpect(status().isOk());
    }

    @Test
    void downloadIsBlockedUnlessTheOwnerAllowedIt() throws Exception {
        String token = registerAndGetToken("download+%d@example.com".formatted(System.nanoTime()));
        String[] ids = createPublishedPublicResume(token);

        mockMvc.perform(get("/api/v1/public/resumes/" + ids[1] + "/" + ids[2] + "/file?download=true"))
                .andExpect(status().isForbidden());

        mockMvc.perform(get("/api/v1/public/resumes/" + ids[1] + "/" + ids[2] + "/file"))
                .andExpect(status().isOk());
    }

    @Test
    void ownerViewingTheirOwnPublicPageDoesNotIncrementViewCount() throws Exception {
        String token = registerAndGetToken("owner-view+%d@example.com".formatted(System.nanoTime()));
        String[] ids = createPublishedPublicResume(token);

        mockMvc.perform(post("/api/v1/public/resumes/" + ids[1] + "/" + ids[2] + "/view")
                        .header("Authorization", "Bearer " + token));

        mockMvc.perform(get("/api/v1/resumes/" + ids[0]).header("Authorization", "Bearer " + token))
                .andExpect(jsonPath("$.viewCount").value(0));
    }

    @Test
    void anonymousViewIncrementsViewCount() throws Exception {
        String token = registerAndGetToken("anon-view+%d@example.com".formatted(System.nanoTime()));
        String[] ids = createPublishedPublicResume(token);

        mockMvc.perform(post("/api/v1/public/resumes/" + ids[1] + "/" + ids[2] + "/view"));

        mockMvc.perform(get("/api/v1/resumes/" + ids[0]).header("Authorization", "Bearer " + token))
                .andExpect(jsonPath("$.viewCount").value(1));
    }

    @Test
    void publicPageForAStructuredResumeExposesOnlyVisibleMaskedSections() throws Exception {
        String token = registerAndGetToken("structured-public+%d@example.com".formatted(System.nanoTime()));

        var createResult = mockMvc.perform(post("/api/v1/resumes")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"name":"Web CV","resumeType":"STRUCTURED"}
                                """))
                .andExpect(status().isOk())
                .andReturn();
        String resumeId = JsonPath.read(createResult.getResponse().getContentAsString(), "$.id");

        mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/sections")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"sectionType":"PERSONAL_INFO","title":"Info","content":{
                                    "fullName":"Jane Doe","headline":"Engineer","email":"jane@example.com",
                                    "phone":"0123456789","location":"Hanoi","website":"https://jane.dev",
                                    "hidePhone":true,"hideEmail":false,"hideLocation":false}}
                                """))
                .andExpect(status().isOk());

        mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/sections")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"sectionType":"ADDITIONAL","title":"Hidden section","content":{"text":"secret"}}
                                """))
                .andReturn();
        String hiddenSectionId = JsonPath.read(
                mockMvc.perform(get("/api/v1/resumes/" + resumeId + "/sections").header("Authorization", "Bearer " + token))
                        .andReturn().getResponse().getContentAsString(),
                "$[1].id");
        mockMvc.perform(patch("/api/v1/resumes/" + resumeId + "/sections/" + hiddenSectionId)
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"visible":false}
                                """))
                .andExpect(status().isOk());

        mockMvc.perform(patch("/api/v1/resumes/" + resumeId)
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"visibility":"PUBLIC"}
                                """))
                .andExpect(status().isOk());
        var publishResult = mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/publish")
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andReturn();
        String publicId = JsonPath.read(publishResult.getResponse().getContentAsString(), "$.publicId");
        String slug = JsonPath.read(publishResult.getResponse().getContentAsString(), "$.slug");

        mockMvc.perform(get("/api/v1/public/resumes/" + publicId + "/" + slug))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.sections.length()").value(1))
                .andExpect(jsonPath("$.sections[0].type").value("PERSONAL_INFO"))
                .andExpect(jsonPath("$.sections[0].content.phone").value(org.hamcrest.Matchers.nullValue()))
                .andExpect(jsonPath("$.sections[0].content.email").value("jane@example.com"));
    }
}
