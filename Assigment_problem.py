# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 22:37:49 2018

@author: ALBA
"""

import pyomo.opt
# Import of the pyomo module
from pyomo.environ import *

m = ConcreteModel()


m.p  = Set(initialize=['p1','p2','p3'], doc='people', ordered = True)
m.j  = Set(initialize=['j1','j2','j3'], doc='jobs', ordered = True)


ctab = {
    ('p1',  'j1') : 11,
    ('p1',  'j2') : 5,
    ('p1',  'j3') : 2,
    ('p2',  'j1') : 15,
    ('p2',  'j2') : 12,
    ('p2',  'j3') : 8,
    ('p3',  'j1') : 3,
    ('p3',  'j2') : 1,
    ('p3',  'j3') : 10
    }

m.d = Param(m.p, m.j, initialize=ctab, doc='Sustainability coefficient')
m.d.display()

m.y = Var(m.p, m.j, within=Binary)

def constraint_logic1(m,p):
  return sum(m.y[p,j] for j in m.j) == 1
m.logic1 = Constraint(m.p, rule=constraint_logic1)
 
def constraint_logic2(m,j):
  return sum(m.y[p,j] for p in m.p) == 1
m.logic2 = Constraint(m.j, rule=constraint_logic2)
 
def objective_rule(m):
  return sum(m.d[p,j]*m.y[p,j] for p in m.p for j in m.j)
m.objective = Objective(rule=objective_rule, sense=maximize, doc='Define objective function')

m.y.display()

opt = SolverFactory("ipopt")
results = opt.solve(m)
results.write()
m.pprint()
