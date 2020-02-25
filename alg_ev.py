# coding=utf-8

import time
import math
import numpy as np
import random

iterator = 1
mu = 0
sigma = 1
sat_max_time = 100

bsat_q = 0
bsat_v = 0
sun_size = 8
pl_size = 5
screen_size = width, height = 1000, 750
sun_weight = 200000.0
pl_weight = 6.0
sat_weight = 0.0001
g_const = 0.0416


def evolution(pl_list_pol, sat_list):

    min_f = 1000000.0

    start_time = random.uniform(5, 20)
    sat_q = random.uniform(0, 360)
    sat_v = random.uniform(10, 20)

    sat_list.append(sat_q)
    sat_list.append(sat_v)
    sat_list.append(start_time)

    n = 0
    omega = 1
    it = 2000

    b_list = []
    b_list.append(sat_q)
    b_list.append(sat_v)
    b_list.append(start_time)

    omega = []
    omega.append(2.5)
    omega.append(0.1)
    omega.append(0.1)

    s = []
    s.append(1)
    s.append(1)
    s.append(1)

    iter1 = 0
    iter2 = 0

    while it > 0:
        min_d = float(calculate(pl_list_pol, sat_list))
        if min_d < min_f:
            min_f = min_d
            b_list[iter1] = sat_list[iter1+4]
            s[iter1] = s[iter1]/b_list[iter1]

        if iter2 < 10:
            iter1 = 0
        if (iter2 > 9):
            iter1 = 1
        if iter2 == 21:
            iter1 = 2
            iter2 = 0

        rand = np.random.normal(mu, sigma, 1)

        if n == 100:
            for x in range(3):
                if s[x] < 0.2:
                    omega[x] = 0.82*omega[x]
                if s[x] > 0.2:
                    omega[x] = 1.2*omega[x]
                s[x] = 1

            n = 0

        sat_list[iter1+4] = b_list[iter1] + rand * omega[iter1]

        iter2 = iter2+1
        n = n+1
        it = it-1

        # print(min_f, min_d, b_list, omega)
    return(min_f, b_list[0], b_list[1], b_list[2])


def calculate(pl_list_pol, sat_list):
    sat_out = sat_list[0]
    sat_in = sat_list[1]

    sat_max_time = sat_list[3]
    sat_q = sat_list[4]
    sat_v = sat_list[5]
    start_time = sat_list[6]

    min_d = 100000

    for pl in pl_list_pol:
        pl[1] = pl[4] + start_time*pl[3]

    sat_x = (float)(pl_list_pol[sat_out-1][0] *
                    math.cos(math.radians(pl_list_pol[sat_out-1][1])) + width/2 + 0.1)
    sat_y = (float)(pl_list_pol[sat_out-1][0] *
                    math.sin(math.radians(pl_list_pol[sat_out-1][1])) + height/2 + 0.1)
    sat_v_x = sat_v * math.cos(math.radians(sat_q))
    sat_v_y = sat_v * math.sin(math.radians(sat_q))

    while sat_max_time > 0:

        force_x = 0.0
        force_y = 0.0

        d_x = (width/2)-sat_x
        d_y = (height/2)-sat_y
        if abs(d_x) <= 0.01 and abs(d_y) <= 0.01:
            print("ZDERZENIE")
            return min_d

        R = math.sqrt(d_x**2 + d_y**2)
        sat_sin = d_y/R
        sat_cos = d_x/R

        sat_force = (float)(sun_weight * g_const / (R**2))
        force_x = force_x + sat_cos*sat_force
        force_y = force_y + sat_sin*sat_force

        iterator = 1

        for pl in pl_list_pol:
            pl_x = (float)(pl[0] * math.cos(math.radians(pl[1])) + (width/2))
            pl_y = (float)(pl[0] * math.sin(math.radians(pl[1])) + (height/2))
            pl[1] = pl[1] + math.radians(pl[3])

            d_x = pl_x-sat_x
            d_y = pl_y-sat_y
            if abs(d_x) <= 0.000001 and abs(d_y) <= 0.000001:
                print("ZDERZENIE")
                return min_d

            R = math.sqrt(d_x**2 + d_y**2)
            if iterator == sat_in:
                if min_d > R:
                    min_d = R

            sat_sin = d_y/R
            sat_cos = d_x/R

            sat_force = (float)(pl_weight * g_const / (R**2))
            force_x = force_x + sat_cos*sat_force
            force_y = force_y + sat_sin*sat_force

            iterator = iterator+1
        sat_v_x += force_x
        sat_v_y += force_y
        sat_x += sat_v_x
        sat_y += sat_v_y

        if sat_x > 2000:
            return min_d
        if sat_x < -2000:
            return min_d
        if sat_y > 2000:
            return min_d
        if sat_y < -2000:
            return min_d

        sat_max_time = sat_max_time-1

    return min_d
