# Copyright (c) 2026 Chinmay Hudedamani. All Rights Reserved.
# APEX AI / Copus AI — 15-Minute Doctor Status Scheduler Engine

import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal
from app.models.pro_tier import DoctorStatusLog

logger = logging.getLogger(__name__)

# Default in-memory cache for fast lookups
DOCTOR_STATUS_CACHE = {
    "dr-chinmay": {
        "id": "dr-chinmay",
        "name": "Dr. Chinmay Hudedamani",
        "status": "AVAILABLE",
        "est_completion_mins": 0,
        "last_updated": datetime.utcnow().isoformat()
    },
    "dr-ananya": {
        "id": "dr-ananya",
        "name": "Dr. Ananya Rao",
        "status": "IN_SURGERY",
        "est_completion_mins": 45,
        "last_updated": datetime.utcnow().isoformat()
    },
    "dr-vikram": {
        "id": "dr-vikram",
        "name": "Dr. Vikramaditya Hegde",
        "status": "ON_BREAK",
        "est_completion_mins": 15,
        "last_updated": datetime.utcnow().isoformat()
    }
}

scheduler = BackgroundScheduler()


def run_15min_status_update():
    """Worker task executed every 15 minutes by APScheduler."""
    logger.info("Executing 15-minute Doctor Status Update job...")
    db = SessionLocal()
    try:
        now_str = datetime.utcnow().isoformat()
        for doc_id, doc in DOCTOR_STATUS_CACHE.items():
            current_est = doc.get("est_completion_mins", 0)
            if doc["status"] in ["IN_SURGERY", "ON_BREAK"] and current_est > 0:
                new_est = max(0, current_est - 15)
                doc["est_completion_mins"] = new_est
                if new_est == 0:
                    doc["status"] = "AVAILABLE"
                doc["last_updated"] = now_str

            # Log to DB
            log_entry = DoctorStatusLog(
                doctor_id=doc_id,
                doctor_name=doc["name"],
                current_status=doc["status"],
                est_completion_mins=doc["est_completion_mins"],
                last_updated=datetime.utcnow()
            )
            db.add(log_entry)

        db.commit()
        logger.info("15-minute Doctor Status successfully updated and logged.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error in 15min doctor status update job: {e}")
    finally:
        db.close()


def update_doctor_status_manually(doc_id: str, new_status: str, est_mins: int = 0):
    """Manually update doctor status from API or OT override."""
    if doc_id in DOCTOR_STATUS_CACHE:
        doc = DOCTOR_STATUS_CACHE[doc_id]
        doc["status"] = new_status
        doc["est_completion_mins"] = est_mins
        doc["last_updated"] = datetime.utcnow().isoformat()

        db = SessionLocal()
        try:
            log_entry = DoctorStatusLog(
                doctor_id=doc_id,
                doctor_name=doc["name"],
                current_status=new_status,
                est_completion_mins=est_mins,
                last_updated=datetime.utcnow()
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to persist manual status update: {e}")
        finally:
            db.close()
        return doc
    return None


def get_all_doctor_statuses():
    """Retrieve current doctor status list."""
    return list(DOCTOR_STATUS_CACHE.values())


def start_doctor_status_scheduler():
    """Starts the background APScheduler for 15-minute status updates."""
    if not scheduler.running:
        scheduler.add_job(
            run_15min_status_update,
            'interval',
            minutes=15,
            id='doctor_15min_status_job',
            replace_existing=True
        )
        scheduler.start()
        logger.info("APScheduler Doctor Status Engine started successfully.")
