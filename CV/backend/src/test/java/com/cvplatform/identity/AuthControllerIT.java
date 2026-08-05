package com.cvplatform.identity;

import static org.hamcrest.Matchers.notNullValue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.cookie;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.cvplatform.support.AbstractIntegrationTest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

class AuthControllerIT extends AbstractIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void registerThenLoginSucceeds() throws Exception {
        String email = "jane.doe+%d@example.com".formatted(System.nanoTime());

        mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"%s","password":"correct-password-1","displayName":"Jane Doe"}
                                """.formatted(email)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accessToken", notNullValue()))
                .andExpect(jsonPath("$.user.email").value(email))
                .andExpect(cookie().exists("cv_refresh_token"))
                .andExpect(cookie().httpOnly("cv_refresh_token", true));

        mockMvc.perform(post("/api/v1/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"%s","password":"correct-password-1"}
                                """.formatted(email)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accessToken", notNullValue()));
    }

    @Test
    void registeringSameEmailTwiceReturnsConflict() throws Exception {
        String email = "dup+%d@example.com".formatted(System.nanoTime());
        String body = """
                {"email":"%s","password":"correct-password-1","displayName":"Dup User"}
                """.formatted(email);

        mockMvc.perform(post("/api/v1/auth/register").contentType(MediaType.APPLICATION_JSON).content(body))
                .andExpect(status().isOk());

        mockMvc.perform(post("/api/v1/auth/register").contentType(MediaType.APPLICATION_JSON).content(body))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.code").value("EMAIL_ALREADY_REGISTERED"))
                .andExpect(jsonPath("$.traceId", notNullValue()));
    }

    @Test
    void loginWithWrongPasswordReturnsUnauthorized() throws Exception {
        String email = "wrongpass+%d@example.com".formatted(System.nanoTime());
        mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"%s","password":"correct-password-1","displayName":"Someone"}
                                """.formatted(email)))
                .andExpect(status().isOk());

        mockMvc.perform(post("/api/v1/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"%s","password":"totally-wrong"}
                                """.formatted(email)))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("INVALID_CREDENTIALS"));
    }

    @Test
    void meWithoutTokenIsUnauthorized() throws Exception {
        mockMvc.perform(get("/api/v1/me"))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("NOT_AUTHENTICATED"));
    }

    @Test
    void meWithValidAccessTokenReturnsCurrentUser() throws Exception {
        String email = "me+%d@example.com".formatted(System.nanoTime());
        MvcResult registerResult = mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"%s","password":"correct-password-1","displayName":"Me User"}
                                """.formatted(email)))
                .andExpect(status().isOk())
                .andReturn();

        String accessToken = com.jayway.jsonpath.JsonPath.read(registerResult.getResponse().getContentAsString(), "$.accessToken");

        mockMvc.perform(get("/api/v1/me").header("Authorization", "Bearer " + accessToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value(email));
    }

    @Test
    void refreshRotatesCookieAndInvalidatesThePreviousOne() throws Exception {
        String email = "refresh+%d@example.com".formatted(System.nanoTime());
        MvcResult registerResult = mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"%s","password":"correct-password-1","displayName":"Refresh User"}
                                """.formatted(email)))
                .andExpect(status().isOk())
                .andReturn();

        jakarta.servlet.http.Cookie originalCookie = registerResult.getResponse().getCookie("cv_refresh_token");

        mockMvc.perform(post("/api/v1/auth/refresh").cookie(originalCookie))
                .andExpect(status().isOk())
                .andExpect(cookie().exists("cv_refresh_token"));

        // Replaying the now-rotated-out cookie must fail.
        mockMvc.perform(post("/api/v1/auth/refresh").cookie(originalCookie))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.code").value("INVALID_REFRESH_TOKEN"));
    }

    @Test
    void logoutRevokesRefreshTokenSoItCannotBeReused() throws Exception {
        String email = "logout+%d@example.com".formatted(System.nanoTime());
        MvcResult registerResult = mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"%s","password":"correct-password-1","displayName":"Logout User"}
                                """.formatted(email)))
                .andExpect(status().isOk())
                .andReturn();

        jakarta.servlet.http.Cookie refreshCookie = registerResult.getResponse().getCookie("cv_refresh_token");

        mockMvc.perform(post("/api/v1/auth/logout").cookie(refreshCookie))
                .andExpect(status().isNoContent());

        mockMvc.perform(post("/api/v1/auth/refresh").cookie(refreshCookie))
                .andExpect(status().isUnauthorized());
    }
}
