# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 19:14:22 2018

@author: Adria
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import
from pyomo.environ import *
 
# Creation of a Concrete Model
model = ConcreteModel()
 
# ================================================================================
## Define sets ##
#  Sets
#       S escenarios de temperatura / nr, fr, mf /
#       O opciones de gestión / cyv, cya, ayv /;
model.s = Set(initialize=['nr','fr','mf'], doc='escenarios de temperatura')
model.o = Set(initialize=['cyv','cya', 'ayv'], doc='opciones de gestión')
 
# ================================================================================

## Define parameters ##
#   Parameters
#       CVS(s) coste del gas en cada escenario [€]
#         / nr 5.0
#           fr 6.0
#           mf 7.5 /
#       PROBS(s) probabilidad de cada escenario [p.u.]
#        /  nr 0.333333
#           fr 0.333333
#           mf 0.333334 /
#       DEMS(s) demanda en un escenario
#       /   nr 100
#           fr 150
#           mf 180 /

model.CVS =   Param(model.s, initialize={'nr':5,'fr':6, 'mf':7.5}, doc='coste del gas en cada escenario [€]')
model.PROBS = Param(model.s, initialize={'nr':0.333333,'fr':0.333333,'mf':0.333334}, doc='probabilidad de cada escenario [p.u.]')
model.DEMS = Param(model.s, initialize={'nr':100,'fr':150,'mf':180}, doc='demanda de cada escenario ')

# ================================================================================


#  Scalar CALM coste de almacenamiento [€ por año] / 1 /
model.CALM = Param(initialize=1, doc='coste de almacenamiento')

# ================================================================================

## Define variables ##
#  Variables
#       X(o) cantidad que gestiona el primer año
#       Y(o) cantidad que gestiona el segundo año
#  Positive Variable x , y ;
model.x = Var(model.o, bounds=(0.0,None), doc='cantidad que gestiona el primer año')
model.y = Var(model.o, bounds=(0.0,None), doc='cantidad que gestiona el segundo año')

# ================================================================================

 
## Define contrains ##
# BALDEM1 .. X('cyv') =E= DEMS('nr') ;

def BALDEM1(model):
  return model.x['cyv']= model.DEMS['nr']
model.demand1 = Constraint(rule=BALDEM1, doc='balance de demanda del primero año')


# BALDEM2 .. X('ayv') + Y('cyv') =E= DEM ;
def BALDEM2(model):
  return model.x['ayv'] + model.y['cyv'] = model.DEM
model.demand2 = Constraint(rule=BALDEM2, doc='balance de demanda del segundo año')
 

#  GSTDEP .. X('cya') =E= X('ayv') ;
def  GSTDEP(model)
  return model.x['cya'] = model.x['ayv']
model.gest = Constraint(rule=GSTDEP, doc='gestion del deposito')
# ================================================================================



## Define Objective and solve ##
#  cost ..    COSTE =E= CVS('nr') * (X('cyv')+X('cya')) + CALM * X('cya')+ CV * (Y('cyv')+Y('cya')) ;
def objective_rule(model):
  return model.CVS['nr'] * ( model.x['cyv'] + model.x['cya'] ) + model.CALM * model.x['cya'] + model.CV * ( model.y['cyv'] + model.y['cya'] )
model.objective = Objective(rule=objective_rule, sense=minimize, doc='Define objective function')
 


#  Model transport /all/ ;
#  Solve transport using lp minimizing z ;
## Display of the output ##
# Display x.l, x.m ;
def pyomo_postprocess(options=None, instance=None, results=None):
  model.x.display()
 
# This is an optional code path that allows the script to be run outside of
# pyomo command-line.  For example:  python transport.py
if __name__ == '__main__':
    # This emulates what the pyomo command-line tools does
    from pyomo.opt import SolverFactory
    import pyomo.environ
    opt = SolverFactory("glpk")
    results = opt.solve(model)
    #sends results to stdout
    results.write()
    print("\nDisplaying Solution\n" + '-'*60)
    pyomo_postprocess(None, model, results)

