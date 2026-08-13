# Random Project in Week 3 - The Diet Problem with a Twist


## Background
As I wrap up the introductory segments to Linear Programming, and have studied the theory behind the Simplex Method, the fundamental theorem of LP, duals, etc., I'm becoming more eager to actually start applying the principles of LP in code. Math and theory are fun, but code is funner.

So I decided to do the classic "diet problem", where you use a food database and a set of nutrition requirements to determine the cheapest possible diet given nutritional constraints. However, many food databases with adequate vitamin and micronutrient information don't have standardized costs.
Since I didn't want to manually enter costs, I solved a *twist* on the diet problem: maximize protein while staying at a caloric requirement. This gave me the opportunity to experiment with PuLP without having to manually enter costs.

## Dataset

Nutritional requirements are from the FDA: https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels

Food nutritional data taken from this Kaggle dataset: https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset?resource=download



## Results

One of the unexpected results of this project was that I have learned that it is impossible (or infeasible) to meet all basic nutrient requirements for 1380 kilocalories or less.

With the bare minimum number of Calories, it is possible to reach roughly 67.7g of protein through:
```
433.97 grams of soybean lecithin oil
2.9 grams of chicken spread
38.89 grams of dried jellyfish
735.11 grams of wheat bran
and 0.0023g of acerola cherry juice
```

For a standard diet of 2000 calories, however, it is possible to get 279.82 grams of protein through
```
687.1 grams of soy proteins isolate
534.08 grams of chicken spread
986.71 grams of cooked oat bran cooked
1.67 grams of wheat bran
0.0023 grams of acerola cherry juice
```

## Discussion

I find it interesting that both solutions involve trace amounts of acerola cherry juice. I presume it has some vitamin or mineral that no other food has while also minimizing Calories or maximizing protein.
I also find it interesting that both solutions include wheat bran, but the 2000kcal diet has a fraction of the 1381kcal diet.

This was a very fun project to work it. It helped brush off my CSV processing skills and introduced me to PuLP. I'm excited to see what else I can do with the software.