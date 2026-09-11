package com.productassist.backend.assistant.service;

import com.productassist.backend.ai.client.AiServiceClient;
import com.productassist.backend.ai.dto.*;
import com.productassist.backend.ai.exception.AiServiceException;
import com.productassist.backend.assistant.dto.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mock.web.MockMultipartFile;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;

@ExtendWith(MockitoExtension.class)
public class AssistantServiceTest {

    @Mock
    private AiServiceClient aiServiceClient;

    @InjectMocks
    private AssistantService assistantService;

    @Test
    public void testAsk_DelegatesToAiServiceClientAndMapsResponse() {
        AssistantAskRequestDto request = new AssistantAskRequestDto(
                "How to resolve E105 alarm?",
                "CNC-X100",
                5
        );

        SourceCitationItemDto citation = new SourceCitationItemDto();
        citation.setDocument_name("troubleshooting-guide.pdf");
        citation.setDocument_type("troubleshooting");
        citation.setPage_number(1);
        citation.setSection("E105 Cooling System");

        RagAskResponseDto aiResponse = new RagAskResponseDto();
        aiResponse.setQuery("How to resolve E105 alarm?");
        aiResponse.setModel("CNC-X100");
        aiResponse.setAnswer("Check coolant sight glass...");
        aiResponse.setSources(List.of(citation));

        Mockito.when(aiServiceClient.askRag(any(RagAskRequestDto.class))).thenReturn(aiResponse);

        AssistantAskResponseDto response = assistantService.ask(request);

        assertNotNull(response);
        assertEquals("How to resolve E105 alarm?", response.getQuery());
        assertEquals("CNC-X100", response.getModel());
        assertEquals("Check coolant sight glass...", response.getAnswer());
        assertEquals(1, response.getSources().size());
        assertEquals("troubleshooting-guide.pdf", response.getSources().get(0).getDocumentName());
        assertEquals(1, response.getSources().get(0).getPageNumber());
    }

    @Test
    public void testStartTroubleshooting_DelegatesToAiServiceClientAndMapsResponse() {
        AssistantTroubleshootStartRequestDto request = new AssistantTroubleshootStartRequestDto(
                "CNC Machine",
                "CNC-X100",
                "E105 cooling system error"
        );

        TroubleshootingSourceItemDto citation = new TroubleshootingSourceItemDto();
        citation.setDocument_name("troubleshooting-guide.pdf");
        citation.setDocument_type("TROUBLESHOOTING");
        citation.setPage_number(1);
        citation.setSection("E105 Diagnostic Section");

        TroubleshootingResponseDto aiResponse = new TroubleshootingResponseDto();
        aiResponse.setSession_id("session-999");
        aiResponse.setModel("CNC-X100");
        aiResponse.setIdentified_issue("Cooling System Malfunction");
        aiResponse.setMessage("Check coolant sight glass level.");
        aiResponse.setStatus("DIAGNOSING");
        aiResponse.setSources(List.of(citation));

        Mockito.when(aiServiceClient.startTroubleshooting(any(StartTroubleshootingRequestDto.class))).thenReturn(aiResponse);

        AssistantTroubleshootResponseDto response = assistantService.startTroubleshooting(request);

        assertNotNull(response);
        assertEquals("session-999", response.getSessionId());
        assertEquals("CNC Machine", response.getProduct());
        assertEquals("CNC-X100", response.getModel());
        assertEquals("DIAGNOSING", response.getStatus());
        assertEquals("Cooling System Malfunction", response.getIdentifiedIssue());
        assertEquals("Check coolant sight glass level.", response.getResponse());
        assertNull(response.getResolution());
        assertEquals(1, response.getSources().size());
        assertEquals("troubleshooting-guide.pdf", response.getSources().get(0).getDocumentName());
    }

    @Test
    public void testContinueTroubleshooting_DelegatesToAiServiceClientAndMapsResponse() {
        AssistantTroubleshootRespondRequestDto request = new AssistantTroubleshootRespondRequestDto(
                "Coolant level is below MIN"
        );

        TroubleshootingResponseDto aiResponse = new TroubleshootingResponseDto();
        aiResponse.setSession_id("session-999");
        aiResponse.setModel("CNC-X100");
        aiResponse.setIdentified_issue("Cooling System Malfunction");
        aiResponse.setMessage("Refill coolant emulsion to MAX mark.");
        aiResponse.setStatus("CORRECTIVE_ACTION");
        aiResponse.setSources(List.of());

        Mockito.when(aiServiceClient.continueTroubleshooting(eq("session-999"), any(ContinueTroubleshootingRequestDto.class)))
                .thenReturn(aiResponse);

        AssistantTroubleshootResponseDto response = assistantService.continueTroubleshooting("session-999", request);

        assertNotNull(response);
        assertEquals("session-999", response.getSessionId());
        assertEquals("CORRECTIVE_ACTION", response.getStatus());
        assertEquals("Refill coolant emulsion to MAX mark.", response.getResponse());
        assertNull(response.getResolution());
    }

    @Test
    public void testGetTroubleshootingSession_DelegatesToAiServiceClientAndMapsResolvedResponse() {
        TroubleshootingResponseDto aiResponse = new TroubleshootingResponseDto();
        aiResponse.setSession_id("session-999");
        aiResponse.setModel("CNC-X100");
        aiResponse.setIdentified_issue("Cooling System Malfunction");
        aiResponse.setMessage("Issue resolved. Machine operating normally.");
        aiResponse.setStatus("RESOLVED");
        aiResponse.setSources(List.of());

        Mockito.when(aiServiceClient.getTroubleshootingSession("session-999"))
                .thenReturn(aiResponse);

        AssistantTroubleshootResponseDto response = assistantService.getTroubleshootingSession("session-999");

        assertNotNull(response);
        assertEquals("session-999", response.getSessionId());
        assertEquals("RESOLVED", response.getStatus());
        assertEquals("Issue resolved. Machine operating normally.", response.getResponse());
        assertEquals("Issue resolved. Machine operating normally.", response.getResolution());
    }

    @Test
    public void testAnalyzeVision_DelegatesAndMapsResponse() {
        MockMultipartFile file = new MockMultipartFile("file", "panel.jpg", "image/jpeg", "image content".getBytes());

        VisionAnalysisResponseDto aiResponse = new VisionAnalysisResponseDto();
        aiResponse.setDetected_product("CNC Machine");
        aiResponse.setDetected_model("CNC-X100");
        aiResponse.setDetected_error_code("E105");
        aiResponse.setVisible_text(List.of("E105 ALARM"));
        aiResponse.setObserved_issue("Coolant Alarm");
        aiResponse.setConfidence(0.98);
        aiResponse.setNotes("Visual scan complete");

        Mockito.when(aiServiceClient.analyzeVision(any())).thenReturn(aiResponse);

        AssistantVisionAnalysisResponseDto response = assistantService.analyzeVision(file);

        assertNotNull(response);
        assertEquals("CNC Machine", response.getDetectedProduct());
        assertEquals("CNC-X100", response.getDetectedModel());
        assertEquals("E105", response.getDetectedErrorCode());
        assertEquals(0.98, response.getConfidence());
        assertEquals("Visual scan complete", response.getNotes());
    }

    @Test
    public void testStartTroubleshootingWithImage_DelegatesAndMapsResponse() {
        MockMultipartFile file = new MockMultipartFile("file", "panel.jpg", "image/jpeg", "image content".getBytes());

        VisionAnalysisResponseDto visionPart = new VisionAnalysisResponseDto();
        visionPart.setDetected_product("CNC Machine");
        visionPart.setDetected_model("CNC-X100");
        visionPart.setDetected_error_code("E105");
        visionPart.setObserved_issue("E105 Alarm");
        visionPart.setConfidence(0.95);

        TroubleshootingResponseDto sessionPart = new TroubleshootingResponseDto();
        sessionPart.setSession_id("session-v123");
        sessionPart.setModel("CNC-X100");
        sessionPart.setStatus("DIAGNOSING");
        sessionPart.setIdentified_issue("Cooling System Malfunction");
        sessionPart.setMessage("Check coolant sight glass level.");
        sessionPart.setSources(List.of());

        VisionTroubleshootResponseDto aiResponse = new VisionTroubleshootResponseDto();
        aiResponse.setVision_analysis(visionPart);
        aiResponse.setTroubleshooting_session(sessionPart);

        Mockito.when(aiServiceClient.startTroubleshootingWithImage(any())).thenReturn(aiResponse);

        AssistantVisionTroubleshootResponseDto response = assistantService.startTroubleshootingWithImage(file);

        assertNotNull(response);
        assertNotNull(response.getVisionAnalysis());
        assertEquals("CNC-X100", response.getVisionAnalysis().getDetectedModel());
        assertNotNull(response.getTroubleshootingSession());
        assertEquals("session-v123", response.getTroubleshootingSession().getSessionId());
        assertEquals("DIAGNOSING", response.getTroubleshootingSession().getStatus());
    }

    @Test
    public void testVision_EmptyFile_ThrowsAiServiceException() {
        MockMultipartFile emptyFile = new MockMultipartFile("file", "panel.jpg", "image/jpeg", new byte[0]);

        AiServiceException ex1 = assertThrows(AiServiceException.class, () -> assistantService.analyzeVision(emptyFile));
        assertEquals(400, ex1.getStatusCode());

        AiServiceException ex2 = assertThrows(AiServiceException.class, () -> assistantService.startTroubleshootingWithImage(emptyFile));
        assertEquals(400, ex2.getStatusCode());
    }
}
