import os
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager

# Use SQLite for persistent storage (better than in-memory for production)
DB_PATH = '/tmp/jobs.db'

@contextmanager
def db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database tables"""
    with db_connection() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            status TEXT,
            created_at TIMESTAMP,
            completed_at TIMESTAMP,
            results BLOB
        )
        ''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            job_id TEXT,
            url TEXT,
            status TEXT,
            message TEXT,
            PRIMARY KEY (job_id, url)
        )
        ''')
        conn.commit()

def store_job(job_id, data):
    """Store a new job in the database"""
    with db_connection() as conn:
        conn.execute('''
        INSERT INTO jobs (id, status, created_at)
        VALUES (?, ?, ?)
        ''', (job_id, 'pending', datetime.now()))
        conn.commit()

def get_job(job_id):
    """Get job details from database"""
    with db_connection() as conn:
        job_row = conn.execute('''
        SELECT id, status, created_at, completed_at, results
        FROM jobs WHERE id = ?
        ''', (job_id,)).fetchone()
        
        if not job_row:
            return None
        
        job = {
            'id': job_row[0],
            'status': job_row[1],
            'created_at': job_row[2],
            'completed_at': job_row[3],
            'results': job_row[4]
        }
        
        # Get progress details
        progress_rows = conn.execute('''
        SELECT url, status, message FROM progress
        WHERE job_id = ?
        ''', (job_id,)).fetchall()
        
        job['progress'] = {
            row[0]: {'status': row[1], 'message': row[2]}
            for row in progress_rows
        }
        
        return job

def update_job(job_id, message=None, url=None, status=None, overall_status=None, results=None):
    """Update job progress in database"""
    with db_connection() as conn:
        if url and status:
            conn.execute('''
            INSERT OR REPLACE INTO progress (job_id, url, status, message)
            VALUES (?, ?, ?, ?)
            ''', (job_id, url, status, message))
        
        if overall_status:
            conn.execute('''
            UPDATE jobs SET status = ? WHERE id = ?
            ''', (overall_status, job_id))
            
            if overall_status == 'completed':
                conn.execute('''
                UPDATE jobs SET completed_at = ? WHERE id = ?
                ''', (datetime.now(), job_id))
        
        if results:
            import json
            conn.execute('''
            UPDATE jobs SET results = ? WHERE id = ?
            ''', (json.dumps(results), job_id))
        
        conn.commit()

# Initialize database on import
init_db()
