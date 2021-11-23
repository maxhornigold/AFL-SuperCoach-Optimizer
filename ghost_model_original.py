
print("\nIMPORTS") ############################################################

from gurobipy import *
from data import get_sets_and_data
from helper import print_ghost_solution, print_ghost_scores

print("\nGETTING SETS AND DATA") ##############################################

# specify the year's data to import
year = '2021'

# import the sets and data
(P, Q_score, Q_sub, Q, P_q, Q_p, R, 
 psi, v, C_q, S_q, X_r, T_r, T_total, B, S_win, E) = get_sets_and_data(year)

print("\nCREATING MODEL") #####################################################

m = Model()

print("\nCREATING VARIABLES") #################################################

# true if player p is in position q.
x = {(p,q): m.addVar(vtype=GRB.BINARY) for p in P for q in Q}

# true if the score of player p is included in round r.
x_bar = {(p,r): m.addVar(vtype=GRB.BINARY) for p in P for r in R}

# true if player p is captain.
c_cap = {p: m.addVar(vtype=GRB.BINARY) for p in P}

# true if player p is vice-captain.
c_vice = {p: m.addVar(vtype=GRB.BINARY) for p in P}

# true if the vice-captain p's score counts in round r.
c_vice_bar = {(p,r): m.addVar(vtype=GRB.BINARY) for p in P for r in R}

# true if player p in in slot s of position q in round r.
y = {(p,q,r,s): m.addVar(vtype=GRB.BINARY) for p in P for q in Q_p[p] 
     if q in Q_sub for s in S_q[q] for r in R}

# true if player p is an emergency in position q.
e = {(p,q): m.addVar(vtype=GRB.BINARY) for p in P for q in Q_p[p] if q in Q_sub}

print("\nSETTING OBJECTIVE FUNCTION") #########################################

# maximize the total score for the season
m.setObjective(
    quicksum(quicksum(
        psi[p,r]*(x_bar[p,r] + c_cap[p] + c_vice_bar[p,r])
        for r in R) for p in P),
    GRB.MAXIMIZE)

print("\nDEFINING CONSTRAINTS") ###############################################

# CAPTAIN CONSTRAINTS

# ensure that there is only one captain and one vice-captain.
constr_4_3_1_a = m.addConstr(
    quicksum(c_cap[p] for p in P) == 1,
    )
constr_4_3_1_b = m.addConstr(
    quicksum(c_vice[p] for p in P) == 1,
    )

# ensure that the captain and vice-captain are in a scoring position.
constr_4_3_3_a = {p: m.addConstr(
    c_cap[p] <= quicksum(x[p,q] for q in Q_p[p] if q in Q_score)
    ) for p in P}
constr_4_3_3_b = {p: m.addConstr(
    c_vice[p] <= quicksum(x[p,q] for q in Q_p[p] if q in Q_score)
    ) for p in P}

# ensure that a scoring vice-captain is already a vice-captain.
constr_4_3_4 = {(p,r): m.addConstr(
    c_vice_bar[p,r] <= c_vice[p]
    ) for p in P for r in R}

# ensure that the vice-captain's score only counts if the captain doesn't play.
constr_4_3_5 = {r: m.addConstr(
    quicksum(c_vice_bar[p,r] for p in P) <= quicksum(
        c_cap[p_d] for p_d in P if psi[p_d,r]==0)
    ) for r in R}

# BUDGET CONSTRAINTS

# ensure that the value of the initial team is within the budget.
constr_4_3_6 = m.addConstr(
    quicksum(quicksum(v[p,0]*x[p,q] for q in Q_p[p]) for p in P) <= B
    )

# POSITIONAL CONSTRAINTS

# ensure that the correct number of spots in each position are filled.
constr_4_3_7 = {q: m.addConstr(
    quicksum(x[p,q] for p in P_q[q]) == C_q[q]
    ) for q in Q}

# ensure that each player can play in at most one position.
constr_4_3_8 = {p: m.addConstr(
    quicksum(x[p,q] for q in Q_p[p]) <= 1
    ) for p in P}

# ensure that the correct number of players scores count each round.
constr_4_3_8 = {r: m.addConstr(
    quicksum(x_bar[p,r] for p in P) <= X_r[r]
    ) for r in R}

# SUBSTITUTE AND EMERGENCY CONSTRAINTS

# ensure that a player can only be an emergency if they are in that position.
constr_4_3_11 = {(p,q): m.addConstr(
    e[p,q] <= x[p,q]
    ) for p in P for q in Q_p[p] if q in Q_sub}

# ensure that the maximum number of emergencies is not exceeded.
constr_4_3_12 = m.addConstr(
    quicksum(quicksum(e[p,q] for q in Q_p[p] if q in Q_sub) for p in P) <= E
    )

# ensure that each player can only assigned to a single substitute slot.
constr_4_3_13 = {(q,r,s): m.addConstr(
    quicksum(y[p,q,r,s] for p in P_q[q]) <= 1
    ) for r in R for q in Q_sub for s in S_q[q]}

# ensure that a player can only be in a slot if they are an emergency.
constr_4_3_14 = {(p,q,r): m.addConstr(
    quicksum(y[p,q,r,s] for s in S_q[q]) <= e[p,q]
    ) for p in P for q in Q_p[p] if q in Q_sub for r in R}

# ensure that each week, the number of players in a scoring position who scored
# a zero represent the maximum number of scoring bench slots in the
# corresponding substitute position.
constr_4_3_15 = {(q,r): m.addConstr(
    quicksum(quicksum(y[p,q+"_sub",r,s] for s in S_q[q+"_sub"]) for p in P_q[q]) <= 
    quicksum(x[p,q] for p in P_q[q] if psi[p,r]==0)
    ) for r in R for q in Q_score}

# ensure that the lower index slots are used before the higher index slots.
constr_4_3_16 = {(q,r,s): m.addConstr(
    quicksum(y[p,q,r,s] - y[p,q,r,s-1] for p in P_q[q]) <= 0
    ) for q in Q_sub for s in S_q[q] if s!=0 for r in R}

# ensure that an emergency is only allocated to a slot whose index is greater
# or equal to the number of other emergencies in the same position who scored
# less than that player that round.
constr_4_3_17 = {(p,q,r): m.addConstr(
    quicksum(e[p_d,q] for p_d in P_q[q] if (psi[p_d,r] < psi[p,r])) +
             quicksum((C_q[q] - s)*y[p,q,r,s] for s in S_q[q]) <= C_q[q]
    ) for q in Q_sub for p in P_q[q] for r in R}

# ensure that a player’s score counts towards the total if they are either in
# a scoring position or are a scoring emergency.
constr_4_3_18 = {(p,r): m.addConstr(
    x_bar[p,r] <= quicksum(x[p,q] for q in Q_p[p] if q in Q_score) +
    quicksum(quicksum(y[p,q,r,s] for s in S_q[q]) for q in Q_p[p] if q in Q_sub)
    ) for r in R for p in P}
    
print("\nOPTIMIZING MODEL") ###################################################

# optimize the model
m.optimize()

print("\nPRINTING SOLUTION") ##################################################

# print the chosen team
print_ghost_solution(m, P, Q, Q_score, Q_sub, P_q, Q_p, x, c_cap, c_vice, e, v)

# print the captain, remaining budget, round score, cumulative score each round
# print_ghost_scores(P, Q_p, R, psi, v, x, x_bar, c_cap, c_vice_bar, B)