## For the Eastern Clubs, certain matchups are guaranteed 2-2
def addEasternClubsGuaranteeCertainMatchup(constraintLibrary):
  addGreatLakesLansingTwoOnTwo(constraintLibrary)
  addGreatLakesWestMichiganTwoOnTwo(constraintLibrary)
  addLansingWestMichiganTwoOnTwo(constraintLibrary)
  addLakeCountyDaytonTwoOnTwo(constraintLibrary)
  addFortWayneDaytonTwoOnTwo(constraintLibrary)
  constraintLibrary.solver.update()

# Fort Waynes and Dayton each play 2 home series with the other away
# and 2 road series with the other home
def addFortWayneDaytonTwoOnTwo(constraintLibrary):
  num_home_fort_wayne = 0
  for s in constraintLibrary.series:
    num_home_fort_wayne += constraintLibrary.assignments[(s,'Dayton Dragons','Fort Wayne TinCaps')]
  constraintLibrary.solver.addConstr(num_home_fort_wayne == 2,name='CertainMatchupTwoToTwo')

  num_home_dayton =0
  for s in constraintLibrary.series:
    num_home_dayton += constraintLibrary.assignments[(s,'Fort Wayne TinCaps','Dayton Dragons')]
  constraintLibrary.solver.addConstr(num_home_dayton == 2,name='CertainMatchupTwoToTwo')

# Lake County and Dayton each play 2 home series with the other away
# and 2 road series with the other home
def addLakeCountyDaytonTwoOnTwo(constraintLibrary):
  num_home_lake_county = 0
  for s in constraintLibrary.series:
    num_home_lake_county += constraintLibrary.assignments[(s,'Dayton Dragons','Lake County Captains')]
  constraintLibrary.solver.addConstr(num_home_lake_county == 2,name='CertainMatchupTwoToTwo')

  num_home_dayton = 0
  for s in constraintLibrary.series:
    num_home_dayton += constraintLibrary.assignments[(s,'Lake County Captains','Dayton Dragons')]
  constraintLibrary.solver.addConstr(num_home_dayton == 2,name='CertainMatchupTwoToTwo')

## Great Lakes and Lansing each play 2 home series with the other away
## and 2 road series with the other home
def addGreatLakesLansingTwoOnTwo(constraintLibrary):
    num_home_great_lakes = 0
    for s in constraintLibrary.series:
      num_home_great_lakes += constraintLibrary.assignments[(s,'Lansing Lugnuts','Great Lakes Loons')]
    constraintLibrary.solver.addConstr(num_home_great_lakes == 2,name='CertainMatchupTwoToTwo')

    num_home_lansing = 0
    for s in constraintLibrary.series:
      num_home_lansing += constraintLibrary.assignments[(s,'Great Lakes Loons','Lansing Lugnuts')]
    constraintLibrary.solver.addConstr(num_home_lansing == 2,name='CertainMatchupTwoToTwo')

## Great Lakes and West Michigan each play 2 home series with the other team away
## and 2 road series with the other team home
def addGreatLakesWestMichiganTwoOnTwo(constraintLibrary):
    num_home_great_lakes = 0
    for s in constraintLibrary.series:
      num_home_great_lakes += constraintLibrary.assignments[(s,'West Michigan Whitecaps','Great Lakes Loons')]
    constraintLibrary.solver.addConstr(num_home_great_lakes == 2,name='CertainMatchupTwoToTwo')

    num_home_west_michigan = 0
    for s in constraintLibrary.series:
      num_home_west_michigan += constraintLibrary.assignments[(s,'Great Lakes Loons','West Michigan Whitecaps')]
    constraintLibrary.solver.addConstr(num_home_west_michigan == 2,name='CertainMatchupTwoToTwo')

## Lansing and West Michigan each play 2 home series with the other team away
## and 2 road series with the other team home
def addLansingWestMichiganTwoOnTwo(constraintLibrary):
    num_home_lansing = 0
    for s in constraintLibrary.series:
      num_home_lansing += constraintLibrary.assignments[(s,'West Michigan Whitecaps','Lansing Lugnuts')]
    constraintLibrary.solver.addConstr(num_home_lansing == 2,name='CertainMatchupTwoToTwo')

    num_home_west_michigan = 0
    for s in constraintLibrary.series:
      num_home_west_michigan += constraintLibrary.assignments[(s,'Lansing Lugnuts','West Michigan Whitecaps')]
    constraintLibrary.solver.addConstr(num_home_west_michigan == 2,name='CertainMatchupTwoToTwo')