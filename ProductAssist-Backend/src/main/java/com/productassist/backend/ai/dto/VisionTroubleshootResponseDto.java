package com.productassist.backend.ai.dto;

public class VisionTroubleshootResponseDto {
    private VisionAnalysisResponseDto vision_analysis;
    private TroubleshootingResponseDto troubleshooting_session;

    public VisionTroubleshootResponseDto() {}

    public VisionAnalysisResponseDto getVision_analysis() { return vision_analysis; }
    public void setVision_analysis(VisionAnalysisResponseDto vision_analysis) { this.vision_analysis = vision_analysis; }

    public TroubleshootingResponseDto getTroubleshooting_session() { return troubleshooting_session; }
    public void setTroubleshooting_session(TroubleshootingResponseDto troubleshooting_session) { this.troubleshooting_session = troubleshooting_session; }
}
