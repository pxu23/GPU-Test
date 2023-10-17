import datetime

from High_A_Central_Constraints.constants import all_dates

def addTotal132Games(constraintLibrary):
    num_games = 0
    for s in constraintLibrary.series:
        for day in all_dates:
            num_games += constraintLibrary.series_dates[(s, day)]

    ## add the constraint to the constraint library's solver
    constraintLibrary.solver.addConstr(num_games == 132,name='EachClub132Games')

    constraintLibrary.solver.update()