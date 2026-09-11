package com.productassist.backend.ai.dto;

public class RagSearchResultItemDto {
    private String content;
    private String document_name;
    private String document_type;
    private int page_number;
    private String section;
    private String model;
    private String product;
    private Double score;
    private String source_file;

    public RagSearchResultItemDto() {}

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public String getDocument_name() { return document_name; }
    public void setDocument_name(String document_name) { this.document_name = document_name; }

    public String getDocument_type() { return document_type; }
    public void setDocument_type(String document_type) { this.document_type = document_type; }

    public int getPage_number() { return page_number; }
    public void setPage_number(int page_number) { this.page_number = page_number; }

    public String getSection() { return section; }
    public void setSection(String section) { this.section = section; }

    public String getModel() { return model; }
    public void setModel(String model) { this.model = model; }

    public String getProduct() { return product; }
    public void setProduct(String product) { this.product = product; }

    public Double getScore() { return score; }
    public void setScore(Double score) { this.score = score; }

    public String getSource_file() { return source_file; }
    public void setSource_file(String source_file) { this.source_file = source_file; }
}
