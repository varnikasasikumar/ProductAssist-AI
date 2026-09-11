package com.productassist.backend.ai.client;

import com.productassist.backend.ai.config.AiServiceConfig;
import com.productassist.backend.ai.dto.*;
import com.productassist.backend.ai.exception.AiServiceException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.client.RestClientTest;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestTemplate;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.*;
import static org.springframework.test.web.client.response.MockRestResponseCreators.*;

@RestClientTest({AiServiceClient.class, AiServiceConfig.class})
@TestPropertySource(properties = "ai.service.base-url=http://127.0.0.1:8000")
public class AiServiceClientTest {

    @Autowired
    private AiServiceClient aiServiceClient;

    @Autowired
    private RestTemplate aiRestTemplate;

    private MockRestServiceServer mockServer;

    @BeforeEach
    public void setUp() {
        mockServer = MockRestServiceServer.createServer(aiRestTemplate);
    }

    @Test
    public void testGetHealth_Success() {
        mockServer.expect(requestTo("http://127.0.0.1:8000/health"))
                .andExpect(method(HttpMethod.GET))
                .andRespond(withSuccess("{\"status\":\"UP\",\"service\":\"ProductAssist AI Service\"}", MediaType.APPLICATION_JSON));

        AiHealthResponseDto health = aiServiceClient.getHealth();
        assertNotNull(health);
        assertEquals("UP", health.getStatus());
        mockServer.verify();
    }

    @Test
    public void testSearchRag_Success() {
        mockServer.expect(requestTo("http://127.0.0.1:8000/rag/search"))
                .andExpect(method(HttpMethod.POST))
                .andRespond(withSuccess("{\"query\":\"E105\",\"top_k\":5,\"total_results\":1,\"results\":[]}", MediaType.APPLICATION_JSON));

        RagSearchRequestDto request = new RagSearchRequestDto("E105", "CNC-X100", 5);
        RagSearchResponseDto response = aiServiceClient.searchRag(request);

        assertNotNull(response);
        assertEquals("E105", response.getQuery());
        mockServer.verify();
    }

    @Test
    public void testAskRag_Success() {
        mockServer.expect(requestTo("http://127.0.0.1:8000/rag/ask"))
                .andExpect(method(HttpMethod.POST))
                .andRespond(withSuccess("{\"query\":\"E105\",\"answer\":\"Check coolant level.\",\"sources\":[],\"retrieved_chunks\":3}", MediaType.APPLICATION_JSON));

        RagAskRequestDto request = new RagAskRequestDto("E105", "CNC-X100", 5);
        RagAskResponseDto response = aiServiceClient.askRag(request);

        assertNotNull(response);
        assertEquals("Check coolant level.", response.getAnswer());
        mockServer.verify();
    }

    @Test
    public void testStartTroubleshooting_Success() {
        mockServer.expect(requestTo("http://127.0.0.1:8000/troubleshoot/start"))
                .andExpect(method(HttpMethod.POST))
                .andRespond(withSuccess("{\"session_id\":\"s-123\",\"model\":\"CNC-X100\",\"status\":\"DIAGNOSING\",\"message\":\"Started\",\"next_question\":\"Is coolant level low?\",\"sources\":[]}", MediaType.APPLICATION_JSON));

        StartTroubleshootingRequestDto request = new StartTroubleshootingRequestDto("CNC-X100", "E105 alarm");
        TroubleshootingResponseDto response = aiServiceClient.startTroubleshooting(request);

        assertNotNull(response);
        assertEquals("s-123", response.getSession_id());
        assertEquals("DIAGNOSING", response.getStatus());
        mockServer.verify();
    }

    @Test
    public void testPythonServiceUnavailable_ThrowsAiServiceException() {
        mockServer.expect(requestTo("http://127.0.0.1:8000/health"))
                .andExpect(method(HttpMethod.GET))
                .andRespond(withServerError());

        AiServiceException exception = assertThrows(AiServiceException.class, () -> {
            aiServiceClient.getHealth();
        });

        assertEquals(500, exception.getStatusCode());
        mockServer.verify();
    }

    @Test
    public void testHttp400BadRequest_ThrowsAiServiceException() {
        mockServer.expect(requestTo("http://127.0.0.1:8000/rag/search"))
                .andExpect(method(HttpMethod.POST))
                .andRespond(withStatus(HttpStatus.BAD_REQUEST).body("{\"detail\":\"Query parameters invalid\"}"));

        RagSearchRequestDto request = new RagSearchRequestDto("", "CNC-X100", 5);
        AiServiceException exception = assertThrows(AiServiceException.class, () -> {
            aiServiceClient.searchRag(request);
        });

        assertEquals(400, exception.getStatusCode());
        assertTrue(exception.getMessage().contains("Query parameters invalid"));
        mockServer.verify();
    }
}
