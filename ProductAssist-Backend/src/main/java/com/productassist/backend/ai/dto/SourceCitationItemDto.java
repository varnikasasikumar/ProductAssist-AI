package com.productassist.backend.ai.dto;

public class SourceCitationItemDto {
    private String document_name;
    private String document_type;
    private int page_number;
    private String section;

    public SourceCitationItemDto() {}

    public String getDocument_name() { return document_name; }
    public void setDocument_name(String document_name) { this.document_name = document_name; }

    public String getDocument_type() { return document_type; }
    public void setDocument_type(String document_type) { this.document_type = document_type; }

    public int getPage_number() { return page_number; }
    public void setPage_number(int page_number) { this.page_number = page_number; }

    public String getSection() { return section; }
    public void setSection(String section) { this.section = section; }
}
