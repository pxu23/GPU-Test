## A Club is home on either side of the ASG break but not both
  ## In our example it's series 15 and 16 on both sides on the ASG break

## to modify (or relax this immovable constraint), we can modify it to be that clubs
## are home on both sides of the ASG break (By default it's that clubs are away on one side of the ASG break)
## bothSidesHomeAllowed boolean variable denotes whether clubs can be home on both sides of the ASG break
## by default, the bothSidesHomeAllowed variables is False
def addHomeOnOneSideOfASGBreak(constraintLibrary,bothSidesHomeAllowed):
    for team in constraintLibrary.teams:
      sum = 0
      for opposing_team in constraintLibrary.teams:
        ## this ensures that no team plays itself
        if team != opposing_team:
          ## add this to the solver for the constraint Library. Note that series 15 and 16
          ## are series on either side of the ASG break. Note (15,opposing_team,team) means that
          ## the team is home on Series 15 and (16,opposing_team,team) means that the team is home on
          ## Series 16
          if bothSidesHomeAllowed == True:
            constraintLibrary.solver.addConstr(constraintLibrary.assignments[(15,opposing_team,team)]
                          + constraintLibrary.assignments[(16,opposing_team,team)] <= 2,name = 'homeOneSideOfASG')
          else:
            constraintLibrary.solver.addConstr(constraintLibrary.assignments[(15,opposing_team,team)]
                          + constraintLibrary.assignments[(16,opposing_team,team)] == 1, name = 'homeOneSideOfASG')

    constraintLibrary.solver.update()