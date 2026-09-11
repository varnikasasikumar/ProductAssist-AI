package com.productassist.backend.assistant.dto;

import jakarta.validation.constraints.NotBlank;

public class AssistantTroubleshootStartRequestDto {

    @NotBlank(message = "Product must not be blank")
    private String product;

    @NotBlank(message = "Model must not be blank")
    private String model;

    @NotBlank(message = "Problem must not be blank")
    private String problem;

    public AssistantTroubleshootStartRequestDto() {}

    public AssistantTroubleshootStartRequestDto(String product, String model, String problem) {
        this.product = product;
        this.model = model;
        this.problem = problem;
    }

    public String getProduct() { return product; }
    public void setProduct(String product) { this.product = product; }

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }

    public String getProblem() { return problem; }
    public void setProblem(String problem) { this.problem = problem; }
}
