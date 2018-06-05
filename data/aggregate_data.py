""" Code by Yoav Kaliblotzky"""

import pandas as pd
import numpy as np
from random import randint

data = pd.read_csv('output.csv')
'''
,id,game_id,owner_name,owner_is_human,owner_result,is_army,is_building,
is_worker,started_at,finished_at,died_at
'''

X = {'result': [], 'cutoff_time': [],
     'num_soldiers_built': [], 'num_soldiers_lost': [],
     'num_buildings_built': [], 'num_buildings_lost': [],
     'num_workers_built': [], 'num_workers_lost': [],
     'num_soldiers_destroyed': [], 'num_buildings_destroyed': [],
     'num_workers_destroyed': []}

data = data[np.isfinite(data['finished_at'])]

for game in range(1, 61):
    current_game = data[(data.game_id == game)]
    game_end = max(current_game[np.isfinite(data['died_at'])]['died_at'])
    cutoff_points = sorted([randint(0, int(((i + 1) / 3) * game_end))
                            for i in range(2)])
    cutoff_points.append(game_end)
    current_game = current_game.reset_index()
    count = 0
    p1 = []
    p2 = []
    for i in range(3):
        p1.append({})
        p2.append({})
        for x in X:
            p1[i][x] = 0
            p2[i][x] = 0
        p1[i]['cutoff_time'] = cutoff_points[i]
        p2[i]['cutoff_time'] = cutoff_points[i]

    # Player 1
    while str(current_game['owner_name'][count]) == 'nan':
        count += 1
    current_player = current_game['owner_name'][count]

    if current_game['owner_result'][count] == 'Win':
        for i in range(3):
            p1[i]['result'] = 1
            p2[i]['result'] = 0
    else:
        for i in range(3):
            p1[i]['result'] = 0
            p2[i]['result'] = 1

    while current_player == current_game['owner_name'][count]:
        max_bins = 0
        if current_game['finished_at'][count] < cutoff_points[0]:
            max_bins = 3
        elif current_game['finished_at'][count] < cutoff_points[1]:
            max_bins = 2
        else:
            max_bins = 1

        for j in range(max_bins):
            i = 2 - j
            if current_game['is_army'][count]:
                p1[i]['num_soldiers_built'] += 1
            elif current_game['is_worker'][count]:
                p1[i]['num_workers_built'] += 1
            else:
                p1[i]['num_buildings_built'] += 1

        if str(current_game['died_at'][count]) != 'nan':
            if current_game['died_at'][count] < cutoff_points[0]:
                max_bins = 3
            elif current_game['died_at'][count] < cutoff_points[1]:
                max_bins = 2
            else:
                max_bins = 1

            for j in range(max_bins):
                i = 2 - j
                if current_game['is_army'][count]:
                    p1[i]['num_soldiers_lost'] += 1
                    p2[i]['num_soldiers_destroyed'] += 1
                elif current_game['is_worker'][count]:
                    p1[i]['num_workers_lost'] += 1
                    p2[i]['num_workers_destroyed'] += 1
                else:
                    p1[i]['num_buildings_lost'] += 1
                    p2[i]['num_buildings_destroyed'] += 1
        count += 1

    # Player 2
    while str(current_game['owner_name'][count]) == 'nan':
        count += 1
    current_player = current_game['owner_name'][count]
    while count < current_game.shape[0]:
        max_bins = 0
        if current_game['finished_at'][count] < cutoff_points[0]:
            max_bins = 3
        elif current_game['finished_at'][count] < cutoff_points[1]:
            max_bins = 2
        else:
            max_bins = 1

        for j in range(max_bins):
            i = 2 - j
            if current_game['is_army'][count]:
                p2[i]['num_soldiers_built'] += 1
            elif current_game['is_worker'][count]:
                p2[i]['num_workers_built'] += 1
            else:
                p2[i]['num_buildings_built'] += 1

        if str(current_game['died_at'][count]) != 'nan':
            if current_game['died_at'][count] < cutoff_points[0]:
                max_bins = 3
            elif current_game['died_at'][count] < cutoff_points[1]:
                max_bins = 2
            else:
                max_bins = 1

            for j in range(max_bins):
                i = 2 - j
                if current_game['is_army'][count]:
                    p2[i]['num_soldiers_lost'] += 1
                    p1[i]['num_soldiers_destroyed'] += 1
                elif current_game['is_worker'][count]:
                    p2[i]['num_workers_lost'] += 1
                    p1[i]['num_workers_destroyed'] += 1
                else:
                    p2[i]['num_buildings_lost'] += 1
                    p1[i]['num_buildings_destroyed'] += 1
        count += 1
    for i in range(3):
        for x in X:
            X[x].append(p1[i][x])
            X[x].append(p2[i][x])


pd.DataFrame(X).to_csv('aggregate_data.csv')