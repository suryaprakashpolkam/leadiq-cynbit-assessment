import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///leadiq.db")
_engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    with _engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS inquiry_analyses (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                inquiry_text TEXT NOT NULL,
                service_category VARCHAR(100),
                readiness VARCHAR(100),
                urgency VARCHAR(30),
                analysis_json TEXT,
                created_at VARCHAR(40)
            )
        """) if DATABASE_URL.startswith("mysql") else text("""
            CREATE TABLE IF NOT EXISTS inquiry_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inquiry_text TEXT NOT NULL,
                service_category TEXT,
                readiness TEXT,
                urgency TEXT,
                analysis_json TEXT,
                created_at TEXT
            )
        """))

def save_analysis(inquiry_text, analysis, readiness):
    init_db()
    import json
    with _engine.begin() as conn:
        result = conn.execute(text("""
            INSERT INTO inquiry_analyses
            (inquiry_text, service_category, readiness, urgency, analysis_json, created_at)
            VALUES (:inquiry, :category, :readiness, :urgency, :payload, :created)
        """), {
            "inquiry": inquiry_text,
            "category": analysis.service_category,
            "readiness": readiness["readiness"],
            "urgency": analysis.urgency,
            "payload": analysis.model_dump_json(),
            "created": datetime.now(timezone.utc).isoformat()
        })
        return result.lastrowid

def list_analyses(limit=50):
    init_db()
    with _engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, service_category, readiness, urgency, created_at
            FROM inquiry_analyses ORDER BY id DESC LIMIT :limit
        """), {"limit": limit}).mappings().all()
    return [dict(row) for row in rows]
