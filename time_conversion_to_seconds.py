""" Time conversions to seconds for the main program """

import time

def __subtract_time( t_des: str, t_cur: str ) -> str:
    """ Subtracts time: desired_time - current_time """

    __list_size = 3

    t_des = t_des + ":00"

    cur_list = t_cur.split(':')
    des_list = t_des.split(':')
    new_list = [0, 0, 0] # [hour, minute, second]
    new_list_str = ['', '', '']

    # convert everything in lists from strings to integers ([h,m,s] format)
    for i in range(__list_size):
        cur_list[i] = int(cur_list[i])
        des_list[i] = int(des_list[i])

    # subtract seconds first
    if(cur_list[2] > des_list[2]): # if current second value is greater than desired
        des_list[2] = 60 - cur_list[2]
        cur_list[1] += 1 # incremet minute after surpassing seconds

        if(cur_list[1] == 60): # fix min
            cur_list[1] = 0
            cur_list[0] += 1
            if(cur_list[0] == 24): # fix hour
                cur_list[0] = 0
    else:
        des_list[2] = des_list[2] - cur_list[2] # subtracting desired with current times

    # subtract minutes
    if(cur_list[1] > des_list[1]):
        des_list[1] = 60 - cur_list[1]
        cur_list[0] += 1

        if(cur_list[0] == 24):
            cur_list[0] = 0
    else:
        des_list[1] = des_list[1] - cur_list[1]

    # subtract hours
    if(cur_list[0] > des_list[0]):
        des_list[0] = 24 - cur_list[0]
    else:
        des_list[0] = des_list[0] - cur_list[0]

    # make sure 24 means 0
    if(new_list[0] == 24):
            new_list[0] = 0

    new_list = des_list.copy()

    # convert new_list to string
    for i in range(len(new_list)):
        if(new_list[i] < 10):
            new_list_str[i] = '0' + str(new_list[i])
        else:
            new_list_str[i] = str(new_list[i])

    # construct string in hh:mm:ss format
    return new_list_str[0] + ':' + new_list_str[1] + ':' + new_list_str[2]


def __get_sec(time_str: str) -> int:
    """ Obtains seconds from a string in the HH:MM:SS format """

    h, m, s = time_str.split(':')

    return int(h) * 3600 + int(m) * 60 + int(s)


def schedule_time(time_str: str, time_str_current = time.strftime('%X')) -> int:
    """ Returns calculations using __subtract_time and __get_sec. Intended to be used for time-scheduling purposes. """

    final_time = __get_sec(__subtract_time(time_str, time_str_current))

    return final_time
