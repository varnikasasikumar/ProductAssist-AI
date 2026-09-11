package com.productassist.backend.ai.dto;

import java.util.List;

public class RagAskResponseDto {
    private String query;
    private String model;
    private String answer;
    private List<SourceCitationItemDto> sources;
    private int retrieved_chunks;

    public RagAskResponseDto() {}

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }

    public String getAnswer() { return answer; }
    public void setAnswer(String answer) { this.answer = answer; }

    public List<SourceCitationItemDto> getSources() { return sources; }
    public void setSources(List<SourceCitationItemDto> sources) { this.sources = sources; }

    public int getRetrieved_chunks() { return retrieved_chunks; }
    public void setRetrieved_chunks(int retrieved_chunks) { this.retrieved_chunks = retrieved_chunks; }
}
