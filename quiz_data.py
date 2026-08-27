"""
Practice quiz question bank for the Principles of Data Science module
(MEC7144CEM). Organised by unit ID (see syllabus_data.UNITS).

Each question: {
    "question": str,
    "options": list[str],
    "answer_index": int,       # index into options
    "explanation": str,
}
"""

QUIZ_BANK = {
    1: [
        {
            "question": "A set of vectors is linearly independent if:",
            "options": [
                "Every vector in the set can be written as a linear combination of the others",
                "No vector in the set can be written as a linear combination of the others",
                "The set contains the zero vector",
                "The set spans a plane",
            ],
            "answer_index": 1,
            "explanation": (
                "Linear independence means the only linear combination of the "
                "vectors that equals the zero vector is the trivial one (all "
                "coefficients zero) -- no vector is redundant."
            ),
        },
        {
            "question": "The rank of a matrix is best described as:",
            "options": [
                "The number of rows in the matrix",
                "The determinant of the matrix",
                "The dimension of the column space (number of linearly independent columns)",
                "The sum of the eigenvalues",
            ],
            "answer_index": 2,
            "explanation": (
                "Rank is the dimension of the column space -- equivalently, the "
                "maximum number of linearly independent rows or columns."
            ),
        },
        {
            "question": "If v is an eigenvector of matrix A with eigenvalue lambda, then:",
            "options": [
                "Av = lambda*v", "Av = v/lambda", "A + v = lambda", "det(A) = lambda*v",
            ],
            "answer_index": 0,
            "explanation": "By definition, Av = lambda*v for eigenvector v and eigenvalue lambda.",
        },
        {
            "question": "Least squares is typically used to:",
            "options": [
                "Find the exact solution to an overdetermined system",
                "Find the best-fit approximate solution when a system has no exact solution",
                "Compute eigenvalues directly",
                "Test for independence between events",
            ],
            "answer_index": 1,
            "explanation": (
                "Least squares finds the solution that minimises the sum of "
                "squared residuals, typically for overdetermined systems with "
                "no exact solution."
            ),
        },
    ],
    2: [
        {
            "question": "Singular Value Decomposition (SVD) factorises a matrix A into:",
            "options": [
                "A = QR", "A = U * Sigma * V^T", "A = LU", "A = PDP^-1 only",
            ],
            "answer_index": 1,
            "explanation": "SVD writes A = U*Sigma*V^T, where U and V are orthogonal and Sigma is diagonal with singular values.",
        },
        {
            "question": "Bayes' theorem relates P(A|B) to:",
            "options": [
                "P(A) and P(B) only, with no other terms",
                "P(B|A), P(A), and P(B)",
                "P(A union B) only",
                "The variance of A and B",
            ],
            "answer_index": 1,
            "explanation": "Bayes' theorem: P(A|B) = P(B|A) * P(A) / P(B).",
        },
        {
            "question": "Two events A and B are independent if:",
            "options": [
                "P(A and B) = P(A) + P(B)",
                "P(A and B) = P(A) times P(B)",
                "P(A|B) = P(B)",
                "P(A) = P(B)",
            ],
            "answer_index": 1,
            "explanation": "Independence means P(A and B) = P(A) times P(B), equivalently P(A|B) = P(A).",
        },
    ],
    3: [
        {
            "question": "The expectation E[X] of a discrete random variable X is:",
            "options": [
                "The most frequently occurring value of X",
                "The sum of each value weighted by its probability",
                "The square root of the variance",
                "Always equal to the median",
            ],
            "answer_index": 1,
            "explanation": "E[X] = sum of x times P(X = x) -- the probability-weighted average of the outcomes.",
        },
        {
            "question": "Which distribution models the number of successes in a fixed number of independent Bernoulli trials?",
            "options": ["Normal", "Poisson", "Binomial", "Exponential"],
            "answer_index": 2,
            "explanation": "The Binomial distribution models the count of successes across n independent trials with fixed success probability p.",
        },
        {
            "question": "A key use of Monte Carlo simulation in this module is to:",
            "options": [
                "Prove theorems analytically",
                "Replace the need for probability distributions entirely",
                "Approximate probabilities/expectations by repeated random sampling",
                "Compute exact eigenvalues of a matrix",
            ],
            "answer_index": 2,
            "explanation": "Simulation builds intuition and approximates quantities that are hard to derive analytically, via repeated random sampling.",
        },
    ],
    4: [
        {
            "question": "Putting a relational database table into a higher normal form primarily aims to:",
            "options": [
                "Increase data redundancy for speed",
                "Reduce redundancy and avoid update/insertion/deletion anomalies",
                "Remove all foreign keys",
                "Convert it to unstructured data",
            ],
            "answer_index": 1,
            "explanation": "Normalisation reduces redundancy and anomalies by organising data according to functional dependencies.",
        },
        {
            "question": "Principal Components Analysis (PCA) is mainly used to:",
            "options": [
                "Impute missing categorical data",
                "Reduce dimensionality while preserving as much variance as possible",
                "Scrape data from web pages",
                "Perform hypothesis tests on means",
            ],
            "answer_index": 1,
            "explanation": "PCA finds orthogonal directions (components) that capture the most variance, used for dimensionality reduction.",
        },
        {
            "question": "Which is a step typically associated with 'data wrangling' rather than EDA?",
            "options": [
                "Plotting a correlation heatmap",
                "Computing summary statistics",
                "Cleaning and transforming raw, messy data into a usable structure",
                "Running PCA",
            ],
            "answer_index": 2,
            "explanation": "Data wrangling covers obtaining, cleaning, and transforming data; EDA covers summarising/visualising the cleaned data.",
        },
    ],
    5: [
        {
            "question": "In simple linear regression, the coefficient (slope) represents:",
            "options": [
                "The correlation coefficient r",
                "The predicted change in the response variable per unit change in the predictor",
                "The variance of the residuals",
                "The p-value of the model",
            ],
            "answer_index": 1,
            "explanation": "The slope is the estimated change in the response variable for a one-unit increase in the predictor.",
        },
        {
            "question": "ANOVA is primarily used to:",
            "options": [
                "Compare means across two or more groups",
                "Reduce the dimensionality of a dataset",
                "Test for linear independence of vectors",
                "Cluster unlabeled data",
            ],
            "answer_index": 0,
            "explanation": "Analysis of Variance (ANOVA) tests whether the means of several groups are equal.",
        },
        {
            "question": "Logistic regression is typically used when the response variable is:",
            "options": [
                "Continuous and unbounded",
                "Binary or categorical",
                "A time series",
                "Always normally distributed",
            ],
            "answer_index": 1,
            "explanation": "Logistic regression models the probability of a binary/categorical outcome using the logistic (sigmoid) function.",
        },
        {
            "question": "A small p-value (e.g. < 0.05) in a hypothesis test typically suggests:",
            "options": [
                "Strong evidence in favour of the null hypothesis",
                "Evidence against the null hypothesis",
                "The sample size was too small",
                "The model has no predictive power",
            ],
            "answer_index": 1,
            "explanation": "A small p-value indicates the observed data would be unlikely under the null hypothesis, so it's treated as evidence against it.",
        },
    ],
}
