import pyomo.environ as pyo

# Create a pyomo model
model = pyo.ConcreteModel()


# Define the variables
model.x1 = pyo.Var(domain=pyo.NonNegativeReals) # This doesn´t have to be x1, it can be anything, I just need to define the domain
model.x2 = pyo.Var(domain=pyo.NonNegativeReals)
# Here define the rest of the variables for our problem. Grid cost, energy consumption, etc.


# Define the constraints (basically the equation system)
model.c=pyo.ConstraintList()
model.c.add(model.x1*10 + 1 >= model.x2) # the result of the expression is a boolean, so whatever we´re evaluating has to evaluate to a boolean
model.c.add(model.x1*(0.2)+4 >= model.x2)
model.c.add(model.x1*(-0.2)+6 >= model.x2)

# Define the objective function (basically the equation to maximize)
model.objective = pyo.Objective(rule=lambda model: model.x1+model.x2*10, sense = pyo.maximize) # Here we can use a custom defined function, for the sake of simplicity it´s a lambda func

# Define the solver
solver = pyo.SolverFactory('glpk')

# Solve the model
result = solver.solve(model)

print(result)
print(model.x1(), model.x2())
print(model.objective())
print(model.display())


