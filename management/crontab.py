from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from datetime import datetime
import time
import os


def asd():
    print(datetime.now())


# sche = BackgroundScheduler()
# sche.add_job(asd, 'cron', hour="5-23", second="*/10")
# print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))
#
#
#
#
# try:
#     sche.start()
# except (KeyboardInterrupt, SystemExit):
#     pass

def mian():
    sche = BackgroundScheduler()
    sche.add_job(asd, 'cron', hour="5-23", second="*/10")
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))

    try:
        sche.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    while (True):
        print('main 1s')
        time.sleep(1)

# if __name__ == '__main__':
#     sche = BackgroundScheduler()
#     sche.add_job(asd,'cron', hour="5-23", second="*/10")
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))
#
#     try:
#         sche.start()
#     except (KeyboardInterrupt, SystemExit):
#         pass
