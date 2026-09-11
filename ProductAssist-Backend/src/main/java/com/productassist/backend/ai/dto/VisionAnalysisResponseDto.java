package com.productassist.backend.ai.dto;

import java.util.List;

public class VisionAnalysisResponseDto {
    private String detected_product;
    private String detected_model;
    private String detected_error_code;
    private List<String> visible_text;
    private String observed_issue;
    private double confidence;
    private String notes;

    public VisionAnalysisResponseDto() {}

    public String getDetected_product() { return detected_product; }
    public void setDetected_product(String detected_product) { this.detected_product = detected_product; }

    public String getDetected_model() { return detected_model; }
    public void setDetected_model(String detected_model) { this.detected_model = detected_model; }

    public String getDetected_error_code() { return detected_error_code; }
    public void setDetected_error_code(String detected_error_code) { this.detected_error_code = detected_error_code; }

    public List<String> getVisible_text() { return visible_text; }
    public void setVisible_text(List<String> visible_text) { this.visible_text = visible_text; }

    public String getObserved_issue() { return observed_issue; }
    public void setObserved_issue(String observed_issue) { this.observed_issue = observed_issue; }

    public double getConfidence() { return confidence; }
    public void setConfidence(double confidence) { this.confidence = confidence; }

    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
}
