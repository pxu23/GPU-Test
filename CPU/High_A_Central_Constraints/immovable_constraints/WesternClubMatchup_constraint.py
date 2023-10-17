## All Western clubs have a minimum of 1-1 and maximum of 2-2 in division
  ## WIS and BEL has minimum of 1-1 and maximum of 2-2
def addWestTeamsHomeRoadMatchupInDivision(constraintLibrary):
    for i in range(len(constraintLibrary.west_teams) - 1):
      for j in range(i + 1,len(constraintLibrary.west_teams)):
        team_one = constraintLibrary.west_teams[i]
        team_two = constraintLibrary.west_teams[j]
        matchup = (team_one,team_two)


        num_home_teamone = 0
        for s in constraintLibrary.series:
          num_home_teamone += constraintLibrary.assignments[(s,team_two,team_one)]

        num_home_teamtwo = 0
        for s in constraintLibrary.series:
          num_home_teamtwo += constraintLibrary.assignments[(s,team_one,team_two)]

        constraintLibrary.solver.addConstr(num_home_teamone >= 1, name='WestTeamsHomeRoadMatchupInDivision')
        constraintLibrary.solver.addConstr(num_home_teamone <= 2, name = 'WestTeamsHomeRoadMatchupInDivision')
        constraintLibrary.solver.addConstr(num_home_teamtwo >= 1, name = 'WestTeamsHomeRoadMatchupInDivision')
        constraintLibrary.solver.addConstr(num_home_teamtwo <= 2, name ='WestTeamsHomeRoadMatchupInDivision')

    constraintLibrary.solver.update()
