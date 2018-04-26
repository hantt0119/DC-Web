# coding:utf-8
import threading
import traceback

import schedule
import time,datetime

from django.db import connection
from sc_new.models import DefnSchd
from sc_new.util import validTLanuch


def run_schd(id, second):
    flag = True
    while flag:
        now = datetime.datetime.now()
        if now.second == second:
            flag = False
            try:
                print("run_schd%s" % (id))
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                cursor = connection.cursor()  # 获得一个游标(cursor)对象
                cursor.execute('select fnc_core_schd(%s)' % id)
            except:
                print('执行run_schd发生异常,id:%s' % (id))
                print(traceback.format_exc())


def run():
    schd_list = DefnSchd.objects.all()
    for m in schd_list:
        times = validTLanuch(m.t_launch)
        if times is not None:
            schedule.every().day.at('%s:%s' % (times[0], times[1])).do(run_schd, m.id, times[2])
    while True:
        schedule.run_pending()
        time.sleep(1)


sche_t = threading.Thread(target=run)
sche_t.start()