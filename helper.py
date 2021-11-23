
##------------------------------SETS-----------------------------------------##

def get_all_players(data):
    return data["player"].values

# get all players who can play in each position
def get_P_q(data, P, Q):
    P_q = {}
    for q in Q:
        P_q[q] = []
    for p in P:
        positions = data[data.player==p]['position'].values[0].split(' ')
        for position in positions:
            P_q[position].append(p)
            P_q[position + '_sub'].append(p)
    return P_q

def get_Q_p(data, P, Q):
    Q_p = {}
    for p in P:
        Q_p[p] = []
        positions = data[data.player==p]['position'].values[0].split(' ')
        for position in positions:
            Q_p[p].append(position)
            Q_p[p].append(position + "_sub")
    return Q_p

##------------------------------DATA-----------------------------------------##

def get_scores(P, R, data):
    scores = {}
    for p in P:
        for r in R:
            round_num_str = 'r' + str(r+1) + '_score'
            score = data[data["player"]==p][round_num_str].values[0]
            scores[p,r] = score
    return scores

def get_prices(P, R, data):
    prices = {}
    for p in P:
        for r in R:
            round_num_str = 'r' + str(r+1) + '_price'
            price = data[data["player"]==p][round_num_str].values[0]
            prices[p,r] = price
    return prices

##------------------------------PRINT SOLUTIONS------------------------------##

def print_optimal_solution(m, 
                           P, P_q, R, Q_score, Q_sub, 
                           x, x_bar, t_in, t_out, b_r, c, psi):

    # print total score
    print("\nTotal score:")
    print(m.objVal)

    for r in R:
    
        print("\n---------- Round",r+1," ----------")    
        
        # print the players who have been traded in
        print("\nPlayers Traded In:")
        for p in P:
            if (r > 0) and (t_in[p,r].x >= 0.99):
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print the players who have been traded out
        print("\nPlayers Traded Out:")
        for p in P:
            if (r > 0) and (t_out[p,r].x >= 0.99):
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print remaining budget
        print("\nRemaining Budget:")
        print(b_r[r].x)
        
        # print captain selection each round
        print("\nCaptain:")
        for p in P:
            if c[p,r].x >= 0.99:
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print the players who have been selected in scoring positions
        print("\nSelected Scoring Players:")
        for q in Q_score:
            for p in P_q[q]:
                if x[p,q,r].x >= 0.99:
                    print("{0:12s} {1:12s} {2:7s} {3:5d} {4:2d}".format(
                        p.split('_')[0],p.split('_')[1],
                        q,psi[p,r],round(x_bar[p,r].x)))
                    
        # print the players who have been selected in substitute positions
        print("\nSelected Substitute Players:")
        for q in Q_sub:
            for p in P_q[q]:
                if x[p,q,r].x >= 0.99:
                    print("{0:12s} {1:12s} {2:7s} {3:5d} {4:2d}".format(
                        p.split('_')[0],p.split('_')[1],
                        q,psi[p,r],round(x_bar[p,r].x)))

def print_optimal_scores(m, 
                           P, P_q, R, Q_score, Q_sub, 
                           x, x_bar, t_in, t_out, b_r, c, psi):
    
    cumulative_score = 0
    
    for r in R:
    
        print("\n---------- Round",r+1," ----------")    
        
        # print the players who have been traded in
        print("\nPlayers Traded In:")
        for p in P:
            if (r > 0) and (t_in[p,r].x >= 0.99):
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print the players who have been traded out
        print("\nPlayers Traded Out:")
        for p in P:
            if (r > 0) and (t_out[p,r].x >= 0.99):
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print remaining budget
        print("\nRemaining Budget:")
        print(b_r[r].x)
        
        # print captain selection each round
        print("\nCaptain:")
        for p in P:
            if c[p,r].x >= 0.99:
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
    
        # print the score for the round
        print("\nRound Score:")
        round_score = 0
        for p in P:
            round_score += psi[p,r]*(x_bar[p,r].x + c[p,r].x)
        print(round_score)
        
        # print the cumulative score
        print("\nCumulative Score:")
        cumulative_score += round_score
        print(cumulative_score)

def print_budget_solution(m, P, Q, Q_score, Q_sub, P_q, Q_p, R, 
                           x, x_bar, t_in, t_out, b_r, c, psi):

    # print the minimum budget
    print("\nMinimum Budget:")
    print(m.objVal)

    for r in R:
    
        print("\n---------- round",r+1," ----------")    
        
        # print the players who have been traded in
        print("\nPlayers Traded In:")
        for p in P:
            if (r > 0) and (t_in[p,r].x >= 0.99):
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print the players who have been traded out
        print("\nPlayers Traded Out:")
        for p in P:
            if (r > 0) and (t_out[p,r].x >= 0.99):
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print remaining budget
        print("\nRemaining Budget:")
        print(b_r[r].x)
        
        # print captain selection each round
        print("\nCaptain:")
        for p in P:
            if c[p,r].x >= 0.99:
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print the players who have been selected in scoring positions
        print("\nSelected Scoring Players:")
        for q in Q_score:
            for p in P_q[q]:
                if x[p,q,r].x >= 0.99:
                    print("{0:12s} {1:12s} {2:7s} {3:5d} {4:2d}".format(
                        p.split('_')[0],p.split('_')[1],
                        q,psi[p,r],round(x_bar[p,r].x)))
                    
        # print the players who have been selected in substitute positions
        print("\nSelected Substitute Players:")
        for q in Q_sub:
            for p in P_q[q]:
                if x[p,q,r].x >= 0.99:
                    print("{0:12s} {1:12s} {2:7s} {3:5d} {4:2d}".format(
                        p.split('_')[0],p.split('_')[1],
                        q,psi[p,r],round(x_bar[p,r].x)))

def print_budget_scores(m, 
                           P, P_q, R, Q_score, Q_sub, 
                           x, x_bar, t_in, t_out, b_r, c, psi):
    
    cumulative_score = 0
    
    for r in R:
    
        print("\n---------- Round",r+1," ----------")    
        
        # print the players who have been traded in
        print("\nPlayers Traded In:")
        for p in P:
            if (r > 0) and (t_in[p,r].x >= 0.99):
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print the players who have been traded out
        print("\nPlayers Traded Out:")
        for p in P:
            if (r > 0) and (t_out[p,r].x >= 0.99):
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print remaining budget
        print("\nRemaining Budget:")
        print(b_r[r].x)
        
        # print captain selection each round
        print("\nCaptain:")
        for p in P:
            if c[p,r].x >= 0.99:
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
    
        # print the score for the round
        print("\nRound Score:")
        round_score = 0
        for p in P:
            round_score += psi[p,r]*(x_bar[p,r].x + c[p,r].x)
        print(round_score)
        
        # print the cumulative score
        print("\nCumulative Score:")
        cumulative_score += round_score
        print(cumulative_score)

def print_ghost_solution(m, P, Q, Q_score, Q_sub, P_q, Q_p, x, c_cap, c_vice, e, v):

    # print total score
    print("\nTotal Score:")
    print(m.objVal)
        
    # print captain selection
    print("\nCaptain:")
    for p in P:
        if c_cap[p].x >= 0.5:
            print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
    
    # print vice-captain selection
    print("\nVice-Captain:")
    for p in P:
        if c_vice[p].x >= 0.5:
            print("{0:12s} {1:12s}".format(
                p.split('_')[0],p.split('_')[1]))
    
    # print initial team value
    print("\nInitial Team Value:")
    total = 0
    for p in P:
        for q in Q_p[p]:
            total += v[p,0]*x[p,q].x
    print(round(total))
    
    # print the players who have been selected in scoring positions
    print("\nSelected Scoring Players:")
    for q in Q_score:
        for p in P_q[q]:
            if x[p,q].x >= 0.5:
                print("{0:12s} {1:12s} {2:7s}".format(
                    p.split('_')[0],p.split('_')[1],q))
                    
    # print the players who have been selected in substitute positions
    print("\nSelected Substitute Players:")
    for q in Q_sub:
        for p in P_q[q]:
            if x[p,q].x >= 0.5:
                print("{0:12s} {1:12s} {2:7s} {3:2d}".format(
                    p.split('_')[0],p.split('_')[1],q,round(e[p,q].x)))
                
def print_ghost_scores(P, Q_p, R, psi, v, x, x_bar, c_cap, c_vice_bar, B):
    
    cumulative_score = 0
    
    team_value = 0
    for p in P:
        for q in Q_p[p]:
            team_value += v[p,0]*x[p,q].x
    
    for r in R:
    
        print("\n---------- Round",r+1," ----------")    
                
        # print remaining budget
        print("\nRemaining Budget:")
        print(B - team_value)
        
        # print captain selection each round
        for p in P:
            if (c_cap[p].x >= 0.99 and psi[p,r] > 0):
                print("\nCaptain:")
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print vice-captain selection each round
        for p in P:
            if (c_vice_bar[p,r].x >= 0.99):
                print("\nVice-Captain:")
                print("{0:12s} {1:12s}".format(p.split('_')[0],p.split('_')[1]))
        
        # print the score for the round
        print("\nRound Score:")
        round_score = 0
        for p in P:
            round_score += psi[p,r]*(x_bar[p,r].x + c_cap[p].x + c_vice_bar[p,r].x)
        print(round_score)
        
        # print the cumulative score
        print("\nCumulative Score")
        cumulative_score += round_score
        print(cumulative_score)
