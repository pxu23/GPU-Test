def addCertainMatchupGuaranteedThreeSeries(constraintLibrary):
  addFWSBMatchup(constraintLibrary)
  addWISBELMatchup(constraintLibrary)
  addWISCRMatchup(constraintLibrary)
  addWISPEOMatchup(constraintLibrary)
  addWISQCMatchup(constraintLibrary)
  constraintLibrary.solver.update()

## FW/SB matchup guaranteed three series
def addFWSBMatchup(constraintLibrary):
    sum = 0
    for s in constraintLibrary.series:
      sum += (constraintLibrary.assignments[(s,'South Bend Cubs','Fort Wayne TinCaps')]
              + constraintLibrary.assignments[(s,'Fort Wayne TinCaps','South Bend Cubs')])
    constraintLibrary.solver.addConstr(sum == 3,name='ThreeSeriesMatchups')

  ## WIS/BEL matchup guaranteed three series
def addWISBELMatchup(constraintLibrary):
    sum = 0
    for s in constraintLibrary.series:
      sum += (constraintLibrary.assignments[(s,'Wisconsin Timber Rattlers','Beloit Sky Carp')]
              + constraintLibrary.assignments[(s,'Beloit Sky Carp','Wisconsin Timber Rattlers')])
    constraintLibrary.solver.addConstr(sum == 3,name='ThreeSeriesMatchups')

  ## WIS/CR matchup guaranteed three series
def addWISCRMatchup(constraintLibrary):
    sum = 0
    for s in constraintLibrary.series:
      sum += (constraintLibrary.assignments[(s,'Wisconsin Timber Rattlers','Cedar Rapids Kernels')]
              + constraintLibrary.assignments[(s,'Cedar Rapids Kernels','Wisconsin Timber Rattlers')])
    constraintLibrary.solver.addConstr(sum == 3,name='ThreeSeriesMatchups')

  ## WIS/PEO matchup
def addWISPEOMatchup(constraintLibrary):
    sum = 0
    for s in constraintLibrary.series:
      sum += (constraintLibrary.assignments[(s,'Wisconsin Timber Rattlers','Peoria Cheifs')]
              + constraintLibrary.assignments[(s,'Peoria Cheifs','Wisconsin Timber Rattlers')])
    constraintLibrary.solver.addConstr(sum == 3,name='ThreeSeriesMatchups')

## WIS/AC matchup
def addWISQCMatchup(constraintLibrary):
    sum = 0
    for s in constraintLibrary.series:
      sum += (constraintLibrary.assignments[(s,'Wisconsin Timber Rattlers','Quad Cities River Bandits')]
              + constraintLibrary.assignments[(s,'Quad Cities River Bandits','Wisconsin Timber Rattlers')])
    constraintLibrary.solver.addConstr(sum == 3,name='ThreeSeriesMatchups')