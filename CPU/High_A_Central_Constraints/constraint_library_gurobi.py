from gurobipy import *

from High_A_Central_Constraints.constants import all_dates
from High_A_Central_Constraints.immovable_constraints.total_games_constraint import addTotal132Games
from High_A_Central_Constraints.immovable_constraints.allSeriesSixGamesWithTwoExceptions_constraint import addAllSeriesSixGamesWithTwoExceptionsConstraint
from High_A_Central_Constraints.immovable_constraints.WesternClubMatchup_constraint import addWestTeamsHomeRoadMatchupInDivision
from High_A_Central_Constraints.immovable_constraints.threeSeriesMatchups import addCertainMatchupGuaranteedThreeSeries

from High_A_Central_Constraints.movable_constraints.spacingOpponentRegionalTrips import addSpacingOppRegionTripsConstraint
from High_A_Central_Constraints.immovable_constraints.southBendAllEasternClubsOnce_constraint import addSouthBendPlayAllEasternClubOnce
from High_A_Central_Constraints.immovable_constraints.playInEverySlot_constraint import addPlayInEverySlot
from High_A_Central_Constraints.immovable_constraints.noPlayASGBreak_constraint import addNoPlayOnASGBreak
from High_A_Central_Constraints.movable_constraints.nonDivisinoalMatchup import addNonDivisonalOpponent
from High_A_Central_Constraints.movable_constraints.maxTravelEastToWest_constraint import addEastToWestMaxTwoTravel
from High_A_Central_Constraints.immovable_constraints.homeAwayPerGame_constraint import addSetHomeAwayPerGame
from High_A_Central_Constraints.movable_constraints.home_asg_break_constraint import addHomeOnOneSideOfASGBreak
from High_A_Central_Constraints.immovable_constraints.EasternClubTwoToTwo_constraint import addEasternClubsGuaranteeCertainMatchup
from High_A_Central_Constraints.movable_constraints.EasternClubMixMatchupInDivision_constraint import addEastTeamsHomeRoadMatchupInDivision
from High_A_Central_Constraints.movable_constraints.playNoMoreThanOnceSameOpponentThreeWeeks_constraint import addPlayNoMoreThanOnceThreeWeek
from High_A_Central_Constraints.immovable_constraints.hostNoMoreThanOnceSameOpponentFourWeeks_constraint import addHostNoMoreThanOnceFourWeek
from High_A_Central_Constraints.movable_constraints.maxTravelWestToEast_constraint import addWestToEastMaxTwoTravel


#print('total number of weeks in season is ',math.ceil(num_days / 7))


class BaseballSchedulingConstraintLibraryGurobi:
    ## This class represents the constraint library for the OR tools.
    ## In this constraint library, we will have the solve methods that solves
    ## the OR tools problem with the constraints added. In each of the methods where
    ## we add a constraint, we call the constraint in the methods defined above while
    ## passing in the constraint library (which is self - the class)
    def __init__(self):
        self.solver = Model()

        self.solver.Params.LogToConsole = 0

        ## creates a pywraplp solver

        ## the dictionary of assignments of teams to series
        self.assignments = {}

        ## 23 series with 6 games each (from Wikipedia)
        self.series = range(1, 24)

        ## the teams in the East division
        self.east_teams = ['Dayton Dragons', 'Fort Wayne TinCaps', 'Great Lakes Loons',
                           'Lake County Captains', 'Lansing Lugnuts', 'West Michigan Whitecaps']

        ## the teams in the West division
        self.west_teams = ['Beloit Sky Carp', 'Cedar Rapids Kernels', 'Peoria Cheifs',
                            'Quad Cities River Bandits', 'South Bend Cubs', 'Wisconsin Timber Rattlers']

        # all High A Central teams
        self.teams = self.east_teams + self.west_teams

        ## division dictionary (assignment of teams to divisions)
        self.team_divisions = {}
        for team in self.teams:
            if team in self.east_teams:
                self.team_divisions[team] = 'east'
            elif team in self.west_teams:
                self.team_divisions[team] = 'west'

        ## we will also define an internal constraint library for use in the AI gym framework
        self.constraints = {}

        ## boolean to show if an optimal solution exists after constraints are added
        self.isOptimal = False  ## default false

        ## boolean value to show if the problem is infeasible
        self.isInfeasible = False  ## default false

        ## sets up the binary decision variables of assignments of home and away teams
        ## to the series
        for s in self.series:
            for away_team in self.teams:
                for home_team in self.teams:
                    if away_team != home_team:
                        var_name = f'X_{s}{away_team}{home_team}'
                        variable = self.solver.addVar(vtype='B', name=var_name)
                        self.assignments[(s, away_team, home_team)] = variable



        ## the dictionary representing the assignment of series to dates in the High
        ## A Central season
        self.series_dates = {}

        # ## creates binary decision variables of assignments of series to datas in the
        # ## High A Central season
        for s in self.series:
             for day in all_dates:
                 var_name = f'Y_{s}{day.strftime("%m/%d/%Y")}'
                 variable = self.solver.addVar(vtype='B', name=var_name)
                 self.series_dates[(s, day)] = variable



        ## we represent the value of the parameters in the movable constraints
        ## are trips between opposite regions spaced? (default 2)
        self.trips_bet_opp_region_spaced = True

        ## max number of times east can travel to west (default 2)
        self.max_east_to_west_trips = 2

        self.max_west_to_east_trips = 2

        ## maximum number of times a team can play the same opponent in three week period
        # default is 1
        self.max_play_same_opponent = 1

        ## is Eastern clubs matchup mix 1-2, 2-2,2-1 (default all True)
        self.eastern_one_to_two = True
        self.eastern_two_to_two = True
        self.eastern_two_to_one = True

        ## can clubs be home on both sides of ASG break (default no)
        self.allow_home_both_sides_ASG = False

        ## upper bound on non-divisional games (default 3)
        self.upper_non_divisional_games = 3

        ## assumption that we play in each slot
        self.addPlayInEverySlotConstraint()

    ## the constraint of playing in every slot
    def addPlayInEverySlotConstraint(self):

        addPlayInEverySlot(self)

    ## the constraint of home on one side of the ASG break
    ## can be modified (movable) to allow home on both sides of ASG break
    def addHomeOnOneSideOfASGBreakConstraint(self):
            ## calls the home on one side of ASG break defined above (passing in self as
            ## the constraintLibrary)
            #self.playInEverySlot()
        addHomeOnOneSideOfASGBreak(self, self.allow_home_both_sides_ASG)

    ## Each slot (or game) is home or away (interpreation:
    ## if one team plays another during one slot (or game)
    # , one is home and another is away)
    def addSetHomeAwayPerGameConstraint(self):
            ## calls the setHomeAwayPerGame constraint defined above (passing in self
            ## as the constraintLibrary)
            #self.playInEverySlot()
            #addSetHomeAwayPerGame(self)
        addSetHomeAwayPerGame(self)

        ## the constraint of south Bend playing all Eastern club once
    def addSouthBendPlayAllEasternClubOnceConstraint(self):
            ## calls the southBendPlayAllEasternClubOnce constraint defined above
            ## (passing in self as the constraintLibrary)
            #self.playInEverySlot()
        addSouthBendPlayAllEasternClubOnce(self)
            # for team in self.east_teams:
            #     sum = 0
            #     for s in self.series:
            #         sum = sum + (self.assignments[(s, team, 'South Bend Cubs')]
            #                      + self.assignments[(s, "South Bend Cubs", team)])
            #     self.solver.addConstr(sum >= 1, name='SouthBendRequiredToPlayAllEasternClubsOnce')

        ## For the Eastern Clubs, certain matchups are guaranteed 2-2
    def addEasternClubsGuaranteeCertainMatchupConstraint(self):
            ## calls the EasternClubGuaranteeCertainMatchup constraint define above
            ## (passing in self as the constraintLibrary)
            #self.playInEverySlot()
        addEasternClubsGuaranteeCertainMatchup(self)


    def addAllSeriesSixGamesWithTwoExceptionsConstraint(self):
        addAllSeriesSixGamesWithTwoExceptionsConstraint(self)

    ## For the eastern clubs we have a mix of 1-2,2-1,2-2
    ## All Western clubs have a minimum of 1-1 and maximum of 2-2 in division
    ## WIS and BEL has minimum of 1-1 and maximum of 2-2

    def addEastTeamsHomeRoadMatchupInDivisionConstraint(self):
             ## calls the EastTeamsHomeRoadMatchupInDivision constraint defined above
             ## (passing in self as the constraintLibrary)
             #self.playInEverySlot()
             addEastTeamsHomeRoadMatchupInDivision(self, self.eastern_one_to_two,
                                                self.eastern_two_to_one,
                                                self.eastern_two_to_two)


        ## All Western clubs have a minimum of 1-1 and maximum of 2-2 in division
        ## WIS and BEL has minimum of 1-1 and maximum of 2-2
    def addWestTeamsHomeRoadMatchupInDivisionConstraint(self):
            ## calls the WestTeamsHomeRoadMatchupInDivision constraint defined above
            ## (passing in self as the constraintLibrary)
            #self.playInEverySlot()
        addWestTeamsHomeRoadMatchupInDivision(self)

        ## Certain Matchups are guaranteed three series
    def addCertainMatchupGuaranteedThreeSeriesConstraint(self):
            ## calls the certainMatchupGuaranteedThreeSeries constraint defined above
            ## (passing in self as the constraintLibrary)
            #self.playInEverySlot()
        addCertainMatchupGuaranteedThreeSeries(self)

        ## Non divisional opponents series for the Western and Eastern clubs
        ## can modify based on lower and upper bound
    def addNonDivisionalOpponentConstraint(self):
            ## calls the NonDivisonalOpponent constraint defined above
            ## (passing in self as the constraintLibrary)
            #self.playInEverySlot()
        addNonDivisonalOpponent(self, self.upper_non_divisional_games)

        ## The east has a max of two trips to the west
        ## movable constraint (can be modified)
    def addEastToWestMaxTwoTravelConstraint(self):
            ## calls the EastToWestMaxTwoTravel constraint defined above
            ## (passing in self as the constraintLibrary)
            #self.playInEverySlot()
        addEastToWestMaxTwoTravel(self, self.max_east_to_west_trips)

            ## The West has a max of two trips to the East

        ## movable constraint (can be modified)
    def addWestToEastMaxTwoTravelConstraint(self):
            ## calls the WestToEastMaxTwoTravel constraint defined above
            ## (passing in self as the constraintLibrary)
            #self.playInEverySlot()
        addWestToEastMaxTwoTravel(self, self.max_west_to_east_trips)

            # Opponent Spacing

        # club cannot play the same opponent more than once within a 3-week period
        # applies to both eastern & western
        ## movable and can be modified to determine on the upper bound on the number of
        ## times a club can play the same opponent more than once in a 3-week period
    def addPlayNoMoreThanOnceThreeWeekConstraint(self):
            ## calls the PlayNoMoreThanOnceThreeWeek constraint defined above
            ## (passing in self as the constraintLibrary)
            #self.playInEverySlot()
        addPlayNoMoreThanOnceThreeWeek(self, self.max_play_same_opponent)

        ## A club cannot host more than once in a four week period
    def addHostNoMoreThanOnceFourWeekConstraint(self):
            ## calls the HostNoMoreThanOnceFourWeek defined above passing in self as the
            ## constraintLibrary
            #self.playInEverySlot()
        addHostNoMoreThanOnceFourWeek(self)

            ## Trips between oppostion region were spaced between each other (excluding SB)

        ## movable (can be modified to allow for no spacing)
    def addSpacingOppRegionTripsConstraint(self):
            ## calls the spacingOppRegionTrips constraint defined above passing in
            ## self as the constraintLibrary
            #self.playInEverySlot()
        addSpacingOppRegionTripsConstraint(self, self.trips_bet_opp_region_spaced)

        ## There are a total of 132 games in the baseball season
    def addTotal132GamesConstraint(self):
            ## calls the Total132Games constraint defined above passing in
            ## self as the constraintLibrary
            #self.playInEverySlot()
        addTotal132Games(self)

        ## There will be no play on the day of the ASG break
    def addNoPlayOnASGBreakConstraint(self):
            ## calls the noPlayOnASGBreak constraint defined above passing in
            ## self as the constraintLibrary
            #self.playInEverySlot()
        addNoPlayOnASGBreak(self)

    #     ## all series are 6 games with the exception of two 3-game series
    #def addAllSeriesSixGamesWithTwoExceptionsConstraint(self):
    #         ## calls the allSeriesSixGamesWithTwoExceptions constraint defined above
    #         ## passing in self as the constraintLibrary
    #         self.playInEverySlot()
    #    addAllSeriesSixGamesWithTwoExceptions(self)

        ## Once certain constraints have been added, we will then solve it to produce
        ## optimal sports schedules. We will do it for both solvers.
    def solve(self):
            ## solver solves the binary integer programming problem
            ## minimizes the objective
        ## we don't take into account distances yet so we just use the zero objective function for faster computation
        ## and scheduling
        self.solver.setObjective(0,GRB.MINIMIZE)
        #self.solver.setObjective(objective, gp.GRB.MINIMIZE)
        self.solver.optimize()
        self.solver.update()
        #print(f'Status is {self.solver.STATUS}')
        #print(f'Optimal status is {GRB.OPTIMAL} ')

        # print(f'Status is {self.solver.STATUS}')
        if self.solver.STATUS == GRB.OPTIMAL:
            self.isOptimal = True
            self.isInfeasible = False
        elif self.solver.STATUS == GRB.INFEASIBLE:
            self.isInfeasible = True
            self.isOptimal = False
        # self.solver_special_days.setObjective(quicksum(self.series_dates[(s,day)] for s in self.series
        #                                                 for day in all_dates),GRB.MINIMIZE)
        # self.solver_special_days.optimize()
        # self.solver_special_days.update()




'''def __init__(self):
        self.solver = gp.Model()
        self.eastern_clubs = ['a', 'b', 'c', 'd', 'e', 'f']
        self.western_clubs = ['g', 'h', 'i', 'j', 'k', 'l']
        self.series = range(1, 24)
        self.assignments = {}
        self.createVariables()

    def createVariables(self):
        for eastern_club in self.eastern_clubs:
            for western_club in self.western_clubs:
                for s in self.series:
                    var_name = f'X_{eastern_club}{western_club}{s}'
                    variable = self.solver.addVar(vtype='B', name=var_name)
                    self.assignments[(eastern_club, western_club, s)] = variable




    def addConstraint(self):
        index = 0
        index2 = 0
        for eastern_club in self.eastern_clubs:
            for western_club in self.western_clubs:
                num_play = 0
                name = f'Constraint_{index2}'
                index += 1

                if (index % 2 == 0):
                    index2 += 1
                for s in self.series:

                    num_play += self.assignments[(eastern_club,western_club,s)]
                self.solver.addConstr(num_play <= 1,name)

        self.solver.update()

    def solve(self):
        total = sum(self.assignments[(eastern_club,western_club,s)] for eastern_club in self.eastern_clubs
                  for western_club in self.western_clubs for s in self.series)
        self.solver.setObjective(total, gp.GRB.MAXIMIZE)
        self.solver.optimize()

    def printModel(self):
        # gets the name of the constraint
        print([constr.constrName for constr in self.solver.getConstrs()])

    def removeConstraint(self, constr_name):
        constrs_to_remove = [constr for constr in self.solver.getConstrs()
                             if constr.constrName == constr_name]
        self.solver.remove(constrs_to_remove)

        self.solver.update()
        print(f"removal of {constr_name} completed") 
        '''