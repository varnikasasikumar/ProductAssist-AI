package com.productassist.backend.assistant.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.productassist.backend.ai.exception.AiGlobalExceptionHandler;
import com.productassist.backend.ai.exception.AiServiceException;
import com.productassist.backend.assistant.dto.*;
import com.productassist.backend.assistant.service.AssistantService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AssistantController.class)
@Import(AiGlobalExceptionHandler.class)
public class AssistantControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private AssistantService assistantService;

    // /api/assistant/ask Tests
    @Test
    public void testAsk_Success() throws Exception {
        AssistantAskRequestDto request = new AssistantAskRequestDto(
                "What should I do if the CNC-X100 shows E105?",
                "CNC-X100",
                5
        );

        SourceCitationDto source = new SourceCitationDto(
                "troubleshooting-guide.pdf",
                "troubleshooting",
                1,
                "E105 Cooling System Malfunction"
        );

        AssistantAskResponseDto expectedResponse = new AssistantAskResponseDto(
                request.getQuery(),
                request.getModel(),
                "Inspect the coolant reservoir level...",
                List.of(source)
        );

        Mockito.when(assistantService.ask(any(AssistantAskRequestDto.class))).thenReturn(expectedResponse);

        mockMvc.perform(post("/api/assistant/ask")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.query").value("What should I do if the CNC-X100 shows E105?"))
                .andExpect(jsonPath("$.model").value("CNC-X100"))
                .andExpect(jsonPath("$.answer").value("Inspect the coolant reservoir level..."))
                .andExpect(jsonPath("$.sources[0].document_name").value("troubleshooting-guide.pdf"))
                .andExpect(jsonPath("$.sources[0].page_number").value(1));
    }

    @Test
    public void testAsk_ValidationFailure_BlankQuery() throws Exception {
        AssistantAskRequestDto request = new AssistantAskRequestDto(
                "   ",
                "CNC-X100",
                5
        );

        mockMvc.perform(post("/api/assistant/ask")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.error").value("Bad Request"))
                .andExpect(jsonPath("$.message").value("query: Query must not be blank"));
    }

    @Test
    public void testAsk_AiServiceFailureHandling() throws Exception {
        AssistantAskRequestDto request = new AssistantAskRequestDto(
                "What should I do if the CNC-X100 shows E105?",
                "CNC-X100",
                5
        );

        Mockito.when(assistantService.ask(any(AssistantAskRequestDto.class)))
                .thenThrow(new AiServiceException("Python AI Service connection failed", 502));

        mockMvc.perform(post("/api/assistant/ask")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadGateway())
                .andExpect(jsonPath("$.status").value(502))
                .andExpect(jsonPath("$.error").value("Bad Gateway"))
                .andExpect(jsonPath("$.message").value("Python AI Service connection failed"));
    }

    // /api/assistant/troubleshoot/start Tests
    @Test
    public void testStartTroubleshooting_Success() throws Exception {
        AssistantTroubleshootStartRequestDto request = new AssistantTroubleshootStartRequestDto(
                "CNC Machine",
                "CNC-X100",
                "The machine stopped suddenly and shows error E105"
        );

        SourceCitationDto source = new SourceCitationDto(
                "troubleshooting-guide.pdf",
                "TROUBLESHOOTING",
                1,
                "E105 Cooling System Malfunction"
        );

        AssistantTroubleshootResponseDto expectedResponse = new AssistantTroubleshootResponseDto(
                "session-123",
                "CNC Machine",
                "CNC-X100",
                "DIAGNOSING",
                "Cooling System Malfunction",
                "Check the coolant sight glass on the reservoir tank.",
                null,
                List.of(source)
        );

        Mockito.when(assistantService.startTroubleshooting(any(AssistantTroubleshootStartRequestDto.class)))
                .thenReturn(expectedResponse);

        mockMvc.perform(post("/api/assistant/troubleshoot/start")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.session_id").value("session-123"))
                .andExpect(jsonPath("$.product").value("CNC Machine"))
                .andExpect(jsonPath("$.model").value("CNC-X100"))
                .andExpect(jsonPath("$.status").value("DIAGNOSING"))
                .andExpect(jsonPath("$.identified_issue").value("Cooling System Malfunction"))
                .andExpect(jsonPath("$.response").value("Check the coolant sight glass on the reservoir tank."))
                .andExpect(jsonPath("$.sources[0].document_name").value("troubleshooting-guide.pdf"));
    }

    @Test
    public void testStartTroubleshooting_ValidationFailure_BlankProduct() throws Exception {
        AssistantTroubleshootStartRequestDto request = new AssistantTroubleshootStartRequestDto(
                "",
                "CNC-X100",
                "The machine stopped suddenly and shows error E105"
        );

        mockMvc.perform(post("/api/assistant/troubleshoot/start")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.error").value("Bad Request"))
                .andExpect(jsonPath("$.message").value("product: Product must not be blank"));
    }

    @Test
    public void testStartTroubleshooting_ValidationFailure_BlankModel() throws Exception {
        AssistantTroubleshootStartRequestDto request = new AssistantTroubleshootStartRequestDto(
                "CNC Machine",
                "   ",
                "The machine stopped suddenly and shows error E105"
        );

        mockMvc.perform(post("/api/assistant/troubleshoot/start")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.error").value("Bad Request"))
                .andExpect(jsonPath("$.message").value("model: Model must not be blank"));
    }

    @Test
    public void testStartTroubleshooting_ValidationFailure_BlankProblem() throws Exception {
        AssistantTroubleshootStartRequestDto request = new AssistantTroubleshootStartRequestDto(
                "CNC Machine",
                "CNC-X100",
                ""
        );

        mockMvc.perform(post("/api/assistant/troubleshoot/start")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.error").value("Bad Request"))
                .andExpect(jsonPath("$.message").value("problem: Problem must not be blank"));
    }

    // /api/assistant/troubleshoot/{sessionId}/respond Tests
    @Test
    public void testContinueTroubleshooting_Success() throws Exception {
        AssistantTroubleshootRespondRequestDto request = new AssistantTroubleshootRespondRequestDto(
                "The coolant level is below MIN."
        );

        AssistantTroubleshootResponseDto expectedResponse = new AssistantTroubleshootResponseDto(
                "session-123",
                "CNC Machine",
                "CNC-X100",
                "CORRECTIVE_ACTION",
                "Cooling System Malfunction - Low Coolant Level",
                "Refill coolant reservoir to MAX level.",
                null,
                List.of()
        );

        Mockito.when(assistantService.continueTroubleshooting(eq("session-123"), any(AssistantTroubleshootRespondRequestDto.class)))
                .thenReturn(expectedResponse);

        mockMvc.perform(post("/api/assistant/troubleshoot/session-123/respond")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.session_id").value("session-123"))
                .andExpect(jsonPath("$.status").value("CORRECTIVE_ACTION"))
                .andExpect(jsonPath("$.response").value("Refill coolant reservoir to MAX level."));
    }

    @Test
    public void testContinueTroubleshooting_ValidationFailure_BlankMessage() throws Exception {
        AssistantTroubleshootRespondRequestDto request = new AssistantTroubleshootRespondRequestDto(
                "   "
        );

        mockMvc.perform(post("/api/assistant/troubleshoot/session-123/respond")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.error").value("Bad Request"))
                .andExpect(jsonPath("$.message").value("message: Message must not be blank"));
    }

    // GET /api/assistant/troubleshoot/{sessionId} Tests
    @Test
    public void testGetTroubleshootingSession_Success() throws Exception {
        AssistantTroubleshootResponseDto expectedResponse = new AssistantTroubleshootResponseDto(
                "session-123",
                "CNC Machine",
                "CNC-X100",
                "RESOLVED",
                "Cooling System Malfunction",
                "Problem resolved. Machine restarted successfully.",
                "Problem resolved. Machine restarted successfully.",
                List.of()
        );

        Mockito.when(assistantService.getTroubleshootingSession("session-123"))
                .thenReturn(expectedResponse);

        mockMvc.perform(get("/api/assistant/troubleshoot/session-123"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.session_id").value("session-123"))
                .andExpect(jsonPath("$.status").value("RESOLVED"))
                .andExpect(jsonPath("$.resolution").value("Problem resolved. Machine restarted successfully."));
    }

    // Multimodal Vision Tests
    @Test
    public void testAnalyzeVision_ValidImage_Success() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "panel.jpg",
                MediaType.IMAGE_JPEG_VALUE,
                "fake image content".getBytes()
        );

        AssistantVisionAnalysisResponseDto expectedResponse = new AssistantVisionAnalysisResponseDto(
                "CNC Machine",
                "CNC-X100",
                "E105",
                List.of("ALARM E105", "COOLANT FLOW"),
                "Coolant Flow Low Alarm visible on HMI",
                0.95,
                "Clear visual match for control panel display"
        );

        Mockito.when(assistantService.analyzeVision(any())).thenReturn(expectedResponse);

        mockMvc.perform(multipart("/api/assistant/vision/analyze").file(file))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.detected_product").value("CNC Machine"))
                .andExpect(jsonPath("$.detected_model").value("CNC-X100"))
                .andExpect(jsonPath("$.detected_error_code").value("E105"))
                .andExpect(jsonPath("$.confidence").value(0.95));
    }

    @Test
    public void testAnalyzeVision_EmptyImage_BadRequest() throws Exception {
        MockMultipartFile emptyFile = new MockMultipartFile(
                "file",
                "empty.jpg",
                MediaType.IMAGE_JPEG_VALUE,
                new byte[0]
        );

        Mockito.when(assistantService.analyzeVision(any()))
                .thenThrow(new AiServiceException("Uploaded image file must be provided and cannot be empty.", 400));

        mockMvc.perform(multipart("/api/assistant/vision/analyze").file(emptyFile))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.message").value("Uploaded image file must be provided and cannot be empty."));
    }

    @Test
    public void testStartTroubleshootingWithImage_ValidImage_Success() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "panel.jpg",
                MediaType.IMAGE_JPEG_VALUE,
                "fake image content".getBytes()
        );

        AssistantVisionAnalysisResponseDto visionAnalysis = new AssistantVisionAnalysisResponseDto(
                "CNC Machine",
                "CNC-X100",
                "E105",
                List.of("E105"),
                "E105 Alarm",
                0.95,
                "Notes"
        );

        AssistantTroubleshootResponseDto session = new AssistantTroubleshootResponseDto(
                "session-v123",
                "CNC Machine",
                "CNC-X100",
                "DIAGNOSING",
                "Cooling System Malfunction",
                "Check coolant level.",
                null,
                List.of()
        );

        AssistantVisionTroubleshootResponseDto expectedResponse = new AssistantVisionTroubleshootResponseDto(visionAnalysis, session);

        Mockito.when(assistantService.startTroubleshootingWithImage(any())).thenReturn(expectedResponse);

        mockMvc.perform(multipart("/api/assistant/troubleshoot/start-with-image").file(file))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.vision_analysis.detected_error_code").value("E105"))
                .andExpect(jsonPath("$.troubleshooting_session.session_id").value("session-v123"))
                .andExpect(jsonPath("$.troubleshooting_session.status").value("DIAGNOSING"));
    }

    @Test
    public void testVision_AiServiceFailureHandling() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "panel.jpg",
                MediaType.IMAGE_JPEG_VALUE,
                "fake image content".getBytes()
        );

        Mockito.when(assistantService.analyzeVision(any()))
                .thenThrow(new AiServiceException("Gemini Vision API error: 502 Bad Gateway", 502));

        mockMvc.perform(multipart("/api/assistant/vision/analyze").file(file))
                .andExpect(status().isBadGateway())
                .andExpect(jsonPath("$.status").value(502))
                .andExpect(jsonPath("$.message").value("Gemini Vision API error: 502 Bad Gateway"));
    }
}
