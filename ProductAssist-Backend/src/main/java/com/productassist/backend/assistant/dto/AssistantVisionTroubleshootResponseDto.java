package com.productassist.backend.assistant.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AssistantVisionTroubleshootResponseDto {

    @JsonProperty("vision_analysis")
    private AssistantVisionAnalysisResponseDto visionAnalysis;

    @JsonProperty("troubleshooting_session")
    private AssistantTroubleshootResponseDto troubleshootingSession;

    public AssistantVisionTroubleshootResponseDto() {}

    public AssistantVisionTroubleshootResponseDto(AssistantVisionAnalysisResponseDto visionAnalysis,
                                                 AssistantTroubleshootResponseDto troubleshootingSession) {
        this.visionAnalysis = visionAnalysis;
        this.troubleshootingSession = troubleshootingSession;
    }

    public AssistantVisionAnalysisResponseDto getVisionAnalysis() { return visionAnalysis; }
    public void setVisionAnalysis(AssistantVisionAnalysisResponseDto visionAnalysis) { this.visionAnalysis = visionAnalysis; }

    public AssistantTroubleshootResponseDto getTroubleshootingSession() { return troubleshootingSession; }
    public void setTroubleshootingSession(AssistantTroubleshootResponseDto troubleshootingSession) { this.troubleshootingSession = troubleshootingSession; }
}
