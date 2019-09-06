from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from snapshotUpdater import snapshotGetter

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(snapshotGetter.wakeup_self, 'interval', minutes=10)
    scheduler.add_job(snapshotGetter.new_Snapshot, 'interval', minutes=30)
    scheduler.start()
