package com.productassist.backend.assistant.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.productassist.backend.ai.dto.SttResponseDto;

public class AssistantVoiceTroubleshootResponseDto {

    @JsonProperty("transcription")
    private SttResponseDto transcription;

    @JsonProperty("troubleshooting_session")
    private AssistantTroubleshootResponseDto troubleshootingSession;

    public AssistantVoiceTroubleshootResponseDto() {}

    public AssistantVoiceTroubleshootResponseDto(SttResponseDto transcription,
                                                 AssistantTroubleshootResponseDto troubleshootingSession) {
        this.transcription = transcription;
        this.troubleshootingSession = troubleshootingSession;
    }

    public SttResponseDto getTranscription() { return transcription; }
    public void setTranscription(SttResponseDto transcription) { this.transcription = transcription; }

    public AssistantTroubleshootResponseDto getTroubleshootingSession() { return troubleshootingSession; }
    public void setTroubleshootingSession(AssistantTroubleshootResponseDto troubleshootingSession) { this.troubleshootingSession = troubleshootingSession; }
}
