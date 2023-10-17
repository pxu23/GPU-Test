## Western clubs have a maximum of two trips to the East
## Note that the max_trips_to_east is default 2, but can vary up to 3 (which is
## immovable)
def addWestToEastMaxTwoTravel(constraintLibrary, max_trips_to_east):
    for team in constraintLibrary.west_teams:
        if team != 'South Bend Cubs':
            west_travel_eastern_home = 0
            for s in constraintLibrary.series:
                for opposing_team in constraintLibrary.east_teams:
                    west_travel_eastern_home += (constraintLibrary.assignments[(s, opposing_team, team)] +
                                                 constraintLibrary.assignments[(s, team, opposing_team)])

                    # excluding SB
                    # if team != 'South Bend Cubs':
                    #  west_travel_eastern_home += self.assignments[(s,team, opposing_team)]

                # adding of travel constraint here
            constraintLibrary.solver.addConstr(west_travel_eastern_home >= 0,
                                               name='WestToEastMaxTwoTravel')
            constraintLibrary.solver.addConstr(west_travel_eastern_home <= max_trips_to_east,
                                               name = 'WestToEastMaxTwoTravel')

    constraintLibrary.solver.update()