package com.productassist.backend.assistant.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SourceCitationDto {

    @JsonProperty("document_name")
    private String documentName;

    @JsonProperty("document_type")
    private String documentType;

    @JsonProperty("page_number")
    private int pageNumber;

    private String section;

    public SourceCitationDto() {}

    public SourceCitationDto(String documentName, String documentType, int pageNumber, String section) {
        this.documentName = documentName;
        this.documentType = documentType;
        this.pageNumber = pageNumber;
        this.section = section;
    }

    public String getDocumentName() { return documentName; }
    public void setDocumentName(String documentName) { this.documentName = documentName; }

    public String getDocumentType() { return documentType; }
    public void setDocumentType(String documentType) { this.documentType = documentType; }

    public int getPageNumber() { return pageNumber; }
    public void setPageNumber(int pageNumber) { this.pageNumber = pageNumber; }

    public String getSection() { return section; }
    public void setSection(String section) { this.section = section; }
}
