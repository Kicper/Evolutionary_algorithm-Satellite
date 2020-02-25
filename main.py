# coding=utf-8

import pygame as pg
import time
import math
from alg_ev import evolution


screen_size = width, height = 1000, 750
sun_size = 8
pl_size = 5
sat_size = 3
sun_weight = 200000.0
pl_weight = 6.0
sat_weight = 0.0001
sun_col = r, g, b = 255, 255, 0
pl_col = r, g, b = 216, 13, 13
sat_col = r, g, b = 255, 255, 255
space_col = r, g, b = 0, 0, 0
g_const = 0.0416
time = 30


def add_object(pl_coor_x, pl_coor_y, pl_radius, color):
    pg.draw.circle(gameDisplay, color, [pl_coor_x, pl_coor_y], pl_radius)


def display(bstart_time):
    pg.display.set_caption('Satellite!')
    clock = pg.time.Clock()

    for pl in pl_list_pol:
        pl[1] = pl[4] + bstart_time*pl[3]
        pl_x = (float)(pl[0] * math.cos(math.radians(pl[1])) + (width/2))
        pl_y = (float)(pl[0] * math.sin(math.radians(pl[1])) + (height/2))
        pl[1] = pl[1] + math.radians(pl[3])

    sat_x = (float)(pl_list_pol[sat_out-1][0] *
                    math.cos(math.radians(pl_list_pol[sat_out-1][1])) + width/2 + 0.1)
    sat_y = (float)(pl_list_pol[sat_out-1][0] *
                    math.sin(math.radians(pl_list_pol[sat_out-1][1])) + height/2 + 0.1)
    sat_v_x = sat_v * math.cos(math.radians(sat_q))
    sat_v_y = sat_v * math.sin(math.radians(sat_q))

    running = True
    while running:

        gameDisplay.fill(space_col)
        add_object(width/2, height/2, 8, sun_col)   # sun
        force_x = 0.0
        force_y = 0.0

        d_x = (width/2)-sat_x
        d_y = (height/2)-sat_y
        if abs(d_x) <= 0.01 and abs(d_y) <= 0.01:
            print("ZDERZENIE")
            running = False
        R = math.sqrt(d_x**2 + d_y**2)
        sat_sin = d_y/R
        sat_cos = d_x/R

        sat_force = (float)(sun_weight * g_const / (R**2))
        force_x = force_x + sat_cos*sat_force
        force_y = force_y + sat_sin*sat_force

        for pl in pl_list_pol:
            pl_x = (float)(pl[0] * math.cos(math.radians(pl[1])) + (width/2))
            pl_y = (float)(pl[0] * math.sin(math.radians(pl[1])) + (height/2))
            pl[1] = pl[1] + math.radians(pl[3])
            add_object((int)(round(pl_x)), (int)(
                round(pl_y)), pl_size, pl_col)  # planets

            d_x = pl_x-sat_x
            d_y = pl_y-sat_y
            if abs(d_x) <= 0.000001 and abs(d_y) <= 0.000001:
                print("ZDERZENIE")
                running = False
            R = math.sqrt(d_x**2 + d_y**2)
            sat_sin = d_y/R
            sat_cos = d_x/R

            sat_force = (float)(pl_weight * g_const / (R**2))
            force_x = force_x + sat_cos*sat_force
            force_y = force_y + sat_sin*sat_force

        sat_v_x += force_x
        sat_v_y += force_y
        sat_x += sat_v_x
        sat_y += sat_v_y

        add_object((int)(round(sat_x)), (int)(round(sat_y)),
                   sat_size, sat_col)  # satellite

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        pg.display.update()
        clock.tick(time)


print("DATA ABOUT PLANETS")
prompt = input("How many planets you want to add: ")
pl_list_pol = []
for pl in range(prompt):
    pl_r = input("Enter distance from sun for " + str(pl + 1) + ". planet: ")
    pl_q = input("Enter angle to the sun for " + str(pl + 1) + ". planet: ")
    pl_v = (math.sqrt(g_const * sun_weight / pl_r))
    pl_q_change = pl_v
    pl_qc = pl_q
    pl_list_pol.append([pl_r, pl_q, pl_v, pl_q_change, pl_qc])

print("DATA ABOUT SATELLITE")
sat_list = []
sat_out = input("From which planet satellite will start: ")
sat_in = input("On which planet satellite will land: ")
sat_dist = input("Enter maximal final distance of satellite to planet: ")
sat_max_time = input("Enter maximal time for travel: ")
sat_list.append(sat_out)
sat_list.append(sat_in)
sat_list.append(sat_dist)
sat_list.append(sat_max_time)

b_d = 100000

find = False
for k in range(100):
    min_f, bsat_q, bsat_v, bstart_time = evolution(
        pl_list_pol, sat_list)
    if min_f < b_d:
        b_d = min_f
        b_q = bsat_q
        b_v = bsat_v
        b_s = bstart_time
    if min_f < sat_list[2]:
        find = True
        break

if find == False:
    print("Cannot find solution which fulfill settings")
else:
    print("Solution find!")

print("BEST SOLUTION:")
print("b_d: " + str(b_d) + "   bsat_q: " + str(bsat_q) +
      "   bsat_v: " + str(bsat_v) + "   bstart_time: " + str(bstart_time))

sat_q = b_q
sat_v = b_v
bstart_time = b_s

gameDisplay = pg.display.set_mode(screen_size)

pg.init()
display(bstart_time)
pg.quit()
quit()
