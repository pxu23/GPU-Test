# Opponent Spacing
# club cannot play the same opponent more than once within a 3-week period
# applies to both eastern & western

## Since this constraint is movable, we can further relax it to be up to 3 times
## Note that the default of the max_play_of_same_opponent is once
def addPlayNoMoreThanOnceThreeWeek(constraintLibrary, max_play_of_same_opponent):
    for s in constraintLibrary.series:
        for curr_team in constraintLibrary.teams:
            for opposing_team in constraintLibrary.teams:
                num_play = 0
                if curr_team != opposing_team:
                    # means curr_team is playing against opposintg_team
                    # num_play += 1
                    if s >= 3:
                        # check on the previous two weeks and the current week
                        num_play += (constraintLibrary.assignments[(s, curr_team, opposing_team)]
                                     + constraintLibrary.assignments[(s, opposing_team, curr_team)]
                                     + constraintLibrary.assignments[(s - 1, curr_team, opposing_team)]
                                     + constraintLibrary.assignments[(s - 1, opposing_team, curr_team)]
                                     + constraintLibrary.assignments[(s - 2, curr_team, opposing_team)]
                                     + constraintLibrary.assignments[(s - 2, opposing_team, curr_team)])
                        # elif s == 2:
                        # check on the previous one week
                        #  num_play += (constraintLibrary.assignments[(s-1, curr_team, opposing_team)]
                        #               + constraintLibrary.assignments[(s-1, curr_team, opposing_team)]
                        #               + constraintLibrary.assignments[(s-1, opposing_team, curr_team)])

                        # if s == 1, num_play remain as 0
                        constraintLibrary.solver.addConstr(num_play <= max_play_of_same_opponent,
                                                     name='PlayNoMoreThanOnceThreeWeeks')
                        # no more than max_play_of_same_opponent

    constraintLibrary.solver.update()