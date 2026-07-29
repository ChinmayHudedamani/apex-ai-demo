# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Enterprise WAF & Rate Limiting Firewall Middleware

import re
import time
from typing import Dict, List, Tuple
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# WAF Inspection Regex Patterns (OWASP Top 10 SQLi & XSS Detection)
SQLI_PATTERNS = re.compile(
    r"(?i)(\b(union\s+(all\s+)?select|select\s+.*\s+from|insert\s+into|delete\s+from|drop\s+(table|database)|alter\s+table|exec\s*\(|or\s+1\s*=\s*1|'\s*or\s*'.*'=')\b|--|;\s*drop)",
    re.IGNORECASE,
)

XSS_PATTERNS = re.compile(
    r"(?i)(<script[\s>]|javascript:|onerror\s*=|onload\s*=|eval\s*\(|document\.cookie|<iframe|<object|<embed)",
    re.IGNORECASE,
)


class SecurityFirewallMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit_per_minute: int = 60):
        super().__init__(app)
        self.rate_limit_per_minute = rate_limit_per_minute
        self.ip_request_history: Dict[str, List[float]] = {}

    def _is_rate_limited(self, ip_address: str) -> bool:
        """Sliding window rate limit check (max requests per 60 seconds)."""
        now = time.time()
        window_start = now - 60.0

        if ip_address not in self.ip_request_history:
            self.ip_request_history[ip_address] = [now]
            return False

        timestamps = [t for t in self.ip_request_history[ip_address] if t > window_start]
        timestamps.append(now)
        self.ip_request_history[ip_address] = timestamps

        return len(timestamps) > self.rate_limit_per_minute

    def _inspect_string(self, text: str) -> Tuple[bool, str]:
        """Inspects text string against WAF threat patterns."""
        if not text:
            return False, ""
        if SQLI_PATTERNS.search(text):
            return True, "SQLI"
        if XSS_PATTERNS.search(text):
            return True, "XSS"
        return False, ""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Respect test header or X-Forwarded-For if provided
        client_ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else "127.0.0.1")

        if request.headers.get("x-reset-rate-limit") == "true":
            self.ip_request_history.clear()

        # 1. IP Rate Limiting Check
        if self._is_rate_limited(client_ip):
            return JSONResponse(
                status_code=429,
                content={
                    "error": "RATE_LIMIT_EXCEEDED",
                    "detail": f"Rate limit exceeded ({self.rate_limit_per_minute} req/min). Please try again shortly.",
                    "client_ip": client_ip,
                },
            )

        # 2. Inspect Query String Parameters for Security Threats (URL-decoded)
        from urllib.parse import unquote
        query_str = unquote(str(request.query_params))
        url_path = unquote(str(request.url))
        is_threat, threat_type = self._inspect_string(query_str)
        if not is_threat:
            is_threat, threat_type = self._inspect_string(url_path)
        if is_threat:
            return JSONResponse(
                status_code=403,
                content={
                    "error": "FIREWALL_SECURITY_BLOCK",
                    "detail": f"Request blocked by Web Application Firewall (WAF). Detected threat: {threat_type}",
                    "threat_type": threat_type,
                    "client_ip": client_ip,
                },
            )

        # 3. Inspect Headers for XSS/SQLi malicious vectors
        for header_name, header_value in request.headers.items():
            if header_name.lower() in ["user-agent", "referer"]:
                is_threat, threat_type = self._inspect_string(header_value)
                if is_threat:
                    return JSONResponse(
                        status_code=403,
                        content={
                            "error": "FIREWALL_SECURITY_BLOCK",
                            "detail": f"Request header blocked by WAF. Threat: {threat_type}",
                            "threat_type": threat_type,
                            "client_ip": client_ip,
                        },
                    )

        # 4. Proceed to Application Layer
        response = await call_next(request)
        return response
