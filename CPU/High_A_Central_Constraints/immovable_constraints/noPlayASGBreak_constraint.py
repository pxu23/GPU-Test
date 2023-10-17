import datetime

## Here we have a method in which there can be no play at all on the day of the
## ASG break. Note that the days of the ASG break is 7/18-7/22,2022
def addNoPlayOnASGBreak(constraintLibrary):
  num_games_on_break = 0
  for s in constraintLibrary.series:
    num_games_on_break += constraintLibrary.series_dates[(s,datetime.datetime(2022,7,18))]
    num_games_on_break += constraintLibrary.series_dates[(s,datetime.datetime(2022,7,19))]
    num_games_on_break += constraintLibrary.series_dates[(s,datetime.datetime(2022,7,20))]
    num_games_on_break += constraintLibrary.series_dates[(s,datetime.datetime(2022,7,21))]
  constraintLibrary.solver_special_days.addConstr(num_games_on_break == 0,name='NoPlayOnASGBreak')

  constraintLibrary.solver.update()



