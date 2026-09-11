package com.productassist.backend.ai.dto;

public class VoiceTroubleshootResponseDto {
    private SttResponseDto transcription;
    private TroubleshootingResponseDto troubleshooting_session;

    public VoiceTroubleshootResponseDto() {}

    public SttResponseDto getTranscription() { return transcription; }
    public void setTranscription(SttResponseDto transcription) { this.transcription = transcription; }

    public TroubleshootingResponseDto getTroubleshooting_session() { return troubleshooting_session; }
    public void setTroubleshooting_session(TroubleshootingResponseDto troubleshooting_session) { this.troubleshooting_session = troubleshooting_session; }
}
