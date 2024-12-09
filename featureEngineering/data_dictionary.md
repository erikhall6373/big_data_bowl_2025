# Data Dictionary For Fields in Feature Store



| Feature                        | Description
| :------------------------------| :----------
| gameId                         | Game identifier, unique (numeric)
| playId                         | Play identifier, not unique across games (numeric)
| nflId                          | Player identification number, unique across players (numeric)
| defender_nflId                 | The nflId associated with the primary defender of a particular receiver
| quarter                        | Game quarter (numeric)
| down                           | Down (numeric)
| yardsToGo                      | Distance needed for a first down (numeric)
| possessionTeam                 | Team abbr of team on offense with possession of ball (text)
| teamAbbr                       | The team abbreviation for the team the player plays for (text)
| passResult                     | Dropback outcome of the play (C: Complete pass, I: Incomplete pass, S: Quarterback sack, IN: Intercepted pass, R: Scramble, text)
| offenseFormation               | Formation used by possession team (text)
| receiverAlignment              | Enumerated as 0x0, 1x0, 1x1, 2x0, 2x1, 2x2, 3x0, 3x1, 3x2 (text)
| playAction                     | Boolean indicating whether there was play-action on the play (Boolean)
| timeToThrow                    | The time (secs) elapsed between snap and pass (numeric)
| inMotionAtBallSnap             | Boolean indicating whether the player was in motion at snap; Rule: If a player is moving faster than 0.62 y/s in the window 0.4 seconds prior to the ball snap, and has moved at least 1.2 yards in that window. (Boolean)
| shiftSinceLineset              | Boolean indicating whether the player shifted since the lineset; Rule: Each player has their own lineset moment, and whether they shift is based on if they move more than 2.5 yards from where they were at their lineset moment. (Boolean)
| motionSinceLineset             | Boolean indicating whether the player went in motion after they were initially set at the line on this play (Boolean)
| wasRunningRoute                | Boolean indicating if the player was running a route on this play (Boolean)
| routeRan                       | The name of the route ran by the player on this play (text)
| playNullifiedByPenalty         | Whether or not an accepted penalty on the play cancels the play outcome. Y stands for yes and N stands for no. (text)
| separation_yardage             | The Euclidean distance between a receiver and the primary defender on a given play
