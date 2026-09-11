import os
import time
import requests
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

import base64

class LLMKeyMissingError(Exception):
    """Raised when required LLM API key is missing."""
    pass

class LLMProviderError(Exception):
    """Raised when LLM API request fails or returns an error."""
    pass

class LLMClient:
    """
    Provider-agnostic LLM Client supporting Google Gemini, OpenAI, and Local LLMs.
    Configurable via environment variables:
      - LLM_PROVIDER (gemini / google / openai / local)
      - LLM_API_KEY or GEMINI_API_KEY or OPENAI_API_KEY
      - LLM_MODEL (default: gemini-2.5-flash)
    """
    def __init__(self, provider: Optional[str] = None, api_key: Optional[str] = None, model: Optional[str] = None):
        self.provider = (provider or os.getenv("LLM_PROVIDER", "gemini")).lower()
        self.model = model or os.getenv("LLM_MODEL", "gemini-2.5-flash")
        
        if self.provider in ["gemini", "google"]:
            self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY") or os.getenv("GOOGLE_API_KEY")
        elif self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
        else:
            self.api_key = api_key or os.getenv("LLM_API_KEY")

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        if not self.api_key and self.provider not in ["ollama", "local", "mock"]:
            raise LLMKeyMissingError(
                f"LLM API key is missing for provider '{self.provider}'. "
                "Please configure GEMINI_API_KEY or LLM_API_KEY in environment variables or ai-service/.env."
            )

        if self.provider in ["gemini", "google"]:
            return self._generate_gemini(system_prompt, user_prompt, temperature)
        elif self.provider == "openai":
            return self._generate_openai(system_prompt, user_prompt, temperature)
        elif self.provider in ["ollama", "local"]:
            return self._generate_local(system_prompt, user_prompt, temperature)
        else:
            raise LLMProviderError(f"Unsupported LLM provider: '{self.provider}'")

    def generate_vision(
        self,
        system_prompt: str,
        user_prompt: str,
        image_bytes: bytes,
        mime_type: str = "image/jpeg",
        temperature: float = 0.1
    ) -> str:
        if not self.api_key and self.provider not in ["ollama", "local", "mock"]:
            raise LLMKeyMissingError(
                f"LLM API key is missing for provider '{self.provider}'. "
                "Please configure GEMINI_API_KEY or LLM_API_KEY in environment variables or ai-service/.env."
            )

        b64_data = base64.b64encode(image_bytes).decode("utf-8")

        if self.provider in ["gemini", "google"]:
            return self._generate_gemini_vision(system_prompt, user_prompt, b64_data, mime_type, temperature)
        elif self.provider == "openai":
            return self._generate_openai_vision(system_prompt, user_prompt, b64_data, mime_type, temperature)
        else:
            # Fallback for local or unsupported vision providers
            return self.generate(system_prompt, user_prompt, temperature)

    def _generate_gemini(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        model_name = self.model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 4096
            }
        }
        
        last_err = None
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=35)
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        text = "".join(part.get("text", "") for part in parts if "text" in part)
                        if text:
                            return text.strip()
                elif response.status_code in [503, 429]:
                    last_err = f"Gemini API returned HTTP {response.status_code}: {response.text}"
                    time.sleep(1.5 * (attempt + 1))
                    continue
                else:
                    try:
                        err_msg = response.json().get("error", {}).get("message", response.text)
                    except Exception:
                        err_msg = response.text
                    last_err = f"Gemini API returned HTTP {response.status_code}: {err_msg}"
                    break
            except Exception as err:
                last_err = f"Network connection failed to Gemini API: {str(err)}"
                time.sleep(1)

        raise LLMProviderError(f"Gemini API Error: {last_err}")

    def _generate_openai(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        model_name = self.model if "gpt" in self.model else "gpt-4o-mini"
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": 4096
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
        except Exception as err:
            raise LLMProviderError(f"Network connection failed to OpenAI API: {str(err)}")

        if response.status_code != 200:
            try:
                err_msg = response.json().get("error", {}).get("message", response.text)
            except Exception:
                err_msg = response.text
            raise LLMProviderError(f"OpenAI API returned HTTP {response.status_code}: {err_msg}")

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError) as e:
            raise LLMProviderError(f"Failed to parse OpenAI API response: {str(e)}")

    def _generate_local(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        payload = {
            "model": self.model if self.model != "gemini-2.5-flash" else "llama3.2",
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        try:
            response = requests.post(ollama_url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            raise LLMProviderError(f"Local LLM returned HTTP {response.status_code}: {response.text}")
        except Exception as e:
            raise LLMProviderError(f"Local LLM error: {str(e)}")

    def _generate_gemini_vision(self, system_prompt: str, user_prompt: str, b64_data: str, mime_type: str, temperature: float) -> str:
        model_name = self.model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": user_prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": b64_data
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 2048
            }
        }
        
        last_err = None
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=35)
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        text = "".join(part.get("text", "") for part in parts if "text" in part)
                        if text:
                            return text.strip()
                elif response.status_code in [503, 429]:
                    last_err = f"Gemini Vision API returned HTTP {response.status_code}: {response.text}"
                    time.sleep(1.5 * (attempt + 1))
                    continue
                else:
                    try:
                        err_msg = response.json().get("error", {}).get("message", response.text)
                    except Exception:
                        err_msg = response.text
                    last_err = f"Gemini Vision API returned HTTP {response.status_code}: {err_msg}"
                    break
            except Exception as err:
                last_err = f"Network connection failed to Gemini Vision API: {str(err)}"
                time.sleep(1)

        raise LLMProviderError(f"Gemini Vision API Error: {last_err}")

    def _generate_openai_vision(self, system_prompt: str, user_prompt: str, b64_data: str, mime_type: str, temperature: float) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        model_name = self.model if "gpt" in self.model else "gpt-4o-mini"
        data_uri = f"data:{mime_type};base64,{b64_data}"
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {"url": data_uri}}
                    ]
                }
            ],
            "temperature": temperature,
            "max_tokens": 2048
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
        except Exception as err:
            raise LLMProviderError(f"Network connection failed to OpenAI Vision API: {str(err)}")

        if response.status_code != 200:
            try:
                err_msg = response.json().get("error", {}).get("message", response.text)
            except Exception:
                err_msg = response.text
            raise LLMProviderError(f"OpenAI Vision API returned HTTP {response.status_code}: {err_msg}")

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError) as e:
            raise LLMProviderError(f"Failed to parse OpenAI Vision API response: {str(e)}")

