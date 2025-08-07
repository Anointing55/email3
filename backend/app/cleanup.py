import os
import glob
import time
from apscheduler.schedulers.background import BackgroundScheduler
from .storage import db_connection

def cleanup_old_files():
    """Delete temporary files older than 24 hours"""
    now = time.time()
    for file in glob.glob('/tmp/*'):
        if os.path.isfile(file) and now - os.stat(file).st_mtime > 86400:  # 24 hours
            try:
                os.remove(file)
            except Exception as e:
                print(f"Error deleting file {file}: {str(e)}")

def cleanup_old_jobs():
    """Delete jobs older than 7 days from database"""
    with db_connection() as conn:
        conn.execute('''
        DELETE FROM jobs 
        WHERE created_at < datetime('now', '-7 days')
        ''')
        conn.execute('''
        DELETE FROM progress
        WHERE job_id NOT IN (SELECT id FROM jobs)
        ''')
        conn.commit()

def setup_scheduler():
    """Setup scheduled cleanup tasks"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_old_files, 'interval', hours=1)
    scheduler.add_job(cleanup_old_jobs, 'interval', hours=24)
    scheduler.start()
