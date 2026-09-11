package com.productassist.backend.ai.controller;

import com.productassist.backend.ai.client.AiServiceClient;
import com.productassist.backend.ai.dto.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.Map;

@RestController
@RequestMapping("/api/ai")
public class AiVerificationController {

    private final AiServiceClient aiServiceClient;

    @Autowired
    public AiVerificationController(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    @GetMapping("/health")
    public ResponseEntity<AiHealthResponseDto> getAiHealth() {
        return ResponseEntity.ok(aiServiceClient.getHealth());
    }

    @PostMapping("/rag/search")
    public ResponseEntity<RagSearchResponseDto> searchRag(@RequestBody RagSearchRequestDto request) {
        return ResponseEntity.ok(aiServiceClient.searchRag(request));
    }

    @PostMapping("/rag/ask")
    public ResponseEntity<RagAskResponseDto> askRag(@RequestBody RagAskRequestDto request) {
        return ResponseEntity.ok(aiServiceClient.askRag(request));
    }

    @PostMapping("/troubleshoot/start")
    public ResponseEntity<TroubleshootingResponseDto> startTroubleshooting(@RequestBody StartTroubleshootingRequestDto request) {
        return ResponseEntity.ok(aiServiceClient.startTroubleshooting(request));
    }

    @PostMapping("/troubleshoot/{sessionId}/respond")
    public ResponseEntity<TroubleshootingResponseDto> continueTroubleshooting(
            @PathVariable("sessionId") String sessionId,
            @RequestBody ContinueTroubleshootingRequestDto request) {
        return ResponseEntity.ok(aiServiceClient.continueTroubleshooting(sessionId, request));
    }

    @GetMapping("/troubleshoot/{sessionId}")
    public ResponseEntity<TroubleshootingResponseDto> getTroubleshootingSession(@PathVariable("sessionId") String sessionId) {
        return ResponseEntity.ok(aiServiceClient.getTroubleshootingSession(sessionId));
    }

    @PostMapping(value = "/vision/analyze", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<VisionAnalysisResponseDto> analyzeVision(@RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(aiServiceClient.analyzeVision(file));
    }

    @PostMapping(value = "/troubleshoot/start-with-image", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<VisionTroubleshootResponseDto> startTroubleshootingWithImage(@RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(aiServiceClient.startTroubleshootingWithImage(file));
    }

    @PostMapping(value = "/voice/transcribe", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<SttResponseDto> transcribeVoice(@RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(aiServiceClient.transcribeVoice(file));
    }

    @PostMapping("/voice/synthesize")
    public ResponseEntity<byte[]> synthesizeVoice(@RequestBody TtsRequestDto request) {
        byte[] audioBytes = aiServiceClient.synthesizeVoice(request);
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType("audio/wav"));
        return ResponseEntity.ok().headers(headers).body(audioBytes);
    }

    @PostMapping(value = "/troubleshoot/start-with-voice", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<VoiceTroubleshootResponseDto> startTroubleshootingWithVoice(@RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(aiServiceClient.startTroubleshootingWithVoice(file));
    }

    @PostMapping(value = "/troubleshoot/{sessionId}/respond-with-voice", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<Map<String, Object>> respondToTroubleshootingWithVoice(
            @PathVariable("sessionId") String sessionId,
            @RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(aiServiceClient.respondToTroubleshootingWithVoice(sessionId, file));
    }
}
