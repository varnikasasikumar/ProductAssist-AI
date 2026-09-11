package com.productassist.backend.assistant.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class AssistantVisionAnalysisResponseDto {

    @JsonProperty("detected_product")
    private String detectedProduct;

    @JsonProperty("detected_model")
    private String detectedModel;

    @JsonProperty("detected_error_code")
    private String detectedErrorCode;

    @JsonProperty("visible_text")
    private List<String> visibleText;

    @JsonProperty("observed_issue")
    private String observedIssue;

    private double confidence;

    private String notes;

    public AssistantVisionAnalysisResponseDto() {}

    public AssistantVisionAnalysisResponseDto(String detectedProduct, String detectedModel, String detectedErrorCode,
                                             List<String> visibleText, String observedIssue, double confidence, String notes) {
        this.detectedProduct = detectedProduct;
        this.detectedModel = detectedModel;
        this.detectedErrorCode = detectedErrorCode;
        this.visibleText = visibleText;
        this.observedIssue = observedIssue;
        this.confidence = confidence;
        this.notes = notes;
    }

    public String getDetectedProduct() { return detectedProduct; }
    public void setDetectedProduct(String detectedProduct) { this.detectedProduct = detectedProduct; }

    public String getDetectedModel() { return detectedModel; }
    public void setDetectedModel(String detectedModel) { this.detectedModel = detectedModel; }

    public String getDetectedErrorCode() { return detectedErrorCode; }
    public void setDetectedErrorCode(String detectedErrorCode) { this.detectedErrorCode = detectedErrorCode; }

    public List<String> getVisibleText() { return visibleText; }
    public void setVisibleText(List<String> visibleText) { this.visibleText = visibleText; }

    public String getObservedIssue() { return observedIssue; }
    public void setObservedIssue(String observedIssue) { this.observedIssue = observedIssue; }

    public double getConfidence() { return confidence; }
    public void setConfidence(double confidence) { this.confidence = confidence; }

    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
}
