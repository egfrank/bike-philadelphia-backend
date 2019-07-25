from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from snapshotUpdater import snapshotGetter

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(snapshotGetter.new_Snapshot, 'interval', minutes=30)
    scheduler.start()
