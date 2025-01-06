# The Value of Pre-Snap Offensive Features on Separation Yardage

## Introduction
One of the biggest advantages a defense has prior to the snap of the football is the ability for any player to move from their position without penalty. Despite this, the offense still has a lot of advantages that they are in control of during pre-snap. Some of these advantages include knowledge of the snap count, and knowledge that a play will feature play-action. The offense can also arrange their players formationally to put blockers in the way of would be tacklers. Lastly, another advantageous impact is the ability to put a player in motion as to help identify defensvie coverage.

All of these are data points we've chosen to analyze as knowledge that an offense has pre-snap, and how that knowledge can influence the separation yardage between a defender and a receiver after the snap of the ball.


## Do Separation Yardage Even Matter?
Before we even begin assessing the impacts on separation yardage, it is worth some investigation into what value separation yardage even has. NFL next gen stats 
gives us some insight into how separation yardage is evaluated. One of those insights is the definition of a quarterback throwing in tight coverage, which is defined as coverage where there is one yard or less worth of separation between the defender and the receiver.

Knowing this definition of a tight coverage window, let's take a look at some boxplot comparing separation yardage across completed and incompleted passes. With regards to the data at hand, it worth note that these visuals and all of the analysis that follow are narrowed to pass plays featuring man-to-man coverage. This particular subset of data is the simplest way to define receivers and their assigned defenders on a particular play.

It appears that incompletions are more frequently in tighter windows compared to completions. That said, any advantage around increasing 
separation yardage by even just one yard is of benefit to the offense.

![Separation Boxplots](https://github.com/erikhall6373/big_data_bowl_2025/blob/main/writeUp/Separation_BoxPlots.png)

## Modeling
We trained a categorical boost regression model, predicting separation yardage within 3 seconds of the snap of the ball. We choose this timeboxing as to reduce the variance of play outcome as separation yardage becomes more chaotic as a play extends past the average amount of time to throw.

The features of consideration were

- **Down** (Down of the given play)
- **Yards to Go** (Distance needed for a first down)
- **Play Action** (Indicator of play-action a given play)
- **Motion Since Line Set** (Indicator of if a given player went in motion after they were initially set at the line on the given play)
- **Shift Since Line Set** (Indicator of if a given player moved more than 2.5 yards from where they were initiall set)
- **In Motion at Ball Snap** (Indicator of if a player is moving faster than 0.62 y/s in the window 0.4 seconds prior to the ball snap and has moved at least 1.2 yards in that window)
- **Receiver Alignment** (Categorial receiver formations eumerated as 0x0, 1x0, 1x1, 2x0, 2x1, 2x2, 3x0, 3x1, 3x2)
- **Route Ran** (Name of the route ran by the given player on the given play)
- **Receiver Speed** (Speed in yards/second of a given receiver)
- **Receiver Direction** (Angle in degrees of receiver while moving)
- **Defender Speed** (Speed in yards/second of a given defender)
- **Defender Direction** (Angle in degrees of defender while moving)
- **Net Distance in the X Direction** ("Cushion" between the receiver and defender at the time of the snap in the x direction - length of the field)
- **Net Distance in the Y Direction** ("Cushion" between the receiver and defender at the time of the snap in the y direction - width of the field)
- **Net Velocity in the X Direction** (Difference in speed moving the length of the field - X direction - between the receiver and defender at the time of the snap)
- **Net Velocity in the Y Direction** (Difference in speed moving the width of the field - Y direction - between the receiver and defender at the time of the snap)
- **Net Theta** (Difference in the direction of movement - angle - between the receiver and defender at the time of the snap)
- **Cushion Yardage** (Euclidean distance between a given receiver and defender at the time of the snap on a given play)


The regression model performed with a Training RMSE:  2.19 yards and a Validation RMSE:  2.41 yards. We can see that the pre-snap information is largely able to explain post-snap separation early in the play (within the first three seconds after the snap.)

![Model ScatterPlot](https://github.com/erikhall6373/big_data_bowl_2025/blob/main/writeUp/model_scatterplot.png)

Using this model, we can look a what pre-snap actions and positioning are most impactful to generating post-snap separation. We can calculate the importance of each feature in the model.

![Feature Importance](https://github.com/erikhall6373/big_data_bowl_2025/blob/main/writeUp/Feature_Importance.png)

As expected, the cushion at the time of the snap is the most important feature in explaining early post-snap separation. The route ran by receiver is the next most important feature to understanding separation. Below, we show the median expected separation for each route when the receiver is in motion and not in motion. For almost all routes, the median expected value is higher when the receiver is in motion.

![Median Separation by Route](https://github.com/erikhall6373/big_data_bowl_2025/blob/main/writeUp/Extra_Work_Motion_Comparison.png)

This model allows us to break early-play separation into two key components: that influenced by pre-snap actions and positions and that influenced by post-snap actions and positions. We can then evaluate each route ran to see how much separation is expected based on the pre-snap information, how much is influenced by post-snap actions, and how often a receiver exceeds the expectation.

  
## Highlights
In the spirit of the Expected Points Added metric, we've identified that one can evaluate player and team performance through added separation yardage. One can also evaluate a success rate of sorts based on how often a player or team is adding separation to a particular play.

Let's take a look at receiver performance with those two lenses;

First up being the receivers where Greg Dortch add separation on 64.23% of plays, and averages 0.72 extra separation yards. Tyreek Hill on the other hand does not add a lot of extra separation but, he more often than not is creating space on 50.76% of plays.

![Reciever Separation](https://github.com/erikhall6373/big_data_bowl_2025/blob/main/writeUp/receiver_separation_summary.png)

<br>
<br>

Defenders on the other hand want to be taking away separation yardage. And Devin Bush certainly appears to do a good job there by taking away 1.11 yards of expected separation. He also has only allowed gained expected separation on just under a quarter of his eligible plays.

![Defender Separation](https://github.com/erikhall6373/big_data_bowl_2025/blob/main/writeUp/defender_separation_summary.png)

<br>
<br>

Which teams do a good job getting receiver additional separation yardage? The Bills appear to lead the way there, where in the aggregate their receivers are adding almost quarter yard worth of separation, and they add separation on 50.53% of plays.

![Team Separation](https://github.com/erikhall6373/big_data_bowl_2025/blob/main/writeUp/team_separation_summary.png)


## Future Work
If given more time the team would do a much deeper dive into the tracking data around motion and it's impact on separation yardage. In our particular set of research, it remains as a high level analysis but with tracking data there's an opportunity to really dig into types of motion and their impact on separation yardage.

 
## Appendix
The code for the project can be found [here](https://github.com/erikhall6373/big_data_bowl_2025)
