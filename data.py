
import pandas as pd
from helper import get_all_players, get_P_q, get_Q_p, get_scores, get_prices

def get_sets_and_data(year):

    files = {"2018": "../Datasets/Combined Data/combined_data_2018_final.csv",
             "2021": "../Datasets/Combined Data/combined_data_2021_final.csv"}
    
    # dataframe
    data = pd.read_csv(files[year])
    
    ##------------------------------ SETS -----------------------------------##
    
    # set of all players
    P = get_all_players(data)
    
    # set of scoring positions
    Q_score = ['DEF','MID','RUC','FWD']
    
    # set of substitute positions
    Q_sub = ['DEF_sub','MID_sub','RUC_sub','FWD_sub']
    
    # set of all positions
    Q = Q_score + Q_sub
    
    # set of all players p who can play in each position q
    P_q = get_P_q(data, P, Q)
    
    # set of all positions q each player p can play
    Q_p = get_Q_p(data, P, Q)
    
    # set of all rounds
    R = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
         10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
         20, 21, 22]

    ##------------------------------ DATA -----------------------------------##
    
    # score of player p in round r
    psi = get_scores(P,R,data)
    
    # price of player p in round r
    v = get_prices(P,R,data)
    
    # number of available spots in position q
    C_q = {'DEF': 6,    'MID': 8,    'RUC':2,     'FWD': 6,
           'DEF_sub':2, 'MID_sub':3, 'RUC_sub':1, 'FWD_sub':2}
    
    # set of slots available in each position
    S_q = {'DEF': [0, 1, 2, 3, 4, 5], 'DEF_sub': [0, 1],
                 'MID': [0, 1, 2, 3, 4, 5, 6, 7], 'MID_sub': [0, 1, 2],
                 'RUC': [0, 1], 'RUC_sub': [0],
                 'FWD': [0, 1, 2, 3, 4, 5], 'FWD_sub': [0, 1]}
    
    # number of players whose scores count towards the score of the team, in round r
    X_r = [22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
           22, 18, 18, 18, 22, 22, 22, 22, 22, 22,
           22, 22, 22]
    
    # maximum number of trades that can be used in round r
    T_r = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
           2, 3, 3, 3, 2, 2, 2, 2, 2, 2,
           2, 2, 2]
    
    # maximum number of trades that can be used across the season
    T_total = 30
    
    # starting budget for the season
    B = 10000000
    
    # winning score for the 2018 season
    winning_scores = {'2018': 53852,
                      '2021': 53859}
    S_win = winning_scores[year]
    
    # maximum number of emergencies per round
    E = 4
    
    ##------------------------------ RETURN ---------------------------------##
    
    return (P, Q_score, Q_sub, Q, P_q, Q_p, R, 
            psi, v, C_q, S_q, X_r, T_r, T_total, B, S_win, E)