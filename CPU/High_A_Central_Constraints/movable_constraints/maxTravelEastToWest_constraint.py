## by default, the max_trips_to_west is 2 but can be relaxed to 3 which is immovable
## Eastern clubs have a max of two trips to the west
def addEastToWestMaxTwoTravel(constraintLibrary, max_trips_to_west):
    for team in constraintLibrary.east_teams:
        east_travel_western_home = 0
        for s in constraintLibrary.series:
            for opposing_team in constraintLibrary.west_teams:
                east_travel_western_home += constraintLibrary.assignments[
                    (s, team, opposing_team)]  # away in team means traveling to western team

        # adding of travel constraint here
        constraintLibrary.solver.addConstr(east_travel_western_home >= 0,
                                           name = 'EastToWestMaxTwoTravel')
        constraintLibrary.solver.addConstr(east_travel_western_home <= max_trips_to_west,
                                           name = 'EastToWestMaxTwoTravel')

    constraintLibrary.solver.update()