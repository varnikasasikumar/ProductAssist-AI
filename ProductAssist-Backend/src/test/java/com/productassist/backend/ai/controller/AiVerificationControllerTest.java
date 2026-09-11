package com.productassist.backend.ai.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.productassist.backend.ai.client.AiServiceClient;
import com.productassist.backend.ai.dto.*;
import com.productassist.backend.ai.exception.AiGlobalExceptionHandler;
import com.productassist.backend.ai.exception.AiServiceException;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.ArrayList;

import static org.mockito.ArgumentMatchers.any;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(AiVerificationController.class)
@Import(AiGlobalExceptionHandler.class)
public class AiVerificationControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private AiServiceClient aiServiceClient;

    @Test
    public void testGetHealth_Success() throws Exception {
        AiHealthResponseDto health = new AiHealthResponseDto("UP", "ProductAssist AI Service", "1.0.0", "Running");
        Mockito.when(aiServiceClient.getHealth()).thenReturn(health);

        mockMvc.perform(get("/api/ai/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"))
                .andExpect(jsonPath("$.service").value("ProductAssist AI Service"));
    }

    @Test
    public void testSearchRag_Success() throws Exception {
        RagSearchResponseDto searchResp = new RagSearchResponseDto();
        searchResp.setQuery("E105");
        searchResp.setTotal_results(2);
        searchResp.setResults(new ArrayList<>());

        Mockito.when(aiServiceClient.searchRag(any(RagSearchRequestDto.class))).thenReturn(searchResp);

        RagSearchRequestDto req = new RagSearchRequestDto("E105", "CNC-X100", 5);

        mockMvc.perform(post("/api/ai/rag/search")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.query").value("E105"))
                .andExpect(jsonPath("$.total_results").value(2));
    }

    @Test
    public void testStartTroubleshooting_Success() throws Exception {
        TroubleshootingResponseDto trResp = new TroubleshootingResponseDto();
        trResp.setSession_id("sess-abc-123");
        trResp.setStatus("DIAGNOSING");
        trResp.setMessage("Cooling System Malfunction detected");
        trResp.setNext_question("Is coolant below MIN?");

        Mockito.when(aiServiceClient.startTroubleshooting(any(StartTroubleshootingRequestDto.class))).thenReturn(trResp);

        StartTroubleshootingRequestDto req = new StartTroubleshootingRequestDto("CNC-X100", "Machine stopped E105");

        mockMvc.perform(post("/api/ai/troubleshoot/start")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(req)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.session_id").value("sess-abc-123"))
                .andExpect(jsonPath("$.status").value("DIAGNOSING"));
    }

    @Test
    public void testServiceUnavailable_Returns503() throws Exception {
        Mockito.when(aiServiceClient.getHealth())
                .thenThrow(new AiServiceException("Python AI Service is unavailable at http://127.0.0.1:8000", 503));

        mockMvc.perform(get("/api/ai/health"))
                .andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.status").value(503))
                .andExpect(jsonPath("$.message").value("Python AI Service is unavailable at http://127.0.0.1:8000"));
    }
}
