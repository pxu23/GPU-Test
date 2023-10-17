## Trips between oppostion region were spaced between each other (excluding SB)
## if this constraint is modified to be relaxed, we can further set num_west_travels
## and num_east_travel to be both <= 2. We can set a boolean variable spaced to
## denote whether trips between opposite regions should be spaced (by default, it's true)
def addSpacingOppRegionTripsConstraint(constraintLibrary, spaced):
    for s in constraintLibrary.series:
        for curr_team in constraintLibrary.east_teams:
            for opposing_team in constraintLibrary.west_teams:
                num_west_travel = 0
                if s > 1:
                    num_west_travel += (constraintLibrary.assignments[(s, opposing_team, curr_team)]
                                        + constraintLibrary.assignments[(s - 1, opposing_team, curr_team)])

                if spaced:
                    constraintLibrary.solver.addConstr(num_west_travel <= 1,
                                                       name='spacingOppRegionTrips')
                else:
                    constraintLibrary.solver.addConstr(num_west_travel <= 2,
                                                       name='spacingOppRegionTrips')

    for s in constraintLibrary.series:
        for curr_team in constraintLibrary.west_teams:
            for opposing_team in constraintLibrary.east_teams:
                num_east_travel = 0
                if s > 1:
                    num_east_travel += (constraintLibrary.assignments[(s, opposing_team, curr_team)]
                                        + constraintLibrary.assignments[(s - 1, opposing_team, curr_team)])

                if spaced:
                    constraintLibrary.solver.addConstr(num_east_travel <= 1,
                                                       name='spacingOppRegionTrips')
                else:
                    constraintLibrary.solver.addConstr(num_east_travel <= 2,
                                                       name='spacingOppRegionTrips')

    constraintLibrary.solver.update()