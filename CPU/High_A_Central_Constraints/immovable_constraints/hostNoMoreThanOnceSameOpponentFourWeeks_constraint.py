## a club cannot host the same opponent more than once in four weeks

def addHostNoMoreThanOnceFourWeek(constraintLibrary):
    for curr_team in constraintLibrary.teams:
        for opposing_team in constraintLibrary.teams:
            num_host = 0
            if curr_team != opposing_team:
                for s in constraintLibrary.series:
                    # num_host += 1
                    if s >= 4:
                        # check on previous 3 weeks
                        num_host += (constraintLibrary.assignments[(s, opposing_team, curr_team)]
                                     + constraintLibrary.assignments[(s - 1, opposing_team, curr_team)]
                                     + constraintLibrary.assignments[(s - 2, opposing_team, curr_team)]
                                     + constraintLibrary.assignments[(s - 3, opposing_team, curr_team)])
                        # elif s == 3:
                #  num_host += (constraintLibrary.assignments[(s-1, opposing_team, curr_team)]
                #               + constraintLibrary.assignments[(s-2, opposing_team, curr_team)])
                # elif s == 2:
                #  num_host += (constraintLibrary.assignments[(s-1, opposing_team, curr_team)])
            constraintLibrary.solver.addConstr(num_host <= 1,
                                         name='ClubCannotHostMoreThanOnceInFourWeekPeriod')

    constraintLibrary.solver.update()