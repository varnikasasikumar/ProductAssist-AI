package com.productassist.backend.assistant.controller;

import com.productassist.backend.ai.dto.SttResponseDto;
import com.productassist.backend.ai.dto.TtsRequestDto;
import com.productassist.backend.assistant.dto.*;
import com.productassist.backend.assistant.service.AssistantService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@CrossOrigin(origins = {"http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"})
@RequestMapping("/api/assistant")
public class AssistantController {

    private final AssistantService assistantService;

    @Autowired
    public AssistantController(AssistantService assistantService) {
        this.assistantService = assistantService;
    }

    @PostMapping("/ask")
    public ResponseEntity<AssistantAskResponseDto> ask(@Valid @RequestBody AssistantAskRequestDto request) {
        AssistantAskResponseDto response = assistantService.ask(request);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/troubleshoot/start")
    public ResponseEntity<AssistantTroubleshootResponseDto> startTroubleshooting(
            @Valid @RequestBody AssistantTroubleshootStartRequestDto request) {
        AssistantTroubleshootResponseDto response = assistantService.startTroubleshooting(request);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/troubleshoot/{sessionId}/respond")
    public ResponseEntity<AssistantTroubleshootResponseDto> continueTroubleshooting(
            @PathVariable("sessionId") String sessionId,
            @Valid @RequestBody AssistantTroubleshootRespondRequestDto request) {
        AssistantTroubleshootResponseDto response = assistantService.continueTroubleshooting(sessionId, request);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/troubleshoot/{sessionId}")
    public ResponseEntity<AssistantTroubleshootResponseDto> getTroubleshootingSession(
            @PathVariable("sessionId") String sessionId) {
        AssistantTroubleshootResponseDto response = assistantService.getTroubleshootingSession(sessionId);
        return ResponseEntity.ok(response);
    }

    @PostMapping(value = "/vision/analyze", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<AssistantVisionAnalysisResponseDto> analyzeVision(@RequestParam("file") MultipartFile file) {
        AssistantVisionAnalysisResponseDto response = assistantService.analyzeVision(file);
        return ResponseEntity.ok(response);
    }

    @PostMapping(value = "/troubleshoot/start-with-image", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<AssistantVisionTroubleshootResponseDto> startTroubleshootingWithImage(
            @RequestParam("file") MultipartFile file) {
        AssistantVisionTroubleshootResponseDto response = assistantService.startTroubleshootingWithImage(file);
        return ResponseEntity.ok(response);
    }

    @PostMapping(value = "/voice/transcribe", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<SttResponseDto> transcribeVoice(@RequestParam("file") MultipartFile file) {
        SttResponseDto response = assistantService.transcribeVoice(file);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/voice/synthesize")
    public ResponseEntity<byte[]> synthesizeVoice(@Valid @RequestBody TtsRequestDto request) {
        byte[] audioBytes = assistantService.synthesizeVoice(request);
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType("audio/wav"))
                .body(audioBytes);
    }

    @PostMapping(value = "/voice/troubleshoot", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<AssistantVoiceTroubleshootResponseDto> startTroubleshootingWithVoice(
            @RequestParam("file") MultipartFile file) {
        AssistantVoiceTroubleshootResponseDto response = assistantService.startTroubleshootingWithVoice(file);
        return ResponseEntity.ok(response);
    }
}
