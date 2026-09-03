
# Recap 
*(7/30/26 - 9/3/26)*

*See the repo [here](https://github.com/drecrash/complexity-lp-cogsci)*

# Prologue

During my 8-week long [summer research](https://lnkd.in/p/gznghJCM) program at Ohio State, my work with the Cognitive Systems Engineering Lab introduced me to the field of cognitive science. Although my initial research interest was in the study of complex systems using computer science, I've realized that computational cognitive science may be even more interesting.

Since I had over two months between the end of my program and the start of my first semester at UCSB, I thought I would take the opportunity to familiarize myself with some of the topics I either have had in the back of my mind for months, or became curious about during my time at OSU.

I was partially inspired by Scott Young's articles on [Ultralearning](https://www.scotthyoung.com/blog/2016/07/28/ultralearn-diy-1/), and although what I pursued during these eight weeks was not at quite that caliber, I do believe I gained beneficial knowledge and skills from the experience.

This post is a recap of what I learned, how I learned it, and a reflection on the project as a whole.

# Section 1: The Subjects

## Section 1.1: Linear Programming

**Overview**

Before the summer started, I learned about linear programming from [this video](https://youtu.be/A81Hp_qpQgs?si=i44j5oh2Y9Lp_xBj) that came across my feed, and I was immediately interested. The math behind optimization is fascinating and I think the applications of LP in disciplines such as game theory and economics make it a very useful tool to at least be familiar with.

I did not get entirely through [the textbook](https://dl.icdst.org/pdfs/files3/faa54c1f53965a11b03f9a13b023f9b2.pdf) I was following, stopping around the chapters on game theory and network applications, but regardless, I built a solid foundation to be built upon if I ever need this skill in the future.

I learned the basic structure of linear programs (such as designing an objective, determining decision variables, etc.), duality theory and shadow prices, sensitivity analysis, matrix definitions, LP in game theory, and LP as networks.

**Projects**

Two of my weekly projects were centered around linear programming. The reason it's comparatively low is because the problems from the textbook are often not actual programming projects. Rather, they were standard assigment questions, like applying the simplex method or calculating duals.

*Resource Allocation*

The first project was a [resource allocation](https://github.com/drecrash/complexity-lp-cogsci/tree/main/weekly-projects/04-resource-allocation) problem. Essentially, a student has three 3-hour blocks of study time per day, and has to maximize their total "performance" by determining how much time to allocate to what subjects. Certain subjects have pre-requisites that must be fulfilled before any time can be spent on them. Each subject has a minimum and maximum time. Energy/productivity varies throughout the day (afternoon is weighted higher than the evening, for instance)

This project was my first experience properly setting up a linear programming problem based on a textual description. The exact details are in the `DISCUSSION.md` for that project, but the key takeaways from that project were:
- How to set up "if/then" statements in LP problems using binary decision variables (necessary for prerequisites)
- How to properly interpret shadow prices

Shadow prices are how much performance can be increased if a certain constraint is relaxed, and I found that adding just one additional hour of study time in the afternoon could boost performance by 28 units.

*Game Theory Solver*

The second project was a [zero-sum game solver](https://github.com/drecrash/complexity-lp-cogsci/tree/main/weekly-projects/06-gametheory-solver).

Games can be represented as matrices, where each player is either the row or column.

For instance, take Rock/Paper/Scissors. If we let $A$ be the matrix for the game, have rows $i$ and columns $j$ represent the choices that each player can make (e.g., row 1 means the row player chooses rock, column 3 means the column player chooses scissors), then $a_{ij}$ can represent how much the row player (Player A) pays the column player (Player B). So the matrix for RPS is:
$$ A = \begin{bmatrix} 0 & 1 & -1 \\ -1 & 0 & 1 \\ 1 & -1 & 0 \end{bmatrix} $$
(negatives mean that Player B pays Player A $|a_{ij}|$)

This can be formulated as a linear programming problem since Player A is trying to *minimize* their expected payoff, and Player B is trying to *maximize* their expected payoff. They are solving the *duals* of one another's problems. The exact details are in that project's `DISCUSSION.md`.

The solver can determine the optimal strategies for each player, which is just a probability distribution of making different choices. For instance, in rock paper scissors, the most optimal strategy is just to pick randomly. However, in the prisoner's dilemma, the most optimal strategy is for both players to confess.

However, this does *not* work for non-zero sum games. But we'll tackle that problem soon

## Section 1.2: Complexity

**Overview**

I was introduced to complexity science in November of 2025 and it's a world that I've been slowly peeking into over the past year.

Over the summer, I discovered [this textbook](https://global.oup.com/academic/product/introduction-to-the-theory-of-complex-systems-9780198821939), and thought it would, at the very least, be an interesting read. 

Getting into it, though, I found it to cover some extremely interesting subjects, namely probability and network theory. I previously thought statistics and probability to be abhorrent, but this textbook introduced topics such as the central limit theorem (CLT), the laws of large and small numbers, stochastic processes, Markov processes, and more, in a way that was very engaging.

**Projects**

Complexity is fundamentally a science driven by simulation and algorithmic work, so it was simple to apply its topics to programming projects. Most notably in the network science and evolution chapters.

- In my [random walk](https://github.com/drecrash/complexity-lp-cogsci/tree/main/weekly-projects/01-randomwalk) project, I directly observed the effects of running a random walk based on random variables from a uniform vs Cauchy distribution. Cauchy distributions lack finite variance, so the CLT does not apply to them. I was also able to empirically observe what the textbook meant by "fat tailed distributions fall off *more slowly*"
- In my [power law](https://github.com/drecrash/complexity-lp-cogsci/tree/main/weekly-projects/02-powerlaws) project, I applied the method of "maximum likelihood" to try and determine the power law used in deriving a set of values from a general pareto distribution. This was one of the more "math-intensive" projects, as it involved finding the power value that is most probable. Which is equivalent to solving this probability for $a$: $p(a|\vec{x}) =\prod_{i=1}^N \frac{a-1}{x_m}(\frac{x_i}{x_m})^{-a}$. All the math is discussed in that project's `DISCUSSION.md`
- In my [Erdos-Reyni](https://github.com/drecrash/complexity-lp-cogsci/tree/main/weekly-projects/03-erdosreyni) project, I generated an ER graph and manually calculated the clustering coefficient using the formula from the textbook to compare against NetworkX's own clustering coefficient function. I also plotted the dynamics of how the size of the largest component size changes over time, noting the thresholds for giant component emergence and complete graph connection.
- In my [epidemic model](https://github.com/drecrash/complexity-lp-cogsci/tree/main/weekly-projects/05-sir) project, I implemented the famous Susceptible-Infected-Recovered model of epidemic spread on networks on the ER network from the previous project, and a newly implemented Barabasi-Albert network. In this project, I also implemented a basic reproductive number calculator (the average number of number that will get infected from one infectious agent) and a critical infectious fraction calculator (total final fraction of infected nodes). 
- In my [replicator equation](https://github.com/drecrash/complexity-lp-cogsci/tree/main/weekly-projects/07-replicator-equation) project, I solved the non-zero sum [Hawk-Dove game](https://darwin.uky.edu/~sargent/Bio608/Hawks&Doves.htm) using the replicator equation from evolution theory. This required defining the problem as a matrix, determining the expected payoff/fitness for hawks/doves based on current population percentages and outcomes, and dynamically simulating how the population levels shifted over time. The nature of this scenario is that the species will eventually reach a *Nash equilibrium* where the percentage of Hawks and percentage of Doves stay the same.


- Chapter 3 (scaling) also had some problems directly from the textbook that I worked through [here](https://github.com/drecrash/complexity-lp-cogsci/tree/main/complexity-problems)

## Section 1.3: Cognitive Science

For cognitive science, I wanted to get a general overview of the field, so I treated this as more of a "survey course".

I found and read many different papers, and I've listed a few of the most notable ones below:

- [The free-energy principle: a unified brain theory?](https://www.nature.com/articles/nrn2787) by Karl Friston
    - My first introduction to the ideas of free energy and the Bayesian Brain Hypothesis. I found myself attached to the idea of cognition and perception as a probability distribution based on Bayesian reasoning. This paper was a great addition to the Complexity chapter on Probability, and got me excited thinking about the future of computational models of cognition
- [Joint representation of working memory and uncertainty in human cortex](https://pubmed.ncbi.nlm.nih.gov/34525327/) by Li et al.
    - This paper's key finding was that actual brain activity from fMRI data reveals that the brain stores information as a probability distribution. I initially read it soon after learning about the Bayesian Brain Hypothesis (BBH), so it was fascinating to learn how the theory was being empirically observed in real subjects. Moreover, the paper found that the *width* of the probability distribution can adequately describe the subject's overall uncertainty, which correlates well with the BBH.
- [Neural Decoding of Collective Wisdom with Multi-Brain Computing](https://pubmed.ncbi.nlm.nih.gov/21782959/) by Eckstein et al.
    - My main takeway from this paper was how collective intelligence emerges when groups of cognitive agents make decisions together. Essentially, each agent observes different factors of the environment, and weights each of these factors differently. So the total perception of an agent can be represented as $w_if_i + w_jf_j + ...$. So collective intelligence emerges from a linear combination of these perceptions, creating an overall understanding that consideres far more environmental factors than just one agent could alone
- [Emergent human-like covert attention in feedforward convolutional neural networks](https://pubmed.ncbi.nlm.nih.gov/38244541/)
    - This paper discussed many things, but my main takeaway was that *attention is an emergent property of optimizing performance*. Attention is generally considered a finite resource or undesirable consequence of human cognitive limitations, but this paper finds that, if you give a feedback-less neural network a cognitive task with no such limitations and no instructions other than to optimize performance, it evolves a system very comparable to human attention.

# Section 2: Tools and Assistance
## Section 2.1: AI

Despite the poor stigma associated with AI, I found it immensely beneficial during this project. I personally believe it would have been a key element of Scott Young's Ultralearning method, had it been as powerful as it is now back in 2016.

I worked with Claude before the summer research concluded, describing my background and goals, and, after some revisions, we designed a solid "curriculum" based on the textbooks I had selected. Many of the programming project concepts were actually born out of suggestions from Claude.

Although I understand it might have been more "impressive" to do this entirely on my own, AI removed the fluff from the self-teaching process and enabled me to focus on actually learning the material. I didn't have to waste time designing a curriculum or deciding what to do and when; rather, just like a normal semester, I simply had reading and assignments to complete.

Any and all code, writing, and reflections in my project repository was developed by me (human, if you couldn't tell). Well, except some of the data in my resource allocation project, I didn't exactly feel like thinking up 20 different subjects and how important they each are.

I think AI is going to be/already is an extremely powerful tool for augmenting learning. Obviously, it can be used irresponsibly and unproductively, but I think anyone with an actual desire to learn the material they are studying will find it more useful than practically any other resource.

## Section 2.2: Notetaking

Throughout this whole project, I took my notes in Markdown, in Obsidian. 

Why did I do this? Because I had Obsidian installed already and didn't feel like getting a different app. They also have a very convenient "templates" feature that I used for writing my notes from textbooks and research papers.

But... working in Markdown also gave me the opportunity to learn how to write in LaTeX: a skill I found very annoying to not have during my time at OSU. I honestly thought it would be more difficult to learn, but after some practice, writing $\sum_{a,b}\frac{(O-E)^2}{E}$ or $\sum_jq_{ij}(x_i\sum_kp_{jk}x_k)-x_i\phi$ becomes $\text{second nature}$.


## Section 2.3: Anki

During the summer, I read [this article](https://augmentingcognition.com/ltm.html) by quantum physicist Michael Nielsen on how he uses Anki in his work, learning, and even daily life. I found it super interesting, and decided to give it a trial run over this 8-week period. 

And man, I don't think I'll ever go back.

The process of not only reviewing cards, but actually having to write the cards, forces you to nitpick what the most important elements of a chapter or paper are (since you don't want to do more cards just for the sake of more cards). Spaced repetition is so powerful for beating the forgetting curve, and Nielsen's tip of putting every subject (like cognitive science, linear programming, and complexity) all in the same deck was a hidden gem. Because everything is together, I might be answering a question about the Bayesian Brain one second and then duality theory the next; and sometimes, this can lead to interdisciplinary connections I might not otherwise considered.

# Section 3: Discussion
## Section 3.1: How do I feel

It was definitely a journey. A lot of times I was questioning if it was worth continuing with it, since I wasn't getting feedback or assessments like I would with a standard education, but each time, the topics were interesting enough to push through the feeling (and also the sunk cost fallacy began to set in). 

If I were to do this again, I'd probably choose one more "humanities"-style course to go along with everything. Working on my blog and writing essays kept me sane from all the numbers, and I think that energy might have been more productively channelled into a dedicated course on an interesting subject, like philosophy or history.

With that said, I do think that doing multiple courses is the right move. Being able to oscillate between LP, Complexity, and Cognitive Science let me get a breath of fresh air every morning instead of just burning myself out hammering the same concepts over and over and over again.

## Section 3.2: Moving forward

I'm starting my first semester at UCSB in about two weeks as a transfer student. I'm incredibly excited, and I hope I'll be able to translate some of the skills I gained this summer, not only from this project but from my research experience as well, to my classes and maybe even a research position on campus.

I'll definitely take on another self-learning project again in the future. I'm not sure when, and I'm not sure what it will be, but it will happen. If anything in this resonated with you, I highly encourage you do something similar when you have the time. It's unbelievably fun once you get into it, and worst comes to worst, even if you don't make anything useful or spend the time "productively": you learned something you're interested in.