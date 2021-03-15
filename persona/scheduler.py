from apscheduler.schedulers.background import BackgroundScheduler
from .services.spotify import spotify_service


def create_scheduler():
    sched = BackgroundScheduler()
