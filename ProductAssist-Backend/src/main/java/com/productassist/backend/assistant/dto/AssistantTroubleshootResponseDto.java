package com.productassist.backend.assistant.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class AssistantTroubleshootResponseDto {

    @JsonProperty("session_id")
    private String sessionId;

    private String product;

    private String model;

    private String status;

    @JsonProperty("identified_issue")
    private String identifiedIssue;

    private String response;

    private String resolution;

    private List<SourceCitationDto> sources;

    public AssistantTroubleshootResponseDto() {}

    public AssistantTroubleshootResponseDto(String sessionId, String product, String model, String status,
                                            String identifiedIssue, String response, String resolution,
                                            List<SourceCitationDto> sources) {
        this.sessionId = sessionId;
        this.product = product;
        this.model = model;
        this.status = status;
        this.identifiedIssue = identifiedIssue;
        this.response = response;
        this.resolution = resolution;
        this.sources = sources;
    }

    public String getSessionId() { return sessionId; }
    public void setSessionId(String sessionId) { this.sessionId = sessionId; }

    public String getProduct() { return product; }
    public void setProduct(String product) { this.product = product; }

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getIdentifiedIssue() { return identifiedIssue; }
    public void setIdentifiedIssue(String identifiedIssue) { this.identifiedIssue = identifiedIssue; }

    public String getResponse() { return response; }
    public void setResponse(String response) { this.response = response; }

    public String getResolution() { return resolution; }
    public void setResolution(String resolution) { this.resolution = resolution; }

    public List<SourceCitationDto> getSources() { return sources; }
    public void setSources(List<SourceCitationDto> sources) { this.sources = sources; }
}
