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
                "coefficients zero) — no vector is redundant."
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
                "Rank is the dimension of the column space — equivalently, the "
                "maximum number of linearly independent rows or columns."
            ),
        },
        {
            "question": "If v is an eigenvector of matrix A with eigenvalue λ, then:",
            "options": [
                "Av = λv", "Av = v/λ", "A + v = λ", "det(A) = λv",
            ],
            "answer_index": 0,
            "explanation": "By definition, Av = λv for eigenvector v and eigenvalue λ.",
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
        {
            "question": "A basis for a vector space is a set of vectors that is:",
            "options": [
                "Linearly dependent and spans the space",
                "Linearly independent and spans the space",
                "Orthogonal but does not need to span the space",
                "Any set with the same number of vectors as the space's dimension, independence not required",
            ],
            "answer_index": 1,
            "explanation": (
                "A basis must be linearly independent AND span the whole "
                "space — every vector in the space is then a unique linear "
                "combination of the basis vectors."
            ),
        },
        {
            "question": "A system of linear equations Ax = b with more equations than unknowns (overdetermined) typically:",
            "options": [
                "Always has a unique exact solution",
                "Has no exact solution in general, so least squares is used instead",
                "Always has infinitely many solutions",
                "Cannot be represented in matrix form",
            ],
            "answer_index": 1,
            "explanation": (
                "An overdetermined system usually has no vector x that "
                "satisfies every equation exactly, which is exactly when "
                "least squares finds the best approximate solution."
            ),
        },
        {
            "question": "Two vectors u and v are orthogonal if:",
            "options": [
                "u · v = 1",
                "u · v = 0",
                "||u|| = ||v||",
                "u = -v",
            ],
            "answer_index": 1,
            "explanation": "Orthogonality means their dot product is zero — geometrically, they meet at a right angle.",
        },
    ],
    2: [
        {
            "question": "Singular Value Decomposition (SVD) factorises a matrix A into:",
            "options": [
                "A = QR", "A = UΣV^T", "A = LU", "A = PDP^-1 only",
            ],
            "answer_index": 1,
            "explanation": "SVD writes A = UΣV^T, where U and V are orthogonal and Σ is diagonal with singular values.",
        },
        {
            "question": "Bayes' theorem relates P(A|B) to:",
            "options": [
                "P(A) and P(B) only, with no other terms",
                "P(B|A), P(A), and P(B)",
                "P(A ∪ B) only",
                "The variance of A and B",
            ],
            "answer_index": 1,
            "explanation": "Bayes' theorem: P(A|B) = P(B|A) P(A) / P(B).",
        },
        {
            "question": "Two events A and B are independent if:",
            "options": [
                "P(A ∩ B) = P(A) + P(B)",
                "P(A ∩ B) = P(A) × P(B)",
                "P(A|B) = P(B)",
                "P(A) = P(B)",
            ],
            "answer_index": 1,
            "explanation": "Independence means P(A ∩ B) = P(A) × P(B), equivalently P(A|B) = P(A).",
        },
        {
            "question": "The 'matrix approach' to linear regression expresses the model as:",
            "options": [
                "y = mx + c only, matrices are not used",
                "y = Xβ + ε, solved via least squares on the design matrix X",
                "A = UΣV^T",
                "P(y|X) = P(X|y)P(y)/P(X)",
            ],
            "answer_index": 1,
            "explanation": (
                "Writing the model as y = Xβ + ε lets you solve for the "
                "coefficients β with a single matrix least-squares "
                "operation, however many predictors there are."
            ),
        },
        {
            "question": "A 'sample space' in probability is:",
            "options": [
                "The set of all possible outcomes of an experiment",
                "The average of all observed samples",
                "A synonym for the population mean",
                "The variance of a random sample",
            ],
            "answer_index": 0,
            "explanation": "The sample space Ω is the complete set of possible outcomes; events are subsets of it.",
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
            "explanation": "E[X] = Σ x·P(X = x) — the probability-weighted average of the outcomes.",
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
        {
            "question": "The variance of a random variable X measures:",
            "options": [
                "The average value of X",
                "How spread out X's values are around its mean",
                "The probability that X equals its mean",
                "The number of possible values X can take",
            ],
            "answer_index": 1,
            "explanation": "Variance is E[(X - E[X])²] — the expected squared distance from the mean, i.e. how spread out the distribution is.",
        },
        {
            "question": "Which distribution is most appropriate for modelling a continuous, symmetric, bell-shaped variable like measurement error?",
            "options": ["Binomial", "Poisson", "Normal", "Bernoulli"],
            "answer_index": 2,
            "explanation": "The Normal (Gaussian) distribution is the standard continuous, symmetric, bell-shaped model, and appears naturally via the Central Limit Theorem.",
        },
        {
            "question": "The Poisson distribution is typically used to model:",
            "options": [
                "The proportion of successes in a fixed number of trials",
                "The number of independent events occurring in a fixed interval of time or space",
                "A continuous measurement with no upper bound",
                "The exact outcome of a single trial",
            ],
            "answer_index": 1,
            "explanation": "Poisson models counts of rare, independent events over a fixed interval — e.g. arrivals per hour — given a known average rate.",
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
        {
            "question": "A correlation coefficient close to 0 between two variables means:",
            "options": [
                "They are strongly causally related",
                "There is little to no *linear* relationship between them",
                "One variable is always double the other",
                "The data must contain errors",
            ],
            "answer_index": 1,
            "explanation": (
                "A correlation near 0 indicates little linear association — "
                "the variables could still have a strong *non-linear* "
                "relationship that correlation doesn't capture."
            ),
        },
        {
            "question": "Which of these is an example of 'data scraping'?",
            "options": [
                "Manually typing survey responses into a spreadsheet",
                "Programmatically extracting data from web pages",
                "Computing the mean of a column",
                "Running a hypothesis test",
            ],
            "answer_index": 1,
            "explanation": "Data scraping is the automated extraction of data from sources like web pages, as part of obtaining raw data for wrangling.",
        },
        {
            "question": "Descriptive statistics (mean, median, standard deviation, etc.) are used to:",
            "options": [
                "Prove causal relationships between variables",
                "Summarise the main features of a dataset",
                "Replace the need for visualisation entirely",
                "Guarantee a model will generalise to new data",
            ],
            "answer_index": 1,
            "explanation": "Descriptive statistics summarise and characterise the data's central tendency, spread, and shape — a first step in EDA.",
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
        {
            "question": "R² (the coefficient of determination) in a regression model represents:",
            "options": [
                "The p-value of the slope coefficient",
                "The proportion of variance in the response explained by the model",
                "The number of predictors in the model",
                "The correlation between the residuals and time",
            ],
            "answer_index": 1,
            "explanation": "R² measures how much of the variance in the response variable is explained by the model, ranging from 0 (no fit) to 1 (perfect fit).",
        },
        {
            "question": "A general linear model that mixes continuous and categorical explanatory variables is typically needed when:",
            "options": [
                "All predictors are continuous",
                "The response variable is always binary",
                "The predictors include a mix of numeric measurements and group/category labels",
                "There is only one predictor variable",
            ],
            "answer_index": 2,
            "explanation": (
                "General linear models extend simple regression to handle "
                "a mix of continuous predictors and categorical factors "
                "(via dummy/indicator coding) in the same model."
            ),
        },
        {
            "question": "In a residual plot for a linear regression, a clear curved (non-random) pattern suggests:",
            "options": [
                "The model fits perfectly",
                "The linear model may be missing a non-linear relationship in the data",
                "The sample size is too large",
                "The response variable must be binary",
            ],
            "answer_index": 1,
            "explanation": (
                "Residuals should look like random scatter around zero if "
                "the linear model is appropriate; a systematic pattern "
                "signals the model is missing structure in the data."
            ),
        },
    ],
}
