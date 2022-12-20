from pyscipopt import Model
model = Model("Example")


ore = model.addVar("ore", vtype="INTEGER")
ore_robot = model.addVar("ore_robot", vtype="INTEGER")
clay = model.addVar("clay", vtype="INTEGER")
clay_robot = model.addVar("clay_robot", vtype="INTEGER")
obsidian = model.addVar("obsidian", vtype="INTEGER")
obsidian_robot = model.addVar("obsidian_robot", vtype="INTEGER")
geode = model.addVar("geode", vtype="INTEGER")
geode_robot = model.addVar("geode_robot", vtype="INTEGER")
model.setObjective(geode, type="maximise")
model.addCons(ore_robot = 4*ore)
model.optimize()
sol = model.getBestSol()
print("x: {}".format(sol[geode]))

