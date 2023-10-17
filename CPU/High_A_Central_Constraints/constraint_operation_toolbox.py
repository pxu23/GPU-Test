#def addConstraint(env,constraintID):
## adds a constraint to the constraint library
def addConstraint(library,constraintID):
    ## we will print to the console the fact that the addConstraint method is called
    ## and that the constraintID under consideration we are trying to add.
    #print('addConstraint is called')
    #print(f'constraintID is {constraintID}')

    ## Case: ConstraintID is SouthBendRequiredToPlayAllEasternClubsOnce
    if constraintID == 'SouthBendRequiredToPlayAllEasternClubsOnce':
      #print('adding constraint SouthBendRequiredToPlayAllEasternClubsOnce')
      ## We will add the constraint that South Bend is required to play all Eastern Clubs once
      ## to the constraint library of the RL immovable agent by calling the constraint class 
      ## defined in the immovable constraints notebook imported in this file. 
      library.addSouthBendPlayAllEasternClubOnceConstraint()
      # library.solve()

    ## Case: The constraint id to add is 2
    elif constraintID == 'NoBackToBackSeries':
      ## We log to the console that we are adding constraint 2
      # print('adding constraint NoBackToBackSeries')

      ## we call the constraint class noBackToBackSeries
      library.addNoBackToBackSeriesConstraint()
      # library.solve()

    ## Case: constraint id to be added is CertainMatchupTwoToTwo
    elif constraintID == 'CertainMatchupTwoToTwo':
      ## we output that we are adding constraint with id CertainMatchupTwoToTwo
      # print('adding constraint CertainMatchupTwoToTwo')
      library.addEasternClubsGuaranteeCertainMatchupConstraint()
      # library.solve()

    ## chosen constraintID is EachClub132Games
    elif constraintID == 'EachClub132Games':
      ## print that we are adding constraint EachClub132Games
      # print('adding constraint EachClub132Games')
      library.addTotal132GamesConstraint()
      # library.solve()

    ## Here our chosen constraint id is AllSeriesSixGamesWithTwoThreeGame
    elif constraintID == 'AllSeriesSixGamesWithTwoThreeGame':
      ## we print that we are adding constraint AllSeriesSixGamesWithTwoThreeGame
      # print('adding constraint AllSeriesSixGamesWithTwoThreeGame')
      library.addAllSeriesSixGamesWithTwoExceptionsConstraint()
      # library.solve()

    elif constraintID == 'ClubCannotHostMoreThanOnceInFourWeekPeriod':
      library.addHostNoMoreThanOnceFourWeekConstraint()
      # library.solve()

    elif constraintID == 'certainMatchupGuaranteedThreeSeries':
      library.addCertainMatchupGuaranteedThreeSeriesConstraint()
      # library.solve()
    elif constraintID == 'WestTeamsHomeRoadMatchupInDivision':
      library.addWestTeamsHomeRoadMatchupInDivisionConstraint()
      # library.solve()
    elif constraintID == 'setHomeAwayPerGame':
      library.addSetHomeAwayPerGameConstraint()
      # library.solve()
    elif constraintID == 'NoPlayOnASGBreak':
      library.addNoPlayOnASGBreakConstraint()
      # library.solve()
    elif constraintID == 'playInEverySlot':
      library.addPlayInEverySlotConstraint()
      # library.solve()

    ## adding movable constraints
    elif constraintID == 'homeOneSideOfASG':
      library.addHomeOnOneSideOfASGBreakConstraint()
      # library.solve()
    
    elif constraintID == 'NonDivisionalOpponent':
      library.addNonDivisionalOpponentConstraint()
      # library.solve()

    elif constraintID == 'EastToWestMaxTwoTravel':
      library.addEastToWestMaxTwoTravelConstraint()
      # library.solve()
    
    elif constraintID == 'WestToEastMaxTwoTravel':
      library.addWestToEastMaxTwoTravelConstraint()
      # library.solve()

    elif constraintID == 'PlayNoMoreThanOnceThreeWeeks':
      library.addPlayNoMoreThanOnceThreeWeekConstraint()
      # library.solve()
    
    elif constraintID == 'EastTeamsHomeRoadMatchupInDivision':
      library.addEastTeamsHomeRoadMatchupInDivisionConstraint()
      # library.solve()
    elif constraintID == 'spacingOppRegionTrips':
      library.addSpacingOppRegionTripsConstraint()
      # library.solve()


## Here we simulate the deletion of a constraint (referenced by constraintID)
## from the agent's constraint library. Note that until we transition to Gurobi, where
## the constraints can be deleted, we will use this temporary approach though it's non-ideal
def deleteConstraint(library,constraintID):
    # print(f'delete constraint {constraintID} started')
    
    ## Since OR tools doesn't support constraint deletion, we will use a different (though non-ideal approach)
    ## clear the solver of the constraint library
    #env.library.__init__()

    ## write to the console while constraint  to be deleted. 
    # print(f'deleting constraint {constraintID}')

    ## Here, we are deleting movable constraints
    if constraintID == 'homeOneSideOfASG':

      library.allow_home_both_sides_ASG = False
    elif constraintID == 'NonDivisionalOpponent':
      library.upper_non_divisional_games = 3
    
    elif constraintID == 'EastTeamsHomeRoadMatchupInDivision':
      library.eastern_one_to_two = True
      library.eastern_two_to_two = True
      library.eastern_two_to_one = True

    elif constraintID == 'EastToWestMaxTwoTravel':

      library.max_east_to_west_trips = 2
    
    elif constraintID == 'WestToEastMaxTwoTarvel':
      library.max_west_to_east_trips = 2

    elif constraintID == 'PlayNoMoreThanOnceThreeWeeks':
      library.max_play_same_opponent = 1

    elif constraintID == 'spacingOppRegionTrips':
      library.trips_bet_opp_region_spaced = True


    # ## get all the constraints that has been added and satisfied, which is not the constraint
    # ## id to be deleted.
    # constraint_remaining = [constr for constr in library.satisfied_constraints if constr != constraintID]
    constraintToDelete = []

    for constr in library.solver.getConstrs():
        if constr.ConstrName == constraintID:
            constraintToDelete.append(constr)
    #constraintsToDelete = library.solver.getConstrByName(constraintID)

    library.solver.remove(constraintToDelete)

    library.solver.update()

    library.solver.optimize()
    #
    # ## We print that we are resetting the constraints when we are deleting
    # print('Resetting the constraints')
    #
    # ## We add all the constraints that are satisfied before the delete (excluding the
    # ## constraint to be deleted)
    # for constr in constraint_remaining:
    #   addConstraint(library,constr)

## substituting a constraint (applies to both immovable and movable constraints)
def substituteConstraint(library,old_constraint,new_constraint):
    deleteConstraint(library,old_constraint)
    addConstraint(library,new_constraint)

## modifying a constraint (movable only)
def modifyConstraint(library,movable_constraint_to_modify):

  ## We first need to delete the original constraint before we can modify it
  deleteConstraint(library,movable_constraint_to_modify)

  ## we are still considering these possibilities to test that our DQN works
  ## will likely add more after SABR or as we get more testing 
  ## we will determine the limit as to the amount of modify (we now aim to keep 
  ## it simply for the purpose of testing our DQN for the movable constraints)
  ## adding movable constraints
  if  movable_constraint_to_modify== 'homeOneSideOfASG':
      library.allow_home_both_sides_ASG = True
    
  elif movable_constraint_to_modify == 'NonDivisionalOpponent':
      ## upper bound on the number of non_divisional_games to be 5 (to which we can modify)
      library.upper_non_divisional_games = 5
  
  elif movable_constraint_to_modify == 'EastTeamsHomeRoadMatchupInDivision':
      ## we can modify it to be that we do not include 1-2,2-2,and 2-2
      ## based on the problem, we can try different modification schemes later on
      library.eastern_one_to_two = False
      library.eastern_two_to_two = False
      library.eastern_two_to_one = False

  elif movable_constraint_to_modify == 'EastToWestMaxTwoTravel':
      ## we can relax it to 3, but 3 is immovable
      library.max_east_to_west_trips = 3
    
  elif movable_constraint_to_modify == 'WestToEastMaxTwoTarvel':
      ## we can relax the upper bound to trips from west to east but 3 is immovable
      library.max_west_to_east_trips = 3

  elif movable_constraint_to_modify == 'PlayNoMoreThanOnceThreeWeeks':
      ## play no more than upper_bound times during 3 weeks
      ## per the problem, we can set different upper bound (but we will focus on at most 5)
      library.max_play_same_opponent = 5

  elif movable_constraint_to_modify == 'spacingOppRegionTrips':
      ## modify it to allow no spacing between trips of opposite region
      library.trips_bet_opp_region_spaced = False

  ## add the modified version of the constraint
  addConstraint(library,movable_constraint_to_modify)