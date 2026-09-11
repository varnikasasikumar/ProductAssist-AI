package com.productassist.backend.ai.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

@Configuration
public class AiServiceConfig {

    @Value("${ai.service.base-url:http://127.0.0.1:8000}")
    private String baseUrl;

    @Value("${ai.service.connect-timeout:5000}")
    private int connectTimeout;

    @Value("${ai.service.read-timeout:30000}")
    private int readTimeout;

    @Bean
    public RestTemplate aiRestTemplate() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(connectTimeout);
        factory.setReadTimeout(readTimeout);
        return new RestTemplate(factory);
    }

    public String getBaseUrl() {
        return baseUrl;
    }
}
