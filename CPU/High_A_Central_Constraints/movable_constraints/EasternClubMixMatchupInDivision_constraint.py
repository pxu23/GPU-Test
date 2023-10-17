## For the eastern clubs we have a mix of 1-2,2-1,2-2
## Note here that the boolean variables OneToTwoIncluded, TwoToOneIncluded,
## and TwoToTwoIncluded are by default true, but to modify this constraint
## any of the boolean variables can be set to false.
def addEastTeamsHomeRoadMatchupInDivision(constraintLibrary, OneToTwoIncluded,
                                        TwoToOneIncluded, TwoToTwoIncluded):
     for i in range(len(constraintLibrary.east_teams) - 1):
         for j in range(i + 1, len(constraintLibrary.east_teams)):
             team_one = constraintLibrary.east_teams[i]
             team_two = constraintLibrary.east_teams[j]
             matchup = (team_one, team_two)

             num_home_teamone = 0
             for s in constraintLibrary.series:
                 num_home_teamone += constraintLibrary.assignments[(s, team_two, team_one)]
#
             num_home_teamtwo = 0
             for s in constraintLibrary.series:
                 num_home_teamtwo += constraintLibrary.assignments[(s, team_one, team_two)]
#
             if OneToTwoIncluded:
                 if TwoToTwoIncluded:
                     if TwoToOneIncluded:
                         constraintLibrary.solver.addConstr(num_home_teamone >= 1,name='EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamone <= 2,name='EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo >= 1,
                                                            name='EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo <= 2,
                                                            name='EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo + num_home_teamone >= 3,
                                                            name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamone + num_home_teamtwo <= 4,
                                                            name = 'EastTeamsHomeRoadMatchupInDivision')

                     else:  # TwoToOne not included but 1-2 and 2-2 included
                         constraintLibrary.solver.addConstr(num_home_teamtwo == 2,name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamone >= 1,name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamone <= 2,name = 'EastTeamsHomeRoadMatchupInDivision')
                         # constraintLibrary.solver.addConstr((num_home_teamone == 2 and num_home_teamtwo == 2)
                         #                              or (num_home_teamone == 1 and num_home_teamtwo == 2),
                         #                                    name = 'EastTeamsHomeRoadMatchupInDivision')
                 else:  # 1-2 included but 2-2 not included
                     if TwoToOneIncluded: # 1-2 included, 2-1 included, but 2-2 not included
                         constraintLibrary.solver.addConstr(num_home_teamone >= 1,name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamone <= 2,name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo >= 1,name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo <= 2,name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo + num_home_teamone == 3, name = 'EastTeamsHomeRoadMatchupInDivision')
                         # constraintLibrary.solver.addConstr((num_home_teamone == 1 and num_home_teamtwo == 2)
                         #                              or (num_home_teamone == 2 and num_home_teamtwo == 1),
                         #                                    name = 'EastTeamsHomeRoadMatchupInDivision')
                     else:  ## 1-2 included, 2-2 not included, and 2-1 not included
                         constraintLibrary.solver.addConstr(num_home_teamone == 1,name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo == 2,name = 'EastTeamsHomeRoadMatchupInDivision')
                         # constraintLibrary.solver.addConstr((num_home_teamone == 1 and num_home_teamtwo == 2),
                         #                                    name = 'EastTeamsHomeRoadMatchupInDivision')
             else:  # 1-2 not included
                 if TwoToTwoIncluded:  # 1-2 not included, 2-2 included
                     if TwoToOneIncluded:  # 1-2 not included, 2-2 included,2-1 included
                         constraintLibrary.solver.addConstr(num_home_teamone == 2, name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo >= 1, name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo <= 2, name = 'EastTeamsHomeRoadMatchupInDivision')
                         # constraintLibrary.solver.addConstr(((num_home_teamone == 2 and num_home_teamtwo == 2)
                         #                              or (num_home_teamone == 2 and num_home_teamtwo == 1)),
                         #                                    name = 'EastTeamsHomeRoadMatchupInDivision')
                     else:  # 1-2 and 2-1 not included but 2-2 included
                         constraintLibrary.solver.addConstr(num_home_teamtwo == 2, name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamone == 2, name = 'EastTeamsHomeRoadMatchupInDivision')
                         # constraintLibrary.solver.addConstr((num_home_teamone == 2 and num_home_teamtwo == 2),
                         #                                    name = 'EastTeamsHomeRoadMatchupInDivision')
                 else:  # 1-2 not included 2-2 not included
                     if TwoToOneIncluded:  # 1-2 not included, 2-2 not included, 2-1 included
                         constraintLibrary.solver.addConstr(num_home_teamone == 2,name = 'EastTeamsHomeRoadMatchupInDivision')
                         constraintLibrary.solver.addConstr(num_home_teamtwo == 1, name = 'EastTeamsHomeRoadMatchupInDivision')
                         # constraintLibrary.solver.addConstr((num_home_teamone == 2 and num_home_teamtwo == 1),
                         #                                    name = 'EastTeamsHomeRoadMatchupInDivision')

     constraintLibrary.solver.update()