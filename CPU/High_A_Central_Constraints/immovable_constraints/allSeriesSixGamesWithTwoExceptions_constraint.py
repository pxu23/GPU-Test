import datetime

from High_A_Central_Constraints.constants import all_dates


def addAllSeriesSixGamesWithTwoExceptionsConstraint(constraintLibrary):
    addFirstSerieThreeGames(constraintLibrary)
    addSecondSeriesSixGames(constraintLibrary)
    addThirdSeriesSixGames(constraintLibrary)
    addFourthSeriesSixGames(constraintLibrary)
    addFifthSeriesSixGames(constraintLibrary)
    addSixthSeriesSixGames(constraintLibrary)
    addSeventhSeriesSixGames(constraintLibrary)
    addEighthSeriesSixGames(constraintLibrary)
    addNinthSeriesSixGames(constraintLibrary)
    addTenthSeriesSixGames(constraintLibrary)
    addEleventhSeriesSixGames(constraintLibrary)
    addTwelfthSeriesSixGames(constraintLibrary)
    addThirteenthSeriesSixGames(constraintLibrary)
    addFourteenthSeriesSixGames(constraintLibrary)
    addFifteenthSeriesSixGames(constraintLibrary)
    addSixteenthSeriesThreeGames(constraintLibrary)
    addSeventeenthSeriesSixGames(constraintLibrary)
    addEighteenthSeriesSixGames(constraintLibrary)
    addNineteenthSeriesSixGames(constraintLibrary)
    addTwentiethSeriesSixGames(constraintLibrary)
    addTwentyFirstSeriesSixGames(constraintLibrary)
    addTwentySecondSeriesSixGames(constraintLibrary)
    TwentyThirdSeriesSixGames(constraintLibrary)


def addFirstSerieThreeGames(constraintLibrary):
    num_games_first_series = 0
    num_games_first_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 4, 8) and day <= datetime.datetime(2022, 4, 10):
            num_games_first_series += constraintLibrary.series_dates[(1, day)]
        else:
            num_games_first_series_outside_dates += constraintLibrary.series_dates[(1, day)]
    constraintLibrary.solver.addConstr(num_games_first_series == 3,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_first_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()


def addSecondSeriesSixGames(constraintLibrary):
    num_games_second_series = 0
    num_games_second_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 4, 11) and day <= datetime.datetime(2022, 4, 17):
            num_games_second_series += constraintLibrary.series_dates[(2, day)]
        else:
            num_games_second_series_outside_dates += constraintLibrary.series_dates[(2, day)]

    constraintLibrary.solver.addConstr(num_games_second_series == 6,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_second_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()


def addThirdSeriesSixGames(constraintLibrary):
    num_games_third_series = 0
    num_games_third_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 4, 18) and day <= datetime.datetime(2022, 4, 24):
            num_games_third_series += constraintLibrary.series_dates[(3, day)]
        else:
            num_games_third_series_outside_dates += constraintLibrary.series_dates[(3, day)]
    constraintLibrary.solver.addConstr(num_games_third_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_third_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addFourthSeriesSixGames(constraintLibrary):
    num_games_fourth_series = 0
    num_games_fourth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 4, 25) and day <= datetime.datetime(2022, 5, 1):
            num_games_fourth_series += constraintLibrary.series_dates[(4, day)]
        else:
            num_games_fourth_series_outside_dates += constraintLibrary.series_dates[(4, day)]

    constraintLibrary.solver.addConstr(num_games_fourth_series == 6,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_fourth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addFifthSeriesSixGames(constraintLibrary):
    num_games_fifth_series = 0
    num_games_fifth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 5, 2) and day <= datetime.datetime(2022, 5, 8):
            num_games_fifth_series += constraintLibrary.series_dates[(5, day)]
        else:
            num_games_fifth_series_outside_dates += constraintLibrary.series_dates[(5, day)]

    constraintLibrary.solver.addConstr(num_games_fifth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_fifth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addSixthSeriesSixGames(constraintLibrary):
    num_games_sixth_series = 0
    num_games_sixth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 5, 9) and day <= datetime.datetime(2022, 5, 15):
            num_games_sixth_series += constraintLibrary.series_dates[(6, day)]
        else:
            num_games_sixth_series_outside_dates += constraintLibrary.series_dates[(6, day)]

    constraintLibrary.solver.addConstr(num_games_sixth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_sixth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addSeventhSeriesSixGames(constraintLibrary):
    num_games_seventh_series = 0
    num_games_seventh_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 5, 16) and day <= datetime.datetime(2022, 5, 22):
            num_games_seventh_series += constraintLibrary.series_dates[(7, day)]
        else:
            num_games_seventh_series_outside_dates += constraintLibrary.series_dates[(7, day)]

    constraintLibrary.solver.addConstr(num_games_seventh_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_seventh_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addEighthSeriesSixGames(constraintLibrary):
    num_games_eigth_series = 0
    num_games_eigth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 5, 23) and day <= datetime.datetime(2022, 5, 29):
            num_games_eigth_series += constraintLibrary.series_dates[(8, day)]
        else:
            num_games_eigth_series_outside_dates += constraintLibrary.series_dates[(8, day)]
    constraintLibrary.solver.addConstr(num_games_eigth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_eigth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

## Memorial day on 5/30/2022 Monday
def addNinthSeriesSixGames(constraintLibrary):
    num_games_ninth_series = 0
    num_games_ninth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 5, 30) and day <= datetime.datetime(2022, 6, 5):
            num_games_ninth_series += constraintLibrary.series_dates[(9, day)]
        else:
            num_games_ninth_series_outside_dates += constraintLibrary.series_dates[(9, day)]

    constraintLibrary.solver.addConstr(num_games_ninth_series_outside_dates == 0,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_ninth_series == 6,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addTenthSeriesSixGames(constraintLibrary):
    num_games_tenth_series = 0
    num_games_tenth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 6, 6) and day <= datetime.datetime(2022, 6, 12):
            num_games_tenth_series += constraintLibrary.series_dates[(10, day)]
        else:
            num_games_tenth_series_outside_dates += constraintLibrary.series_dates[(10, day)]

    constraintLibrary.solver.addConstr(num_games_tenth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_tenth_series_outside_dates == 0,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addEleventhSeriesSixGames(constraintLibrary):
    num_games_eleventh_series = 0
    num_games_eleventh_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 6, 13) and day <= datetime.datetime(2022, 6, 19):
            num_games_eleventh_series += constraintLibrary.series_dates[(11, day)]
        else:
            num_games_eleventh_series_outside_dates += constraintLibrary.series_dates[(11, day)]

    constraintLibrary.solver.addConstr(num_games_eleventh_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_eleventh_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addTwelfthSeriesSixGames(constraintLibrary):
    num_games_twelfth_series = 0
    num_games_twelfth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 6, 20) and day <= datetime.datetime(2022, 6, 26):
            num_games_twelfth_series += constraintLibrary.series_dates[(12, day)]
        else:
            num_games_twelfth_series_outside_dates += constraintLibrary.series_dates[(12, day)]
    constraintLibrary.solver.addConstr(num_games_twelfth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_twelfth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addThirteenthSeriesSixGames(constraintLibrary):
    num_games_thirteenth_series = 0
    num_games_thirteenth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 6, 27) and day <= datetime.datetime(2022, 7, 3):
            num_games_thirteenth_series += constraintLibrary.series_dates[(13, day)]
        else:
            num_games_thirteenth_series_outside_dates += constraintLibrary.series_dates[(13, day)]
    constraintLibrary.solver.addConstr(num_games_thirteenth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_thirteenth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

## Monday July 4th is independence day
def addFourteenthSeriesSixGames(constraintLibrary):
    num_games_fourteenth_series = 0
    num_games_fourteenth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 7, 4) and day <= datetime.datetime(2022, 7, 10):
            num_games_fourteenth_series += constraintLibrary.series_dates[(14, day)]
        else:
            num_games_fourteenth_series_outside_dates += constraintLibrary.series_dates[(14, day)]
    constraintLibrary.solver.addConstr(num_games_fourteenth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_fourteenth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addFifteenthSeriesSixGames(constraintLibrary):
    num_games_fifteenth_series = 0
    num_games_fifteenth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 7, 11) and day <= datetime.datetime(2022, 7, 17):
            num_games_fifteenth_series += constraintLibrary.series_dates[(15, day)]
        else:
            num_games_fifteenth_series_outside_dates += constraintLibrary.series_dates[(15, day)]

    constraintLibrary.solver.addConstr(num_games_fifteenth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_fifteenth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addSixteenthSeriesThreeGames(constraintLibrary):
    num_games_sixteenth_series = 0
    num_games_sixteenth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 7, 22) and day <= datetime.datetime(2022, 7, 24):
            num_games_sixteenth_series += constraintLibrary.series_dates[(16, day)]
        else:
            num_games_sixteenth_series_outside_dates += constraintLibrary.series_dates[(16, day)]

    constraintLibrary.solver.addConstr(num_games_sixteenth_series_outside_dates == 0,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_sixteenth_series == 3,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addSeventeenthSeriesSixGames(constraintLibrary):
    num_games_seventeenth_series = 0
    num_games_seventeenth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 7, 25) and day <= datetime.datetime(2022, 7, 31):
            num_games_seventeenth_series += constraintLibrary.series_dates[(17, day)]
        else:
            num_games_seventeenth_series_outside_dates += constraintLibrary.series_dates[(17, day)]

    constraintLibrary.solver.addConstr(num_games_seventeenth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_seventeenth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addEighteenthSeriesSixGames(constraintLibrary):
    num_games_eighteenth_series = 0
    num_games_eighteenth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 8, 1) and day <= datetime.datetime(2022, 8, 7):
            num_games_eighteenth_series += constraintLibrary.series_dates[(18, day)]
        else:
            num_games_eighteenth_series_outside_dates += constraintLibrary.series_dates[(18, day)]

    constraintLibrary.solver.addConstr(num_games_eighteenth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_eighteenth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addNineteenthSeriesSixGames(constraintLibrary):
    num_games_nineteenth_series = 0
    num_games_nineteenth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 8, 8) and day <= datetime.datetime(2022, 8, 14):
            num_games_nineteenth_series += constraintLibrary.series_dates[(19, day)]
        else:
            num_games_nineteenth_series_outside_dates += constraintLibrary.series_dates[(19, day)]

    constraintLibrary.solver.addConstr(num_games_nineteenth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_nineteenth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addTwentiethSeriesSixGames(constraintLibrary):
    num_games_twentieth_series = 0
    num_games_twentieth_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 8, 15) and day <= datetime.datetime(2022, 8, 21):
            num_games_twentieth_series += constraintLibrary.series_dates[(20, day)]
        else:
            num_games_twentieth_series_outside_dates += constraintLibrary.series_dates[(20, day)]

    constraintLibrary.solver.addConstr(num_games_twentieth_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_twentieth_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addTwentyFirstSeriesSixGames(constraintLibrary):
    num_games_twenty_first_series = 0
    num_games_twenty_first_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 8, 22) and day <= datetime.datetime(2022, 8, 28):
            num_games_twenty_first_series += constraintLibrary.series_dates[(21, day)]
        else:
            num_games_twenty_first_series_outside_dates += constraintLibrary.series_dates[(21, day)]
    constraintLibrary.solver.addConstr(num_games_twenty_first_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_twenty_first_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def addTwentySecondSeriesSixGames(constraintLibrary):
    num_games_twenty_second_series = 0
    num_games_twenty_second_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 8, 29) and day <= datetime.datetime(2022, 9, 4):
            num_games_twenty_second_series += constraintLibrary.series_dates[(22, day)]
        else:
            num_games_twenty_second_series_outside_dates += constraintLibrary.series_dates[(22, day)]
    constraintLibrary.solver.addConstr(num_games_twenty_second_series == 6,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_twenty_second_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()

def TwentyThirdSeriesSixGames(constraintLibrary):
    num_games_twenty_third_series = 0
    num_games_twenty_third_series_outside_dates = 0
    for day in all_dates:
        if day >= datetime.datetime(2022, 9, 5) and day <= datetime.datetime(2022, 9, 11):
            num_games_twenty_third_series += constraintLibrary.series_dates[(23, day)]
        else:
            num_games_twenty_third_series_outside_dates += constraintLibrary.series_dates[(23, day)]
    constraintLibrary.solver.addConstr(num_games_twenty_third_series == 6,name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.addConstr(num_games_twenty_third_series_outside_dates == 0,
                                       name='AllSeriesSixGamesWithTwoThreeGame')
    constraintLibrary.solver.update()