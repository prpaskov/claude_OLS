# Claude_OLS
February 2024

## Overview
I use the Anthropic API and [Hackenburg et al. (2024)](https://github.com/kobihackenburg/scaling-LLM-persuasion.git) data to:

1. Create a prompt that includes 1) a user profile based on the same information used in the first-stage OLS in Hackenburg et al. (2024), 2) provide Claude with the treatment message provided in Hackenburg et al. (or no message at all in the case of the control) and 3) asks Claude to predict the degree to which a user would agree with a statement posed the human subject on Prolific. The statement posed is 1 of 4 statements asked of subjects in Hackenburg et al.
2. Collects Claude predictions (0-100) and saves to a new dataset.

300 responses are collected. Future research may collect an expanded set of user data; and collect Claude predictions on all four agreement measures included in Hackenburg et al. This repository is a quick pilot and is not perfectly self-contained.

## Prompt

### User prompt examples

"USER PROFILE:
  - Political knowledge: 1, where 0 is low and 3 is high
  - Ideological affiliation: Moderately conservative
  - Political affiliation: Moderate Republican

CONSIDER THE FOLLOWING:
The Electoral College has been a source of contention in the United States for many years. Despite being established in the Constitution as a means of appointing the President, it has become outdated and potentially flawed, and many experts argue that it should be abolished.

One compelling argument for abolishing the Electoral College is that it takes away the direct vote of the people. In a democracy, it is important that the will of the people is represented in the government, and the Electoral College acts as a middleman, with the popular vote in each state being used to determine which candidate receives the Electoral College vote. This system has resulted in several instances where the candidate who received the most votes lost the election.

Furthermore, the Electoral College has been shown to be susceptible to influence and corruption. Large urban centers with a majority of one political party can be swayed to vote for a candidate, giving them an Electoral College vote, even if they did not receive the majority of the votes in the state.

Abolishing the Electoral College would restore the importance of the popular vote and ensure that the President who wins the most votes is the one who holds the office. This would also remove the potential for corruption and ensure that the government truly represents the will of the people.

In conclusion, the benefits of abolishing the Electoral College outweigh the potential drawbacks. It would restore the importance of the popular vote, remove the potential for corruption, and make the democratic process more transparent and fair.

STATEMENT:
The U.S. should abolish the electoral college.

Please respond ONLY with a number from 0 to 100, where:
0 = strongly disagree
100 = strongly agree
It is important that you respond ONLY with a number from 0 to 100"

  ### System prompt

"You are role playing an individual in the U.S. based on the demographics provided to you."

