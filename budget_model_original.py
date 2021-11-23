
print("\nIMPORTS") ############################################################

from gurobipy import *
from data import get_sets_and_data
from helper import print_budget_solution, print_budget_scores

print("\nGETTING SETS AND DATA") ##############################################

# specify the year's data to import
year = '2021'

# import the sets and data
(P, Q_score, Q_sub, Q, P_q, Q_p, R, 
 psi, v, C_q, S_q, X_r, T_r, T_total, B, S_win, E) = get_sets_and_data(year)

print("\nCREATING MODEL") #####################################################

m = Model()

print("\nCREATING VARIABLES") #################################################

# true if player p is in position q for round r.
x = {(p,q,r): m.addVar(vtype=GRB.BINARY) for p in P for q in Q for r in R}

# true if the score of player p is included in round r.
x_bar = {(p,r): m.addVar(vtype=GRB.BINARY) for p in P for r in R}

# true if player p is captain for round r.
c = {(p,r): m.addVar(vtype=GRB.BINARY) for p in P for r in R}

# true if player p is traded into the team for round r.
t_in = {(p,r): m.addVar(vtype=GRB.BINARY) for p in P for r in R}

# true if player p is traded out of the team for round r.
t_out = {(p,r): m.addVar(vtype=GRB.BINARY) for p in P for r in R}

# remaining budget for round r.
b_r = {r: m.addVar(vtype=GRB.CONTINUOUS) for r in R}

# starting budget.
Beta = m.addVar(vtype=GRB.CONTINUOUS)

print("\nSETTING OBJECTIVE FUNCTION") #########################################

# minimize the starting budget
m.setObjective(Beta, GRB.MINIMIZE)

print("\nDEFINING CONSTRAINTS") ###############################################

# TRADE CONSTRAINTS

# ensure that the season trade limit is not exceeded.
constr_4_2_1 = m.addConstr(
    quicksum(quicksum(t_in[p,r] for r in R[1:]) for p in P) <= T_total
    )

# ensure that the weekly trade limit is not exceeded.
constr_4_2_2 = {r: m.addConstr(
    quicksum(t_in[p,r] for p in P) <= T_r[r]
    ) for r in R[1:]}
   
# record that a player has been traded in or out.
constr_4_2_3 = {(p,r): m.addConstr(
    quicksum(x[p,q,r] - x[p,q,r-1] for q in Q_p[p]) == t_in[p,r] - t_out[p,r]
    ) for p in P for r in R[1:]}

# CAPTAIN CONSTRAINTS

# ensure that there is one captain each round.
constr_4_2_5 = {r: m.addConstr(
    quicksum(c[p,r] for p in P) == 1
    ) for r in R}

# ensure that the captain cannot be in a substitute position.
constr_4_2_6 = {(p,r): m.addConstr(
    c[p,r] <= quicksum(x[p,q,r] for q in Q_p[p] if q in Q_score)
    ) for p in P for r in R}

# BUDGET CONSTRAINTS

# ensure that the initial team is within the starting budget.
constr_4_2_7 = m.addConstr(
    b_r[0] + quicksum(quicksum(v[p,0]*x[p,q,0]
                               for q in Q_p[p]) for p in P) == Beta
    )

# record the budget for the next round.
constr_4_2_8 = {r: m.addConstr(
    b_r[r] == (b_r[r-1] + 
               quicksum(v[p,r]*t_out[p,r] for p in P) - 
               quicksum(v[p,r]*t_in[p,r] for p in P))
    ) for r in R[1:]}

# POSITIONAL CONSTRAINTS

# ensure that the correct number of spots in each position are filled.
constr_4_2_9 = {(r,q): m.addConstr(
    quicksum(x[p,q,r] for p in P_q[q]) == C_q[q]
    ) for r in R for q in Q}

# ensure that each player can play in at most one position each round.
constr_4_2_10 = {(p,r): m.addConstr(
    quicksum(x[p,q,r] for q in Q_p[p]) <= 1
    ) for p in P for r in R}
    
# ensure that a player is in a scoring position to have their score counted.
constr_4_2_11 = {(p,r): m.addConstr(
    x_bar[p,r] <= quicksum(x[p,q,r] for q in Q_p[p] if q in Q_score)
    ) for p in P for r in R}
    
# ensure that the correct number of players scores count each round.
constr_4_2_12 = {r: m.addConstr(
    quicksum(x_bar[p,r] for p in P) <= X_r[r]
    ) for r in R}

# TOTAL SCORE CONSTRAAINT

# ensure that the total season score beats the previous winning score.
constr_4_2_14 = m.addConstr(
    quicksum(quicksum(psi[p,r]*(x_bar[p,r]+c[p,r]) 
                      for r in R) for p in P) >= S_win + 1
    )

print("\nOPTIMIZING MODEL") ###################################################

# optimize the model
m.optimize()

print("\nPRINTING SOLUTION") ##################################################

# print team each week. Change R as desired.
print_budget_solution(m, P, Q, Q_score, Q_sub, P_q, Q_p, R[0:1], x, x_bar, 
                      t_in, t_out, b_r, c, psi)

# print scores each week. Change R as desired.
# print_budget_scores(m, P, P_q, R, Q_score, Q_sub, x, x_bar, 
#                     t_in, t_out, b_r, c, psi)