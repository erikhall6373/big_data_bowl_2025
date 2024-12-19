# The Value of Players in Motion on Separation Yardage

## Introduction
One of the biggest advantages a defense has prior to the snap of the football is the ability for any player to move from their position without penalty.
The offense on the other hand can only have one player in motion at a time. The question is how can an offense best use a player in motion to their benefit? An example may 
be the identification of pass coverage, as a defender would follow a player in motion across the field. In this particular analysis though, we take a look at how a receiver 
in motion can affect their separation from the nearest defender.


## Does Separation Yardage Even Matter?
Before we even begin assessing the impact of motion on separation yardage, it is worth some investigation what value separation yardage even has. NFL next gen stats 
gives us some insight into how separation yardage is evaluated. One of those insight is the definition of a quarterback throwing in tight coverage, which is defined as 
coverage there is one yard or less worth of separation.

In the boxplots below we see pretty plainly that incompletions are more frequently tighter windows compared to completions. That said, any advantage around increasing 
separation yardage by even just one yard is of benefit to the offense.

## Model Methods
We trained a categorical boost regression model prediction separation yardage within 3 seconds of the snap of the ball. We choose this timeboxing as to reduce the variance 
of play outcome as separation yardage becomes more chaotic as play extends past the average amount of time to throw.

The features of consideration were

- X
- Y
- Z
  
## Highlights
Let's look at the receivers that the best at their craft in generating separation yards over expected, and see how motion took effect on a handful of plays.

## Future Work
If given more time the team would do a deeper dive into the tracking data to assess what would have happened if a player hadn't in gone motion. 
This requires restructing tracking data such that the recorded data would have to be altered to reflect the desired scenario.
## Appendix
Code is here blah....
