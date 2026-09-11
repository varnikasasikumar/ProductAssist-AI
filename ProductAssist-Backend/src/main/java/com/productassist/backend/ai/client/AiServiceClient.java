package com.productassist.backend.ai.client;

import com.productassist.backend.ai.config.AiServiceConfig;
import com.productassist.backend.ai.dto.*;
import com.productassist.backend.ai.exception.AiServiceException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;
    private final AiServiceConfig aiServiceConfig;

    @Autowired
    public AiServiceClient(RestTemplate aiRestTemplate, AiServiceConfig aiServiceConfig) {
        this.restTemplate = aiRestTemplate;
        this.aiServiceConfig = aiServiceConfig;
    }

    private String getBaseUrl() {
        return aiServiceConfig.getBaseUrl();
    }

    // Health Endpoint
    public AiHealthResponseDto getHealth() {
        String url = getBaseUrl() + "/health";
        return executeGet(url, AiHealthResponseDto.class);
    }

    // RAG Endpoints
    public RagSearchResponseDto searchRag(RagSearchRequestDto request) {
        String url = getBaseUrl() + "/rag/search";
        return executePost(url, request, RagSearchResponseDto.class);
    }

    public RagAskResponseDto askRag(RagAskRequestDto request) {
        String url = getBaseUrl() + "/rag/ask";
        return executePost(url, request, RagAskResponseDto.class);
    }

    // Agentic Troubleshooting Endpoints
    public TroubleshootingResponseDto startTroubleshooting(StartTroubleshootingRequestDto request) {
        String url = getBaseUrl() + "/troubleshoot/start";
        return executePost(url, request, TroubleshootingResponseDto.class);
    }

    public TroubleshootingResponseDto continueTroubleshooting(String sessionId, ContinueTroubleshootingRequestDto request) {
        String url = getBaseUrl() + "/troubleshoot/" + sessionId + "/respond";
        return executePost(url, request, TroubleshootingResponseDto.class);
    }

    public TroubleshootingResponseDto getTroubleshootingSession(String sessionId) {
        String url = getBaseUrl() + "/troubleshoot/" + sessionId;
        return executeGet(url, TroubleshootingResponseDto.class);
    }

    // Multimodal Vision Endpoints
    public VisionAnalysisResponseDto analyzeVision(MultipartFile file) {
        String url = getBaseUrl() + "/vision/analyze";
        return executeMultipartPost(url, file, VisionAnalysisResponseDto.class);
    }

    public VisionTroubleshootResponseDto startTroubleshootingWithImage(MultipartFile file) {
        String url = getBaseUrl() + "/troubleshoot/start-with-image";
        return executeMultipartPost(url, file, VisionTroubleshootResponseDto.class);
    }

    // Voice Interaction Endpoints
    public SttResponseDto transcribeVoice(MultipartFile file) {
        String url = getBaseUrl() + "/voice/transcribe";
        return executeMultipartPost(url, file, SttResponseDto.class);
    }

    public byte[] synthesizeVoice(TtsRequestDto request) {
        String url = getBaseUrl() + "/voice/synthesize";
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<TtsRequestDto> entity = new HttpEntity<>(request, headers);
        
        try {
            ResponseEntity<byte[]> response = restTemplate.exchange(url, HttpMethod.POST, entity, byte[].class);
            return response.getBody();
        } catch (HttpClientErrorException ex) {
            throw new AiServiceException(ex.getResponseBodyAsString(), ex.getStatusCode().value(), ex);
        } catch (HttpServerErrorException ex) {
            throw new AiServiceException(ex.getResponseBodyAsString(), ex.getStatusCode().value(), ex);
        } catch (ResourceAccessException ex) {
            throw new AiServiceException("Python AI Service is unavailable at " + getBaseUrl(), 503, ex);
        } catch (RestClientException ex) {
            throw new AiServiceException("Failed to communicate with Python AI Service: " + ex.getMessage(), 500, ex);
        }
    }

    public VoiceTroubleshootResponseDto startTroubleshootingWithVoice(MultipartFile file) {
        String url = getBaseUrl() + "/troubleshoot/start-with-voice";
        return executeMultipartPost(url, file, VoiceTroubleshootResponseDto.class);
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> respondToTroubleshootingWithVoice(String sessionId, MultipartFile file) {
        String url = getBaseUrl() + "/troubleshoot/" + sessionId + "/respond-with-voice";
        return executeMultipartPost(url, file, Map.class);
    }

    // Helper Methods
    private <T> T executeGet(String url, Class<T> responseType) {
        try {
            return restTemplate.getForObject(url, responseType);
        } catch (HttpClientErrorException ex) {
            throw new AiServiceException(ex.getResponseBodyAsString(), ex.getStatusCode().value(), ex);
        } catch (HttpServerErrorException ex) {
            throw new AiServiceException(ex.getResponseBodyAsString(), ex.getStatusCode().value(), ex);
        } catch (ResourceAccessException ex) {
            throw new AiServiceException("Python AI Service is unavailable at " + getBaseUrl(), 503, ex);
        } catch (RestClientException ex) {
            throw new AiServiceException("Failed to communicate with Python AI Service: " + ex.getMessage(), 500, ex);
        }
    }

    private <T> T executePost(String url, Object requestPayload, Class<T> responseType) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Object> entity = new HttpEntity<>(requestPayload, headers);

        try {
            return restTemplate.postForObject(url, entity, responseType);
        } catch (HttpClientErrorException ex) {
            throw new AiServiceException(ex.getResponseBodyAsString(), ex.getStatusCode().value(), ex);
        } catch (HttpServerErrorException ex) {
            throw new AiServiceException(ex.getResponseBodyAsString(), ex.getStatusCode().value(), ex);
        } catch (ResourceAccessException ex) {
            throw new AiServiceException("Python AI Service is unavailable at " + getBaseUrl(), 503, ex);
        } catch (RestClientException ex) {
            throw new AiServiceException("Failed to communicate with Python AI Service: " + ex.getMessage(), 500, ex);
        }
    }

    private <T> T executeMultipartPost(String url, MultipartFile file, Class<T> responseType) {
        if (file == null || file.isEmpty()) {
            throw new AiServiceException("Uploaded file is missing or empty.", 400);
        }

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        try {
            ByteArrayResource fileResource = new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename() != null ? file.getOriginalFilename() : "upload.file";
                }
            };
            body.add("file", fileResource);
        } catch (IOException e) {
            throw new AiServiceException("Failed to read uploaded file contents: " + e.getMessage(), 400, e);
        }

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        try {
            return restTemplate.postForObject(url, requestEntity, responseType);
        } catch (HttpClientErrorException ex) {
            throw new AiServiceException(ex.getResponseBodyAsString(), ex.getStatusCode().value(), ex);
        } catch (HttpServerErrorException ex) {
            throw new AiServiceException(ex.getResponseBodyAsString(), ex.getStatusCode().value(), ex);
        } catch (ResourceAccessException ex) {
            throw new AiServiceException("Python AI Service is unavailable at " + getBaseUrl(), 503, ex);
        } catch (RestClientException ex) {
            throw new AiServiceException("Failed to communicate with Python AI Service: " + ex.getMessage(), 500, ex);
        }
    }
}
