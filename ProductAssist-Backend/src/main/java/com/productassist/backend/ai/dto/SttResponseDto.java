package com.productassist.backend.ai.dto;

public class SttResponseDto {
    private String text;
    private String language;
    private double confidence;

    public SttResponseDto() {}

    public String getText() { return text; }
    public void setText(String text) { this.text = text; }

    public String getLanguage() { return language; }
    public void setLanguage(String language) { this.language = language; }

    public double getConfidence() { return confidence; }
    public void setConfidence(double confidence) { this.confidence = confidence; }
}
