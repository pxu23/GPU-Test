## This is the method for the constraint that the south Bend is required to play
## all Eastern clubs once
def addSouthBendPlayAllEasternClubOnce(constraintLibrary):
  for team in constraintLibrary.east_teams:
    sum = 0
    for s in constraintLibrary.series:
        sum = sum + (constraintLibrary.assignments[(s,team,'South Bend Cubs')]
                       + constraintLibrary.assignments[(s,"South Bend Cubs",team)])
    constraintLibrary.solver.addConstr(sum >= 1, name = 'SouthBendRequiredToPlayAllEasternClubsOnce')

  constraintLibrary.solver.update()