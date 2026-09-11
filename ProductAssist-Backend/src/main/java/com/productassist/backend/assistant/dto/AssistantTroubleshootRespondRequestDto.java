package com.productassist.backend.assistant.dto;

import jakarta.validation.constraints.NotBlank;

public class AssistantTroubleshootRespondRequestDto {

    @NotBlank(message = "Message must not be blank")
    private String message;

    public AssistantTroubleshootRespondRequestDto() {}

    public AssistantTroubleshootRespondRequestDto(String message) {
        this.message = message;
    }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
}
