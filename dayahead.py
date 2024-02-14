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
start_shiftable_loads = 16  # Start of shiftable loads
end_shiftable_loads = 44  # End of shiftable loads

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

