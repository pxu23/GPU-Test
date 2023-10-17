# In this constraint, every team must play in each slot (exactly once)
def addPlayInEverySlot(constraintLibrary):
    for s in constraintLibrary.series:
      for curr_team in constraintLibrary.teams:
          sum = 0
          for opposing_team in constraintLibrary.teams:
            if curr_team != opposing_team:
                sum = sum + (constraintLibrary.assignments[(s, curr_team, opposing_team)]
                    + constraintLibrary.assignments[(s, opposing_team, curr_team)])
          constraintLibrary.solver.addConstr(sum == 1, name='playInEverySlot')

    constraintLibrary.solver.update()