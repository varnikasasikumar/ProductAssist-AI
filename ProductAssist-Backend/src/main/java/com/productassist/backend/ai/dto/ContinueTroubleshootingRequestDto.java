package com.productassist.backend.ai.dto;

public class ContinueTroubleshootingRequestDto {
    private String response;

    public ContinueTroubleshootingRequestDto() {}

    public ContinueTroubleshootingRequestDto(String response) {
        this.response = response;
    }

    public String getResponse() { return response; }
    public void setResponse(String response) { this.response = response; }
}
