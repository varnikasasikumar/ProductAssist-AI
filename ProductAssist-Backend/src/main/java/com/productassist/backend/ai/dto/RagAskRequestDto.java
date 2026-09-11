package com.productassist.backend.ai.dto;

public class RagAskRequestDto {
    private String query;
    private String model;
    private Integer top_k = 5;

    public RagAskRequestDto() {}

    public RagAskRequestDto(String query, String model, Integer top_k) {
        this.query = query;
        this.model = model;
        if (top_k != null) {
            this.top_k = top_k;
        }
    }

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }

    public Integer getTop_k() { return top_k; }
    public void setTop_k(Integer top_k) { this.top_k = top_k; }
}
