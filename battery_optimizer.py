import gurobipy as gp
from gurobipy import GRB
import numpy as np
import os

# Define constants
HOURS_IN_DAY = 48
U = 3  # Number of users
M = 5  # Number of shiftable loads
N = 5  # Number of non-shiftable loads
os.environ["GRB_LICENSE_FILE"] = "./gurobi.lic"

# Create a new model
model = gp.Model()

# Define variables
dollar_u = model.addMVar(HOURS_IN_DAY, vtype=GRB.CONTINUOUS, name="dollar_u")
dollar_csf = model.addMVar(HOURS_IN_DAY, vtype=GRB.CONTINUOUS, name="dollar_csf")

# Define parameters
dollar = [[]] # Will be defined later
dollar_csf = gp.quicksum((beta[u] * k_b[u][h] * P_b[u][h] for u in range(U)) for h in range(HOURS_IN_DAY)) + k_MCP[h] * P_b_G[h]

# Set objective function
objective = dollar[h][u] + dollar_csf
model.setObjective(objective, GRB.MAXIMIZE)

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

import matplotlib.pyplot as plt

# Extract the optimal gamma_m values
optimal_gamma_m = [[gamma_m[h][m].x for h in range(HOURS_IN_DAY)] for m in range(M)]

# Plot gamma_m curves
for m in range(M):
    plt.plot(range(HOURS_IN_DAY), optimal_gamma_m[m], label=f"Curve {m+1}")

# Set labels and title
plt.xlabel("h")
plt.ylabel("gamma_m")
plt.title("Gamma_m Curves")

# Add legend
plt.legend()

# Save the plot
plt.savefig("plot.png")

# Show the plot
plt.show()

# Create a new figure
plt.figure()

# Extract the optimal P_m values
optimal_P_m = [[P_m[h][m].x for h in range(HOURS_IN_DAY)] for m in range(M)]

# Plot P_m curves
for m in range(M):
    plt.plot(range(HOURS_IN_DAY), optimal_P_m[m], label=f"P_m {m+1}")

# Set labels and title
plt.xlabel("h")
plt.ylabel("P_m")
plt.title("P_m Curves")

# Add legend
plt.legend()

# Save the plot
plt.savefig("P_m_plot.png")

# Show the plot
plt.show()

# Create a new figure
plt.figure()

# Extract the optimal P_n values
optimal_P_n = [[P_n[h][n].x for h in range(HOURS_IN_DAY)] for n in range(N)]


# Plot P_n curves
for n in range(N):
    plt.plot(range(HOURS_IN_DAY), optimal_P_n[n], label=f"P_n {n+1}")

# Set labels and title
plt.xlabel("h")
plt.ylabel("P_n")
plt.title("P_n Curves")

# Add legend
plt.legend()

# Save the plot
plt.savefig("P_n_plot.png")

# Show the plot
plt.show()

