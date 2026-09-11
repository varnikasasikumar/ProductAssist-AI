package com.productassist.backend.assistant.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public class AssistantAskRequestDto {

    @NotBlank(message = "Query must not be blank")
    private String query;

    private String model;

    @Min(value = 1, message = "top_k must be at least 1")
    @Max(value = 10, message = "top_k must be at most 10")
    private Integer top_k = 5;

    public AssistantAskRequestDto() {}

    public AssistantAskRequestDto(String query, String model, Integer top_k) {
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
