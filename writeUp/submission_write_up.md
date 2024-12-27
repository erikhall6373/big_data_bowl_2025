# The Value of Pre-Snap Offensive Features on Separation Yardage

## Introduction
One of the biggest advantages a defense has prior to the snap of the football is the ability for any player to move from their position without penalty. Despite this, the offense still has a lot of advantages that they are in control of during pre-snap. Some of these advantages include knowledge of the snap count, and knowledge that a play will feature play-action. The offense can also arrange their players formationally to put many blockers in the way of would be tacklers. Lastly, another advantageous impact is the ability to put a player in motion as to help identify defensvie coverage.

All of these are data points we've chosen to analyze as knowledge that an offense has pre-snap, and how that knowledge can influence the separation yardage between a defender and a receiver.


## Does Separation Yardage Even Matter?
Before we even begin assessing the impact of motion on separation yardage, it is worth some investigation what value separation yardage even has. NFL next gen stats 
gives us some insight into how separation yardage is evaluated. One of those insights is the definition of a quarterback throwing in tight coverage, which is defined as 
coverage there is one yard or less worth of separation.

In the boxplots below we see pretty plainly that incompletions are more frequently in tighter windows compared to completions. That said, any advantage around increasing 
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
If given more time the team would do a much deeper dive into the tracking data around motion and it's impact on separation yardage. In particular set of research, it remains as a high level analysis but with tracking data it appears that there is much more to consider

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">I didn&#39;t think it was possible for me to like Joe Brady any more, but I was wrong. Shift/Motion theory can be an incredible weapon if you know how to utilize it. <a href="https://t.co/zqc34t89Gp">https://t.co/zqc34t89Gp</a> <a href="https://t.co/TkrHCFe974">pic.twitter.com/TkrHCFe974</a></p>&mdash; Honest NFL (@TheHonestNFL) <a href="https://twitter.com/TheHonestNFL/status/1869858318606541134?ref_src=twsrc%5Etfw">December 19, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


## Appendix
Code is here blah....
