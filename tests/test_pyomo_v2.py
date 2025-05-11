import pyomo.environ as pyo
import matplotlib
matplotlib.use('Qt5Agg')  # Use PyQt5 backend
import matplotlib.pyplot as plt


# INITIAL THOUGHTS:
# Define the sets -> all time steps (t E T)

# Define the parameters 
# Pt - Price at a time t E T
# Qt - charging energy at a time t E T
# S0 - initial storage charge state (also the max if we´re evaluating at the beginning)
# Wmax - maximum power sold


# Variables (decision variables) how much power we´re going to sell at each time period
# wt - power sold at time t E T
# st - energy stored at time t E T

# Objective -> maximize the revenue of the electricity sold
# Maximize "Z" = sum(Pt*wt)


# Constraints
# The power we´re producing is less or equal than the max power produce in t E T (wt <= Wmax)
# The storage is less or equal than the max storage in t E T (st <= S0)
# Track the difference in storage between t and t-1 (st-(st-1) = Qt - wt) (valid for all t in the set T such that index t is greater or equal to 2)
# Define the initial storage (S1-S0 = Q1-w1)



# NOW CODING: 


# Index in time (P sub T) later this should be variable
# THESE HAVE TO BE DICTS!!! PYOMO NEEDS DICTS!!
price_schedule ={
    0:0.5,
    1:0.6,
    2:1.0,
    3:1.0,
    4:0.9,
    5:1.1,
    6:1.8,
    7:1.5,
    8:0.9,
    9:0.8,
    10:0.7,
    11:1.0 
}

# Index in time (Q sub T) later this should be variable
# THESE HAVE TO BE DICTS!!! PYOMO NEEDS DICTS!!
charge_schedule = {
    0:0.0,
    1:0.0,
    2:0.0,
    3:0.0,
    4:0.3,
    5:0.15,
    6:0.15,
    7:0.05,
    8:0.05,
    9:0.05,
    10:0,
    11:0
}


# Define the model
model = pyo.ConcreteModel()

# --------------- Parameters and constant information
# Number of time steps
model.nt = pyo.Param(initialize=len(price_schedule), domain=pyo.Integers)

# Set of time steps
model.T = pyo.Set(initialize=range(model.nt()))

# Sales price at each time step
model.price = pyo.Param(model.T, initialize=price_schedule)

# Power added from charging at each time step
model.charge = pyo.Param(model.T, initialize=charge_schedule)

# Initial/maximum storage inventory
model.S0 = pyo.Param(initialize=500., domain=pyo.NonNegativeReals)

# Maximum instantaneous power
model.Wmax = pyo.Param(initialize=150., domain=pyo.NonNegativeReals)


# --------------- Variables
# Power output
model.w = pyo.Var(model.T, domain=pyo.NonNegativeReals)  # This defines w for all t in T

# Energy stored
model.s = pyo.Var(model.T, domain=pyo.NonNegativeReals)  # This defines s for all t in T


# --------------- Objective function
def objective_func(model):
    # sum the price times power produced for all time steps
    return sum([model.w[t]*model.price[t] for t in model.T])

# Define the objective function
model.objective = pyo.Objective(rule=objective_func, sense=pyo.maximize)


# --------------- Constraints
# Storage inventory is limited by capacity
def constr_store_capacity(model, t):
    if t == 0:
        return model.s[t] == model.S0 # If t = 0, the storage is the initial storage
    else:
        return model.s[t] <= model.S0 # If t > 0, the storage is less than the initial storage
model.constr_store_capacity = pyo.Constraint(model.T, rule=constr_store_capacity) # Evaluates the constraint for all t in T
# If we had more sets that we want to pass, we could do it like this:
# model.constr_store_capacity = pyo.Constraint(model.T, model.S, rule=constr_store_capacity)

# Power output limited by maximum power
def constr_power(model, t):
    return model.w[t] <= model.Wmax # Tells us if we´re producing less than the maximum power
model.constr_power = pyo.Constraint(model.T, rule=constr_power)

# Track the difference in storage between t and t-1
def constr_store_balance(model, t):
    if t == 0:
        return model.s[t] == model.S0 - model.w[t] + model.charge[t]*model.S0
    else:
        return model.s[t] == model.s[t-1] - model.w[t] + model.charge[t]
model.constr_store_balance = pyo.Constraint(model.T, rule=constr_store_balance)


# Set up the solver
solver = pyo.SolverFactory('glpk')

# Run the simulation
# Set the keepfiles to true if we want to debug the solver
results = solver.solve(model, keepfiles=True, logfile='solve.log')


# Print and summarize the results
print(model.display())
print(f"time\tprice\tpower\tstorage")
for t in model.T:
    print(f"{t}\t{model.price[t]:.2f}\t{pyo.value(model.w[t]):>5.1f}\t{pyo.value(model.s[t]):>5.1f}")


# Plot the results
plt.bar(range(model.nt()), [pyo.value(model.w[t]) for t in model.T], label='Power sold')
plt.ylabel('Power sold (W)')
plt.xlabel('Time (h)')
plt.title('Power sold at each hour')
plt.legend()
ax = plt.gca().twinx()
ax.plot(range(model.nt()), [pyo.value(model.s[t])/model.S0() for t in model.T], 'r-', label='Storage', color="red", marker="o")
ax.plot(range(model.nt()), [model.price[t] for t in model.T], 'g-', label='Price', color="green", marker="o")
ax.set_ylabel('Storage (%) and Price (€/kWh)')
ax.legend(loc='lower left')
plt.show()




        














