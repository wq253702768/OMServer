#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import datetime


def date_calculation(start_time,end_time):
    '''

    :param start_time: begin time
    :param end_time:  end time
    :return: 4:30:00 4 hours 30 min
    '''
    s_time = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    e_time = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    if e_time > s_time:
        s_over_time = datetime.datetime(s_time[0],s_time[1],s_time[2],s_time[3],s_time[4])
        e_over_time = datetime.datetime(e_time[0],e_time[1],e_time[2],e_time[3],e_time[4])
        return (e_over_time - s_over_time)

    else:
        return False
