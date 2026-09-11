package com.productassist.backend.ai.dto;

import java.util.List;

public class TroubleshootingResponseDto {
    private String session_id;
    private String model;
    private String identified_issue;
    private String message;
    private String next_question;
    private String status;
    private String reasoning_summary;
    private List<TroubleshootingSourceItemDto> sources;

    public TroubleshootingResponseDto() {}

    public String getSession_id() { return session_id; }
    public void setSession_id(String session_id) { this.session_id = session_id; }

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }

    public String getIdentified_issue() { return identified_issue; }
    public void setIdentified_issue(String identified_issue) { this.identified_issue = identified_issue; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public String getNext_question() { return next_question; }
    public void setNext_question(String next_question) { this.next_question = next_question; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getReasoning_summary() { return reasoning_summary; }
    public void setReasoning_summary(String reasoning_summary) { this.reasoning_summary = reasoning_summary; }

    public List<TroubleshootingSourceItemDto> getSources() { return sources; }
    public void setSources(List<TroubleshootingSourceItemDto> sources) { this.sources = sources; }
}
