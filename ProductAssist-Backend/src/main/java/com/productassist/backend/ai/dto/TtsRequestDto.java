package com.productassist.backend.ai.dto;

public class TtsRequestDto {
    private String text;
    private String voice = "alloy";
    private String format = "wav";

    public TtsRequestDto() {}

    public TtsRequestDto(String text) {
        this.text = text;
    }

    public TtsRequestDto(String text, String voice, String format) {
        this.text = text;
        if (voice != null) this.voice = voice;
        if (format != null) this.format = format;
    }

    public String getText() { return text; }
    public void setText(String text) { this.text = text; }

    public String getVoice() { return voice; }
    public void setVoice(String voice) { this.voice = voice; }

    public String getFormat() { return format; }
    public void setFormat(String format) { this.format = format; }
}
