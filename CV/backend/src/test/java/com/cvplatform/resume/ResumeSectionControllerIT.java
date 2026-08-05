package com.cvplatform.resume;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.cvplatform.support.AbstractIntegrationTest;
import com.jayway.jsonpath.JsonPath;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

class ResumeSectionControllerIT extends AbstractIntegrationTest {

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

    private String createStructuredResume(String token) throws Exception {
        var result = mockMvc.perform(post("/api/v1/resumes")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"name":"Web CV","resumeType":"STRUCTURED"}
                                """))
                .andExpect(status().isOk())
                .andReturn();
        return JsonPath.read(result.getResponse().getContentAsString(), "$.id");
    }

    @Test
    void addingEditingAndReorderingSectionsWorks() throws Exception {
        String token = registerAndGetToken("sections+%d@example.com".formatted(System.nanoTime()));
        String resumeId = createStructuredResume(token);

        var summaryResult = mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/sections")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"sectionType":"SUMMARY","title":"Summary","content":{"text":"Hello world"}}
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.position").value(0))
                .andReturn();
        String summaryId = JsonPath.read(summaryResult.getResponse().getContentAsString(), "$.id");

        var skillsResult = mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/sections")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"sectionType":"SKILLS","title":"Skills","content":{"skills":[{"name":"Java","level":"EXPERT"}]}}
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.position").value(1))
                .andReturn();
        String skillsId = JsonPath.read(skillsResult.getResponse().getContentAsString(), "$.id");

        // Duplicate type rejected.
        mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/sections")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"sectionType":"SUMMARY","title":"Summary 2","content":{"text":"dup"}}
                                """))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.code").value("DUPLICATE_SECTION_TYPE"));

        // Invalid content shape rejected.
        mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/sections")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"sectionType":"EDUCATION","title":"Education","content":"not-an-object"}
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("INVALID_SECTION_CONTENT"));

        // Reorder: skills first, then summary.
        mockMvc.perform(put("/api/v1/resumes/" + resumeId + "/sections/order")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"sectionIds\":[\"%s\",\"%s\"]}".formatted(skillsId, summaryId)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(skillsId))
                .andExpect(jsonPath("$[1].id").value(summaryId));

        // Hide the summary section.
        mockMvc.perform(patch("/api/v1/resumes/" + resumeId + "/sections/" + summaryId)
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"visible":false}
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.visible").value(false));

        // Preview reflects only the visible section.
        mockMvc.perform(get("/api/v1/resumes/" + resumeId + "/sections/preview")
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].type").value("SKILLS"));

        // Cannot publish - need at least one visible section is satisfied (SKILLS is visible), so publish should succeed.
        mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/publish")
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("PUBLISHED"));

        mockMvc.perform(delete("/api/v1/resumes/" + resumeId + "/sections/" + skillsId)
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isNoContent());
    }

    @Test
    void cannotPublishAStructuredResumeWithNoVisibleSections() throws Exception {
        String token = registerAndGetToken("empty-structured+%d@example.com".formatted(System.nanoTime()));
        String resumeId = createStructuredResume(token);

        mockMvc.perform(post("/api/v1/resumes/" + resumeId + "/publish")
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.code").value("CANNOT_PUBLISH"));
    }

    @Test
    void sectionsDoNotApplyToPdfResumes() throws Exception {
        String token = registerAndGetToken("pdf-sections+%d@example.com".formatted(System.nanoTime()));
        var result = mockMvc.perform(post("/api/v1/resumes")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"name":"My CV","resumeType":"PDF"}
                                """))
                .andExpect(status().isOk())
                .andReturn();
        String resumeId = JsonPath.read(result.getResponse().getContentAsString(), "$.id");

        mockMvc.perform(get("/api/v1/resumes/" + resumeId + "/sections").header("Authorization", "Bearer " + token))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("NOT_A_STRUCTURED_RESUME"));
    }
}
