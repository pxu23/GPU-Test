def addSetHomeAwayPerGame(constraintLibrary):
  for s in constraintLibrary.series:
    for i in range(len(constraintLibrary.teams)):
      for j in range(len(constraintLibrary.teams)):
        if i != j:
          curr_team = constraintLibrary.teams[i]
          opposing_team = constraintLibrary.teams[j]
          sum = (constraintLibrary.assignments[(s,curr_team,opposing_team)]
                   + constraintLibrary.assignments[(s,opposing_team,curr_team)])
          constraintLibrary.solver.addConstr(sum <= 1,name='setHomeAwayPerGame')

  constraintLibrary.solver.update()