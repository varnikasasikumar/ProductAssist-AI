package com.productassist.backend.assistant.dto;

import java.util.List;

public class AssistantAskResponseDto {
    private String query;
    private String model;
    private String answer;
    private List<SourceCitationDto> sources;

    public AssistantAskResponseDto() {}

    public AssistantAskResponseDto(String query, String model, String answer, List<SourceCitationDto> sources) {
        this.query = query;
        this.model = model;
        this.answer = answer;
        this.sources = sources;
    }

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }

    public String getAnswer() { return answer; }
    public void setAnswer(String answer) { this.answer = answer; }

    public List<SourceCitationDto> getSources() { return sources; }
    public void setSources(List<SourceCitationDto> sources) { this.sources = sources; }
}
