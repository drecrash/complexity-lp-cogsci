# Week 6 Project - Game Theory Solver

## Reading
- LP Chapter 11: Game Theory

## Background

One useful application of linear programming is in solving games that can be defined in *payoff matrices*. These payoff matrices 
denote the loss/gain of one party (the row or column player). For instance, the payoff matrix for the Row Player (Player A) is $A$ such that $a_{ij}$ is the amount that A pays player B (the Column Player) if A chooses $i$ and B chooses $j$. If $a_ij < 0$, then that means Player A has *gained* something.

For *symmetric games*, the payoff matrix for player B is just $A^T$. But for *asymmetric games*, the payoff matrix for player B is unique.

For symmetric games, it's easy to see that Player B wants to minimize the payoff for Player A. And Player A wants to maximize the payoff for themselves.

Since one player is maximizing and the other is minimizing, and they both are working with the same payoff matrix, the problem for the column player becomes

$$\begin{align}

	maximize \begin{bmatrix} 0 \\ 1\end{bmatrix}\begin{bmatrix} x \\ v\end{bmatrix} \\
	subject \space to \begin{bmatrix} -A & e \\ e^T & 0\end{bmatrix} \begin{bmatrix} x \\ v\end{bmatrix} = \begin{bmatrix} \le \\ =\end{bmatrix}\begin{bmatrix} 0 \\ 1\end{bmatrix}

	\end{align}
$$

And the problem for the row player becomes

$$\begin{align}

	minimize \begin{bmatrix} 0 \\ 1\end{bmatrix}\begin{bmatrix} x \\ u\end{bmatrix} \\
	subject \space to \begin{bmatrix} -A^T & e \\ e^T & 0\end{bmatrix} \begin{bmatrix} x \\ u\end{bmatrix} = \begin{bmatrix} \ge \\ =\end{bmatrix}\begin{bmatrix} 0 \\ 1\end{bmatrix}

	\end{align}
$$
## The Project

This project is to implement a simple game solver. It applies PuLP and the above equations to achieve this.

It's important to note that this solver will only work with *zero-sum games*.

It is able to properly solve the rock paper scissors problem (each player chooses completely randomly), and the Prisoner's Dilemma (each player confesses).

It will output the optimal probabilities for each option as well as the *value of the game* (the minimum that the row player can achieve and the maximum that the column player can achieve)

