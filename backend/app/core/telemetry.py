# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — Error Monitoring & Sentry Telemetry SDK Initialization

import os
from app.core.logging import logger

SENTRY_DSN = os.getenv("SENTRY_DSN", "")


def init_telemetry():
    """Initializes Sentry Error Monitoring SDK if DSN is configured."""
    if not SENTRY_DSN:
        logger.info("SENTRY_DSN not set. Running in local exception logging mode.")
        return

    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            environment=os.getenv("ENVIRONMENT", "production"),
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
            integrations=[
                FastApiIntegration(transaction_style="endpoint"),
                SqlalchemyIntegration(),
            ],
            send_default_pii=False,
        )
        logger.info("Sentry Telemetry SDK initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Sentry Telemetry SDK: {e}")
