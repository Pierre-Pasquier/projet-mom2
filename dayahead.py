import gurobipy as gp
from gurobipy import GRB
import numpy as np
import os

# Define constants
HOURS_IN_DAY = 48
M = 5  # Number of shiftable loads
N = 5  # Number of non-shiftable loads
os.environ["GRB_LICENSE_FILE"] = "./gurobi.lic"

# Create a new model
model = gp.Model()

# Define variables
gamma_m = model.addMVar((HOURS_IN_DAY,M), vtype=GRB.CONTINUOUS, name="gamma_m")
gamma_n = model.addMVar((HOURS_IN_DAY,N), vtype=GRB.CONTINUOUS, name="gamma_n")
P_m = model.addMVar((HOURS_IN_DAY,M), vtype=GRB.CONTINUOUS, name="P_m")
P_n = model.addMVar((HOURS_IN_DAY,N), vtype=GRB.CONTINUOUS, name="P_n")
Tu_set = model.addVars(HOURS_IN_DAY,vtype=GRB.CONTINUOUS, name="Tu_set")
Tu_req = model.addVars(HOURS_IN_DAY,vtype=GRB.CONTINUOUS, name="Tu_req")

# Define parameters
E_m = np.random.rand(M)  # Random energy values for demonstration
E_n = np.random.rand(N)  # Random energy values for demonstration
P_min = 0
#P_ul is the onsite power produced
P_ul = 50
P_max = 100
T_min = 18
T_max = 25
kG = 0.1  # Price of power from the grid
dissatisfaction_cost = 0.5  # Fixed dissatisfaction cost per unit change in temperature
start_shiftable_loads = 0  # Start of shiftable loads
end_shiftable_loads = 24  # End of shiftable loads

# Set objective function
objective = gp.quicksum((gp.quicksum(gamma_m[h][m]*P_m[h][m] for m in range(M)) + gp.quicksum(gamma_n[h][n]*P_n[h][n] for n in range(N)) - P_ul) for h in range(HOURS_IN_DAY)) * kG + dissatisfaction_cost * gp.quicksum(Tu_set[h] - Tu_req[h] for h in range(HOURS_IN_DAY))
model.setObjective(objective, GRB.MINIMIZE)

# Add constraints
for m in range(M):
    model.addConstr(gp.quicksum(gamma_m[h][m] * P_m[h][m] for h in range(start_shiftable_loads, end_shiftable_loads)) == E_m[m])
for n in range(N):
    model.addConstr(gp.quicksum(gamma_n[h][n] * P_n[h][n] for h in range(start_shiftable_loads, end_shiftable_loads)) == E_n[n])

for h in range(HOURS_IN_DAY):
    model.addConstr(gp.quicksum(gamma_m[h][m] * P_m[h][m] for m in range(M)) + gp.quicksum(gamma_n[h][n] * P_n[h][n] for n in range(N)) >= 0)
for h in range(HOURS_IN_DAY):
    for m in range(M):
        if start_shiftable_loads <= h <= end_shiftable_loads:
            model.addConstr(P_m[h][m] >= 0)
        else:
            model.addConstr(gamma_m[h][m] >= 0)
    for n in range(N):
        if start_shiftable_loads <= h <= end_shiftable_loads:
            model.addConstr(P_n[h][n] >= 0)
        else:
            model.addConstr(gamma_n[h][n] >= 0)

for h in range(HOURS_IN_DAY):
    model.addConstrs(P_m[h][m] >= P_min for m in range(M))
    model.addConstrs(P_n[h][n] <= P_max for n in range(N))

for h in range(HOURS_IN_DAY):
    model.addConstr(Tu_set[h] >= T_min)
    model.addConstr(Tu_set[h] <= T_max)
    model.addConstr(Tu_req[h] >= T_min)
    model.addConstr(Tu_req[h] <= T_max)

# Optimize the model
model.optimize()

# Display the results
print("Optimal gamma:", [[gamma_m[h][m] for h in range(HOURS_IN_DAY)] for m in range(M)])
print("Optimal P_m:", [[P_m[h][m] for h in range(HOURS_IN_DAY)] for m in range(M)])
print("Optimal P_n:", [[P_m[h][n] for h in range(HOURS_IN_DAY)] for m in range(n)])
print("Optimal Tu_set:", [Tu_set[h] for h in range(HOURS_IN_DAY)])
print("Optimal Tu_req:", [Tu_req[h] for h in range(HOURS_IN_DAY)])
print("Objective value:", model.objVal)