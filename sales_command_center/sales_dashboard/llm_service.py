"""
LLM Fallback Service
Implements a robust fallback strategy across multiple LLM providers:
1. Euri AI (Primary)
2. DeepSeek (Secondary)
3. Google Gemini (Tertiary)

If one provider fails, automatically falls back to the next available provider.
"""

import os
import logging
import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from enum import Enum
import json

import httpx

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers"""
    EURI = "euri"
    DEEPSEEK = "deepseek"
    GOOGLE = "google"
    OPENAI = "openai"  # Fallback option
    ANTHROPIC = "anthropic"  # Fallback option


@dataclass
class LLMConfig:
    """Configuration for an LLM provider"""
    provider: LLMProvider
    api_key: str
    model: str
    base_url: Optional[str] = None
    max_tokens: int = 2000
    temperature: float = 0.7
    timeout: int = 30
    enabled: bool = True


@dataclass
class LLMResponse:
    """Standardized response from LLM"""
    content: str
    provider: LLMProvider
    model: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[float] = None
    success: bool = True
    error: Optional[str] = None


class LLMFallbackService:
    """
    LLM Service with automatic fallback between providers.

    Priority order:
    1. Euri AI
    2. DeepSeek
    3. Google Gemini
    4. OpenAI (if configured)
    5. Anthropic (if configured)
    """

    # Provider configurations
    PROVIDER_CONFIGS = {
        LLMProvider.EURI: {
            "base_url": "https://api.euron.one/api/v1",  # Euri AI API endpoint
            "default_model": "euri-text-1",
            "chat_endpoint": "/chat/completions"
        },
        LLMProvider.DEEPSEEK: {
            "base_url": "https://api.deepseek.com/v1",
            "default_model": "deepseek-chat",
            "chat_endpoint": "/chat/completions"
        },
        LLMProvider.GOOGLE: {
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
            "default_model": "gemini-1.5-flash",
            "chat_endpoint": "/models/{model}:generateContent"
        },
        LLMProvider.OPENAI: {
            "base_url": "https://api.openai.com/v1",
            "default_model": "gpt-4-turbo-preview",
            "chat_endpoint": "/chat/completions"
        },
        LLMProvider.ANTHROPIC: {
            "base_url": "https://api.anthropic.com/v1",
            "default_model": "claude-3-sonnet-20240229",
            "chat_endpoint": "/messages"
        }
    }

    def __init__(self):
        """Initialize the LLM Fallback Service"""
        self.providers: List[LLMConfig] = []
        self._http_client = httpx.Client(timeout=60)
        self._load_providers()

        logger.info(f"LLM Fallback Service initialized with {len(self.providers)} providers")
        for p in self.providers:
            logger.info(f"  - {p.provider.value}: {p.model} (enabled: {p.enabled})")

    def _load_providers(self):
        """Load provider configurations from environment variables"""

        # 1. Euri AI (Primary)
        euri_key = os.getenv("EURI_API_KEY")
        if euri_key:
            self.providers.append(LLMConfig(
                provider=LLMProvider.EURI,
                api_key=euri_key,
                model=os.getenv("EURI_MODEL", "euri-text-1"),
                base_url=os.getenv("EURI_BASE_URL", self.PROVIDER_CONFIGS[LLMProvider.EURI]["base_url"]),
                max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7"))
            ))

        # 2. DeepSeek (Secondary)
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key:
            self.providers.append(LLMConfig(
                provider=LLMProvider.DEEPSEEK,
                api_key=deepseek_key,
                model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
                base_url=os.getenv("DEEPSEEK_BASE_URL", self.PROVIDER_CONFIGS[LLMProvider.DEEPSEEK]["base_url"]),
                max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7"))
            ))

        # 3. Google Gemini (Tertiary)
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key:
            self.providers.append(LLMConfig(
                provider=LLMProvider.GOOGLE,
                api_key=google_key,
                model=os.getenv("GOOGLE_MODEL", "gemini-1.5-flash"),
                base_url=os.getenv("GOOGLE_BASE_URL", self.PROVIDER_CONFIGS[LLMProvider.GOOGLE]["base_url"]),
                max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7"))
            ))

        # 4. OpenAI (Fallback)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.providers.append(LLMConfig(
                provider=LLMProvider.OPENAI,
                api_key=openai_key,
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
                base_url=self.PROVIDER_CONFIGS[LLMProvider.OPENAI]["base_url"],
                max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7"))
            ))

        # 5. Anthropic (Fallback)
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.providers.append(LLMConfig(
                provider=LLMProvider.ANTHROPIC,
                api_key=anthropic_key,
                model=os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
                base_url=self.PROVIDER_CONFIGS[LLMProvider.ANTHROPIC]["base_url"],
                max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7"))
            ))

        if not self.providers:
            logger.warning("No LLM providers configured! Set at least one API key.")

    def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None,
        preferred_provider: Optional[LLMProvider] = None
    ) -> LLMResponse:
        """
        Send a chat message with automatic fallback.

        Args:
            user_message: The user's message
            system_prompt: Optional system prompt
            context: Optional context to include
            preferred_provider: Optional preferred provider to try first

        Returns:
            LLMResponse with the result
        """
        if not self.providers:
            return LLMResponse(
                content="No LLM providers configured. Please set API keys in environment.",
                provider=LLMProvider.EURI,
                model="none",
                success=False,
                error="No providers configured"
            )

        # Build the full message
        full_message = user_message
        if context:
            full_message = f"Context:\n{context}\n\nQuery: {user_message}"

        # Reorder providers if preferred provider specified
        providers_to_try = self.providers.copy()
        if preferred_provider:
            providers_to_try.sort(
                key=lambda p: 0 if p.provider == preferred_provider else 1
            )

        # Try each provider in order
        errors = []
        for config in providers_to_try:
            if not config.enabled:
                continue

            try:
                logger.info(f"Trying LLM provider: {config.provider.value}")
                start_time = time.time()

                response = self._call_provider(config, full_message, system_prompt)

                latency = (time.time() - start_time) * 1000
                logger.info(f"Success with {config.provider.value} in {latency:.0f}ms")

                return LLMResponse(
                    content=response,
                    provider=config.provider,
                    model=config.model,
                    latency_ms=latency,
                    success=True
                )

            except Exception as e:
                error_msg = f"{config.provider.value}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"Provider {config.provider.value} failed: {e}")
                continue

        # All providers failed
        return LLMResponse(
            content="I apologize, but I'm unable to process your request at the moment. Please try again later.",
            provider=self.providers[0].provider if self.providers else LLMProvider.EURI,
            model="fallback",
            success=False,
            error="; ".join(errors)
        )

    def _call_provider(
        self,
        config: LLMConfig,
        message: str,
        system_prompt: Optional[str]
    ) -> str:
        """Call a specific LLM provider"""

        if config.provider == LLMProvider.EURI:
            return self._call_euri(config, message, system_prompt)
        elif config.provider == LLMProvider.DEEPSEEK:
            return self._call_deepseek(config, message, system_prompt)
        elif config.provider == LLMProvider.GOOGLE:
            return self._call_google(config, message, system_prompt)
        elif config.provider == LLMProvider.OPENAI:
            return self._call_openai(config, message, system_prompt)
        elif config.provider == LLMProvider.ANTHROPIC:
            return self._call_anthropic(config, message, system_prompt)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")

    def _call_euri(
        self,
        config: LLMConfig,
        message: str,
        system_prompt: Optional[str]
    ) -> str:
        """Call Euri AI API (OpenAI-compatible)"""
        url = f"{config.base_url}/chat/completions"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        response = self._http_client.post(
            url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": config.model,
                "messages": messages,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature
            },
            timeout=config.timeout
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _call_deepseek(
        self,
        config: LLMConfig,
        message: str,
        system_prompt: Optional[str]
    ) -> str:
        """Call DeepSeek API (OpenAI-compatible)"""
        url = f"{config.base_url}/chat/completions"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        response = self._http_client.post(
            url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": config.model,
                "messages": messages,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature
            },
            timeout=config.timeout
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _call_google(
        self,
        config: LLMConfig,
        message: str,
        system_prompt: Optional[str]
    ) -> str:
        """Call Google Gemini API"""
        url = f"{config.base_url}/models/{config.model}:generateContent"

        # Build content parts
        contents = []
        if system_prompt:
            contents.append({
                "role": "user",
                "parts": [{"text": f"System Instructions: {system_prompt}"}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Understood. I will follow these instructions."}]
            })

        contents.append({
            "role": "user",
            "parts": [{"text": message}]
        })

        response = self._http_client.post(
            url,
            headers={"Content-Type": "application/json"},
            params={"key": config.api_key},
            json={
                "contents": contents,
                "generationConfig": {
                    "maxOutputTokens": config.max_tokens,
                    "temperature": config.temperature
                }
            },
            timeout=config.timeout
        )
        response.raise_for_status()

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def _call_openai(
        self,
        config: LLMConfig,
        message: str,
        system_prompt: Optional[str]
    ) -> str:
        """Call OpenAI API"""
        url = f"{config.base_url}/chat/completions"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        response = self._http_client.post(
            url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": config.model,
                "messages": messages,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature
            },
            timeout=config.timeout
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _call_anthropic(
        self,
        config: LLMConfig,
        message: str,
        system_prompt: Optional[str]
    ) -> str:
        """Call Anthropic Claude API"""
        url = f"{config.base_url}/messages"

        payload = {
            "model": config.model,
            "max_tokens": config.max_tokens,
            "messages": [{"role": "user", "content": message}]
        }

        if system_prompt:
            payload["system"] = system_prompt

        response = self._http_client.post(
            url,
            headers={
                "x-api-key": config.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=config.timeout
        )
        response.raise_for_status()

        data = response.json()
        return data["content"][0]["text"]

    def get_available_providers(self) -> List[str]:
        """Get list of configured providers"""
        return [p.provider.value for p in self.providers if p.enabled]

    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        return {
            "providers": [
                {
                    "name": p.provider.value,
                    "model": p.model,
                    "enabled": p.enabled
                }
                for p in self.providers
            ],
            "total_configured": len(self.providers),
            "fallback_order": [p.provider.value for p in self.providers]
        }

    def __del__(self):
        """Cleanup HTTP client"""
        if hasattr(self, '_http_client'):
            self._http_client.close()


# Global instance for easy access
_llm_service: Optional[LLMFallbackService] = None


def get_llm_service() -> LLMFallbackService:
    """Get the global LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMFallbackService()
    return _llm_service


def chat_with_fallback(
    message: str,
    system_prompt: Optional[str] = None,
    context: Optional[str] = None
) -> str:
    """
    Convenience function for quick LLM calls with fallback.

    Args:
        message: The user message
        system_prompt: Optional system prompt
        context: Optional context

    Returns:
        The LLM response content
    """
    service = get_llm_service()
    response = service.chat(message, system_prompt, context)
    return response.content
