# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Security Firewall Automated Tests

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_owasp_security_headers_present():
    """Test that OWASP security headers are present on every response."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert "max-age=" in response.headers.get("Strict-Transport-Security", "")
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


def test_waf_blocks_sqli_in_query_params():
    """Test WAF blocks SQL injection payloads in query parameters."""
    response = client.get("/api/v1/doctors?search=' OR 1=1 --")
    assert response.status_code == 403
    data = response.json()
    assert data["error"] == "FIREWALL_SECURITY_BLOCK"
    assert data["threat_type"] == "SQLI"


def test_waf_blocks_union_select_injection():
    """Test WAF blocks UNION SELECT injection."""
    response = client.get("/api/v1/doctors?q=1 UNION SELECT * FROM users")
    assert response.status_code == 403
    assert response.json()["threat_type"] == "SQLI"


def test_waf_blocks_drop_table_injection():
    """Test WAF blocks DROP TABLE injection."""
    response = client.get("/api/v1/doctors?q=; DROP TABLE users")
    assert response.status_code == 403
    assert response.json()["threat_type"] == "SQLI"


def test_waf_blocks_xss_script_tag():
    """Test WAF blocks XSS <script> tag payloads in query parameters."""
    response = client.get("/api/v1/doctors?search=<script>alert(1)</script>")
    assert response.status_code == 403
    data = response.json()
    assert data["error"] == "FIREWALL_SECURITY_BLOCK"
    assert data["threat_type"] == "XSS"


def test_waf_blocks_xss_onerror():
    """Test WAF blocks XSS onerror attribute injection."""
    response = client.get('/api/v1/doctors?name=<img onerror="alert(1)">')
    assert response.status_code == 403
    assert response.json()["threat_type"] == "XSS"


def test_waf_blocks_xss_javascript_protocol():
    """Test WAF blocks javascript: protocol injection."""
    response = client.get("/api/v1/doctors?url=javascript:alert(1)")
    assert response.status_code == 403
    assert response.json()["threat_type"] == "XSS"


def test_waf_allows_clean_requests():
    """Test WAF allows clean, safe requests through."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"


def test_waf_allows_normal_api_call():
    """Test WAF allows normal API call with no malicious payload."""
    response = client.get("/api/v1/doctors")
    assert response.status_code == 200


def test_rate_limiter_blocks_excessive_requests():
    """Test IP rate limiter blocks requests after exceeding threshold."""
    # Use a fresh TestClient to get clean rate limit state
    from app.main import app as fresh_app
    test_client = TestClient(fresh_app)

    # Send 61 requests rapidly (limit is 60/min)
    blocked = False
    for i in range(65):
        resp = test_client.get("/health")
        if resp.status_code == 429:
            blocked = True
            data = resp.json()
            assert data["error"] == "RATE_LIMIT_EXCEEDED"
            break

    assert blocked, "Rate limiter did not block after 60+ requests"
