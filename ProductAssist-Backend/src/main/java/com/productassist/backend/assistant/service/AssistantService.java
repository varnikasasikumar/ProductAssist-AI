package com.productassist.backend.assistant.service;

import com.productassist.backend.ai.client.AiServiceClient;
import com.productassist.backend.ai.dto.*;
import com.productassist.backend.ai.exception.AiServiceException;
import com.productassist.backend.assistant.dto.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.Collections;
import java.util.List;

@Service
public class AssistantService {

    private final AiServiceClient aiServiceClient;

    @Autowired
    public AssistantService(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    public AssistantAskResponseDto ask(AssistantAskRequestDto request) {
        RagAskRequestDto aiRequest = new RagAskRequestDto(
                request.getQuery(),
                request.getModel(),
                request.getTop_k()
        );

        RagAskResponseDto aiResponse = aiServiceClient.askRag(aiRequest);

        List<SourceCitationDto> sources = Collections.emptyList();
        if (aiResponse != null && aiResponse.getSources() != null) {
            sources = aiResponse.getSources().stream()
                    .map(item -> new SourceCitationDto(
                            item.getDocument_name(),
                            item.getDocument_type(),
                            item.getPage_number(),
                            item.getSection()
                    ))
                    .toList();
        }

        return new AssistantAskResponseDto(
                aiResponse != null ? aiResponse.getQuery() : request.getQuery(),
                aiResponse != null ? aiResponse.getModel() : request.getModel(),
                aiResponse != null ? aiResponse.getAnswer() : "",
                sources
        );
    }

    public AssistantTroubleshootResponseDto startTroubleshooting(AssistantTroubleshootStartRequestDto request) {
        StartTroubleshootingRequestDto aiRequest = new StartTroubleshootingRequestDto(
                request.getModel(),
                request.getProblem()
        );

        TroubleshootingResponseDto aiResponse = aiServiceClient.startTroubleshooting(aiRequest);
        return mapTroubleshootingResponse(aiResponse, request.getProduct(), request.getModel());
    }

    public AssistantTroubleshootResponseDto continueTroubleshooting(String sessionId, AssistantTroubleshootRespondRequestDto request) {
        ContinueTroubleshootingRequestDto aiRequest = new ContinueTroubleshootingRequestDto(
                request.getMessage()
        );

        TroubleshootingResponseDto aiResponse = aiServiceClient.continueTroubleshooting(sessionId, aiRequest);
        return mapTroubleshootingResponse(aiResponse, null, null);
    }

    public AssistantTroubleshootResponseDto getTroubleshootingSession(String sessionId) {
        TroubleshootingResponseDto aiResponse = aiServiceClient.getTroubleshootingSession(sessionId);
        return mapTroubleshootingResponse(aiResponse, null, null);
    }

    public AssistantVisionAnalysisResponseDto analyzeVision(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new AiServiceException("Uploaded image file must be provided and cannot be empty.", 400);
        }

        VisionAnalysisResponseDto aiResponse = aiServiceClient.analyzeVision(file);
        return mapVisionAnalysisResponse(aiResponse);
    }

    public AssistantVisionTroubleshootResponseDto startTroubleshootingWithImage(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new AiServiceException("Uploaded image file must be provided and cannot be empty.", 400);
        }

        VisionTroubleshootResponseDto aiResponse = aiServiceClient.startTroubleshootingWithImage(file);

        AssistantVisionAnalysisResponseDto visionDto = null;
        if (aiResponse != null && aiResponse.getVision_analysis() != null) {
            visionDto = mapVisionAnalysisResponse(aiResponse.getVision_analysis());
        }

        AssistantTroubleshootResponseDto sessionDto = null;
        if (aiResponse != null && aiResponse.getTroubleshooting_session() != null) {
            sessionDto = mapTroubleshootingResponse(aiResponse.getTroubleshooting_session(), null, null);
        }

        return new AssistantVisionTroubleshootResponseDto(visionDto, sessionDto);
    }

    public SttResponseDto transcribeVoice(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new AiServiceException("Uploaded audio file must be provided and cannot be empty.", 400);
        }
        return aiServiceClient.transcribeVoice(file);
    }

    public byte[] synthesizeVoice(TtsRequestDto request) {
        if (request == null || request.getText() == null || request.getText().isBlank()) {
            throw new AiServiceException("Text for speech synthesis must not be blank.", 400);
        }
        return aiServiceClient.synthesizeVoice(request);
    }

    public AssistantVoiceTroubleshootResponseDto startTroubleshootingWithVoice(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new AiServiceException("Uploaded audio file must be provided and cannot be empty.", 400);
        }

        VoiceTroubleshootResponseDto aiResponse = aiServiceClient.startTroubleshootingWithVoice(file);

        SttResponseDto sttDto = null;
        if (aiResponse != null && aiResponse.getTranscription() != null) {
            sttDto = aiResponse.getTranscription();
        }

        AssistantTroubleshootResponseDto sessionDto = null;
        if (aiResponse != null && aiResponse.getTroubleshooting_session() != null) {
            sessionDto = mapTroubleshootingResponse(aiResponse.getTroubleshooting_session(), null, null);
        }

        return new AssistantVoiceTroubleshootResponseDto(sttDto, sessionDto);
    }

    private AssistantVisionAnalysisResponseDto mapVisionAnalysisResponse(VisionAnalysisResponseDto aiResponse) {
        if (aiResponse == null) {
            return new AssistantVisionAnalysisResponseDto();
        }
        return new AssistantVisionAnalysisResponseDto(
                aiResponse.getDetected_product(),
                aiResponse.getDetected_model(),
                aiResponse.getDetected_error_code(),
                aiResponse.getVisible_text(),
                aiResponse.getObserved_issue(),
                aiResponse.getConfidence(),
                aiResponse.getNotes()
        );
    }

    private AssistantTroubleshootResponseDto mapTroubleshootingResponse(TroubleshootingResponseDto aiResponse,
                                                                        String fallbackProduct,
                                                                        String fallbackModel) {
        if (aiResponse == null) {
            return new AssistantTroubleshootResponseDto();
        }

        List<SourceCitationDto> sources = Collections.emptyList();
        if (aiResponse.getSources() != null) {
            sources = aiResponse.getSources().stream()
                    .map(item -> new SourceCitationDto(
                            item.getDocument_name(),
                            item.getDocument_type(),
                            item.getPage_number(),
                            item.getSection()
                    ))
                    .toList();
        }

        String product = fallbackProduct != null ? fallbackProduct : "CNC Machine";
        String model = aiResponse.getModel() != null ? aiResponse.getModel() : fallbackModel;
        String status = aiResponse.getStatus();
        String responseMessage = aiResponse.getMessage();
        String resolution = "RESOLVED".equalsIgnoreCase(status) ? responseMessage : null;

        return new AssistantTroubleshootResponseDto(
                aiResponse.getSession_id(),
                product,
                model,
                status,
                aiResponse.getIdentified_issue(),
                responseMessage,
                resolution,
                sources
        );
    }
}
