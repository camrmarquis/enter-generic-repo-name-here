## Yahoo Fantasy API 

Documentation for the Yahoo fantasy api can be found here -> https://developer.yahoo.com/fantasysports/guide/

## Lottery

To keep the league at a high level of competition, I propose the introduction of an NBA style draft lottery.

In the latest version of the NBA lottery, the 14 teams that do not make the playoffs are entered into a drawing to determine their draft order. 
The odds (as of 2020) are such that the bottom 3 teams are given an equal probability of obtaining the number 1 pick, followed by gradually decreasing 
probability for the remaining 11 teams.

The exact odds for the NBA lottery are as follows (note the 1st seed represents team with worst record)

| Seed       | 1   | 2   | 3   | 4    | 5    | 6   | 7    | 8   | 9    | 10  | 11  | 12   | 13   | 14   |
|------------|-----|-----|-----|------|------|-----|------|-----|------|-----|-----|------|------|------|
| P(#1 pick) | .14 | .14 | .14 | .125 | .105 | .09 | .075 | .06 | .045 | .03 | .02 | .013 | .012 | .005 |

A drawing is performed using these odds for the first four picks. After the first four picks are decided, the remaining picks are determined based on the records of the remaining teams. 
This is done so that no team's draft position can be more than 4 spots lower than its seed in the lottery.

This system is what is known as a Plackett-Luce ranking model (see [Discrete Choice](https://en.wikipedia.org/wiki/Discrete_choice)) which follows:

<img src="https://squared2020.files.wordpress.com/2017/09/screen-shot-2017-09-30-at-9-27-55-am.png"/>

<img src="https://squared2020.files.wordpress.com/2017/09/screen-shot-2017-09-30-at-9-33-23-am.png"/>
     
<img src="https://squared2020.files.wordpress.com/2017/09/screen-shot-2017-09-30-at-9-37-06-am.png"/>  

<img src="https://squared2020.files.wordpress.com/2017/09/screen-shot-2017-09-30-at-9-39-49-am.png"/>
  
and so on for determining order

 <img src="https://squared2020.files.wordpress.com/2017/09/screen-shot-2017-09-30-at-9-55-05-am.png"/>

 <img src="https://squared2020.files.wordpress.com/2017/09/screen-shot-2017-09-30-at-9-37-06-am.png"/>
 
 <img src="https://squared2020.files.wordpress.com/2017/09/screen-shot-2017-09-30-at-10-03-22-am.png"/>
  
and so on for determining rank.

Expanding these iterations out to cover all 14 teams creates an odds table that looks as follows:

<img src="https://squared2020.files.wordpress.com/2017/09/screen-shot-2017-09-30-at-10-51-10-am.png?w=1400"/>

#### My Proposal ####

** NOTE ** *"Seed" refers to your position in the lottery. "Rank" refers to your standings in the league at the end of the regular season.*

Enter Generic Name Here should instate a draft lottery system where all 6 non-playoff teams are entered. The actual drawing will decide which teams get the top three picks.
This ensures no team could slide no more than three spots from their end-of-season rank.

The initial draft probabilities based on seed would be as follows:

| Seed       | 1   | 2   | 3   | 4   | 5    | 6    |
|------------|-----|-----|-----|-----|------|------|
| P(#1 pick) | .40 | .33 | .08 | .02 | .013 | .007 |

Now you might note 2 things here:
1. The odds are far better for the top two seeds, despite the fact we are deciding three pick by lottery.
2. These odds only sum to 0.85, not 1.

...to which I say nice job, Sherlock. The remaining 15% chance will be up for grabs in the consolation bracket. (which lottery teams 1 and 2 do not get to participate in).  
How this remaining chance is allocated is dependent on how the lower seed teams fare against the higher seeds in the consolation tournament. (Chris I'd like to know how you see this working exactly... so more to come on this aspect).

#### Example Scenario ####

Say the rule is decided that if the 8th ranked team wins the consolation bracket they are awarded the remaining 15% chance. The final lottery odds would be:

| Seed       | 1   | 2   | 3   | 4   | 5    | 6    |
|------------|-----|-----|-----|-----|------|------|
| P(#1 pick) | .40 | .33 | .23 | .02 | .013 | .007 |

This results in a final odds table of:

|   Seed |   1st Pick |   2nd Pick |   3rd Pick |   4th Pick |    5th Pick |    6th Pick |
|-------:|-----------:|-----------:|-----------:|-----------:|------------:|------------:|
|      1 |      0.4   |  0.332747  |  0.224529  |  0.0427243 | 0           | 0           |
|      2 |      0.33  |  0.331979  |  0.277203  |  0.0598792 | 0.000938954 | 0           |
|      3 |      0.23  |  0.275962  |  0.383994  |  0.106246  | 0.00378736  | 1.13716e-05 |
|      4 |      0.02  |  0.0295625 |  0.0567788 |  0.791151  | 0.101642    | 0.000865302 |
|      5 |      0.013 |  0.0193097 |  0.037266  |  0         | 0.893631    | 0.0367931   |
|      6 |      0.007 |  0.0104404 |  0.0202293 |  0         | 0           | 0.96233     |

This is calculated in `lottery/build_odds_table.py`. So the 6th seed in the lottery has a 0.7% chance at the first pick, a 1.04% chance at the 2nd pick, a 2% chance at the 3rd pick and so on.
