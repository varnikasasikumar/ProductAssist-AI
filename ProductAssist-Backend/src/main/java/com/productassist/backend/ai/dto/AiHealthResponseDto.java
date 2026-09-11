package com.productassist.backend.ai.dto;

public class AiHealthResponseDto {
    private String status;
    private String service;
    private String version;
    private String message;

    public AiHealthResponseDto() {}

    public AiHealthResponseDto(String status, String service, String version, String message) {
        this.status = status;
        this.service = service;
        this.version = version;
        this.message = message;
    }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getService() { return service; }
    public void setService(String service) { this.service = service; }

    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
}
