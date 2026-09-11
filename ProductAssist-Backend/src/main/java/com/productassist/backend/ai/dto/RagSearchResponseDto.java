package com.productassist.backend.ai.dto;

import java.util.List;

public class RagSearchResponseDto {
    private String query;
    private String model;
    private int top_k;
    private int total_results;
    private List<RagSearchResultItemDto> results;

    public RagSearchResponseDto() {}

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }

    public int getTop_k() { return top_k; }
    public void setTop_k(int top_k) { this.top_k = top_k; }

    public int getTotal_results() { return total_results; }
    public void setTotal_results(int total_results) { this.total_results = total_results; }

    public List<RagSearchResultItemDto> getResults() { return results; }
    public void setResults(List<RagSearchResultItemDto> results) { this.results = results; }
}
