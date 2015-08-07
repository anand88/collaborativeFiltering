# Summary

Implement a recommender system that uses stastical collaborative filtering, and evaluate it's performance using the Absolute Mean Error and the Root Mean Square Error metrics.

A pool of 5 processes predicts the rating for each combination of movie and user. As you know, multiprocessing is awesome.

#Executing the Program

Type the following line:

"python CollabFinal.py <name of file with training data> <name of file with test data>"

The script uses Python 3 syntax, and the data is in the format that is used in the Netflix Prize data.

#Performance:

Using 32,55,353 lines of data for training and 383 lines of data randomly extracted for testing the results obtained were:  

Absolute Mean Error: 0.751579120964987
Root Mean Square Error: 0.9859209041709854


