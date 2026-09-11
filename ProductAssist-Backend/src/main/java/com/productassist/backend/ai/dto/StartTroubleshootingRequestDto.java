package com.productassist.backend.ai.dto;

public class StartTroubleshootingRequestDto {
    private String model;
    private String problem;

    public StartTroubleshootingRequestDto() {}

    public StartTroubleshootingRequestDto(String model, String problem) {
        this.model = model;
        this.problem = problem;
    }

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }

    public String getProblem() { return problem; }
    public void setProblem(String problem) { this.problem = problem; }
}
