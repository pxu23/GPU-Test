## Non divisional opponents series for the Western and Eastern clubs
## upper bound denotes an upper bound on the number of series
## to modify this, we can increase the upper bound to some value (say 5)
## by default, the lower_bound is 0 and the upper_bound is 3
def addNonDivisonalOpponent(constraintLibrary, upper_bound):
    ## A team from the West plays a team from the East
    for team in constraintLibrary.east_teams:
        for opposing_team in constraintLibrary.west_teams:
            east_non_divisional_series_with_west_team = 0
            # travel constraint combined: six eastern clubs have maximum of two trips to the west
            for s in constraintLibrary.series:
                east_non_divisional_series_with_west_team += (constraintLibrary.assignments[(s, opposing_team, team)] +
                                                              constraintLibrary.assignments[(s, team, opposing_team)])

            constraintLibrary.solver.addConstr(east_non_divisional_series_with_west_team >= 0,name = 'NonDivisionalOpponent')
            constraintLibrary.solver.addConstr(east_non_divisional_series_with_west_team <= upper_bound,name = 'NonDivisionalOpponent')


    ## A team from the East plays a team from the West
    for team in constraintLibrary.west_teams:
        for opposing_team in constraintLibrary.east_teams:
            west_non_divisional_series_with_east_team = 0
            for s in constraintLibrary.series:
                west_non_divisional_series_with_east_team += (constraintLibrary.assignments[(s, opposing_team, team)] +
                                                              constraintLibrary.assignments[(s, team, opposing_team)])

            constraintLibrary.solver.addConstr(west_non_divisional_series_with_east_team >= 0,
                                               name='NonDivisionalOpponent')
            constraintLibrary.solver.addConstr(west_non_divisional_series_with_east_team <= upper_bound,
                                         name = 'NonDivisionalOpponent')

    constraintLibrary.solver.update()