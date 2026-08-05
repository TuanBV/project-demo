package com.cvplatform.common.config;

import com.cvplatform.common.web.RequestCorrelationFilter;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;

/**
 * Registered as a plain servlet filter (outside the Spring Security chain)
 * with the highest possible precedence, so the correlation id is present
 * for literally every request - including ones Spring Security rejects
 * before they reach any of our own filters.
 */
@Configuration
public class RequestCorrelationFilterConfig {

    @Bean
    public FilterRegistrationBean<RequestCorrelationFilter> requestCorrelationFilter() {
        FilterRegistrationBean<RequestCorrelationFilter> registration = new FilterRegistrationBean<>(new RequestCorrelationFilter());
        registration.setOrder(Ordered.HIGHEST_PRECEDENCE);
        return registration;
    }
}
