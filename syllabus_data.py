"""
Structured content for the "Principles of Data Science" module
(MEC7144CEM, MSc Data Science, Middle East College).

This is the single source of truth the rest of the app (syllabus browser
and quizzes) is built from, so content stays specific to this module
rather than generic data-science trivia.
"""

MODULE_INFO = {
    "code": "MEC7144CEM",
    "title": "Principles of Data Science",
    "programme": "MSc Data Science",
    "college": "Middle East College",
    "level": "OQF Level 9 (Master's)",
    "credit_hours": "300 / 30",
    "contact_hours": 60,
    "type": "Core",
    "objectives": (
        "While data science tools and technologies are evolving rapidly, this module "
        "aims to build foundational knowledge and understanding of the mathematical "
        "concepts, statistical models, and data analytics skills at the heart of data "
        "science. Students study and apply the mathematics of linear algebra and "
        "probability, apply statistical models and exploratory data analysis to "
        "summarise, compare, visualise and test data, and use software tools and "
        "high-level libraries to investigate real multivariate datasets."
    ),
    "learning_outcomes": [
        "Demonstrate systematic knowledge and critical understanding in topics in "
        "linear algebra, probability and statistical models, relevant to data science.",
        "Investigate, develop, combine and critically assess approaches and solutions "
        "to challenges in data analysis, statistical modelling, and communication of "
        "results, both individually and as part of a team.",
        "Evaluate and apply mathematical, statistical and data science methods, "
        "models, analytical skills and software tools to transform data, assess and "
        "compare models, solve problems and investigate fundamental properties and "
        "concepts in data science.",
    ],
    "assessments": [
        {
            "name": "Individual Assignment",
            "weight": "30%",
            "duration": "6 weeks",
            "maps_to_lo": "LO1",
            "description": (
                "Applying linear algebra and probability, e.g. properties of "
                "orthogonal matrices and the multivariate normal distribution."
            ),
        },
        {
            "name": "Portfolio",
            "weight": "40%",
            "duration": "7 weeks",
            "maps_to_lo": "LO2",
            "description": (
                "Part group, part individual -- mini-projects in data analysis, "
                "statistical modelling, and communication of results."
            ),
        },
        {
            "name": "Practical Test",
            "weight": "30%",
            "duration": "2 hours",
            "maps_to_lo": "LO3",
            "description": (
                "Individual, time-constrained test involving problem-solving and "
                "data analysis using software."
            ),
        },
    ],
    "pass_rule": (
        "Assignment must be at least 40%, Portfolio at least 40%, Test at least 40%, "
        "and the overall Module Mark must be at least 40% to pass."
    ),
    "references": {
        "basic": [
            "Everitt, B. and Hothorn, T. -- An Introduction to Applied Multivariate "
            "Analysis with R, Springer, 2011.",
            "Lay, D.C., Lay, S.R. and McDonald, J.J. -- Linear Algebra and its "
            "Applications (5th edition), Pearson, 2014.",
        ],
        "recommended": [
            "Spiegelhalter, D. -- The Art of Statistics: Learning from Data, Pelican "
            "Books, 2019.",
            "Wickham, H. and Grolemund, G. -- R for Data Science: Import, Tidy, "
            "Transform, Visualize, and Model Data, O'Reilly, 2016.",
        ],
    },
}

UNITS = [
    {
        "id": 1,
        "title": "Linear Algebra Foundations",
        "topics": [
            "Systems of linear equations, vectors, vector spaces, linear "
            "independence, and basis.",
            "Matrices, determinants, linear transformations, the four "
            "fundamental subspaces, and rank.",
            "Eigenvalues and eigenvectors, orthogonality, least squares, and "
            "numerical methods.",
        ],
        "key_terms": [
            "vector space", "linear independence", "basis", "determinant",
            "rank", "eigenvalue", "eigenvector", "orthogonality",
            "least squares",
        ],
    },
    {
        "id": 2,
        "title": "Applied Linear Algebra & Probability Review",
        "topics": [
            "Practical applications using NumPy: visualising data in "
            "multi-dimensional arrays, the matrix approach to linear "
            "regression, and matrix decompositions such as SVD.",
            "Review of probability: sample spaces, conditional probability, "
            "independence, probability trees, and Bayes' theorem.",
        ],
        "key_terms": [
            "NumPy array", "singular value decomposition", "conditional "
            "probability", "independence", "Bayes' theorem", "sample space",
        ],
    },
    {
        "id": 3,
        "title": "Probability Distributions & Simulation",
        "topics": [
            "Common discrete and continuous probability distributions, "
            "random variables, expectation, and variance.",
            "Fitting models to empirical data.",
            "Using simulation to illustrate probability concepts and build "
            "intuition.",
        ],
        "key_terms": [
            "random variable", "expectation", "variance", "binomial "
            "distribution", "normal distribution", "Poisson distribution",
            "Monte Carlo simulation",
        ],
    },
    {
        "id": 4,
        "title": "Data Wrangling & Exploratory Data Analysis",
        "topics": [
            "Data wrangling: obtaining, importing, cleaning, transforming "
            "and storing data, including scraping, structured data, "
            "relational databases, and normal forms.",
            "Exploratory data analysis: data visualisation, descriptive "
            "statistics, correlation, and multivariate techniques such as "
            "principal components analysis (PCA).",
        ],
        "key_terms": [
            "data cleaning", "normal forms", "relational database",
            "descriptive statistics", "correlation", "principal components "
            "analysis",
        ],
    },
    {
        "id": 5,
        "title": "Statistical Modelling",
        "topics": [
            "Simple linear regression, analysis of variance (ANOVA), and "
            "general linear models with continuous and categorical "
            "explanatory variables.",
            "Logistic regression and hypothesis testing.",
            "Libraries and tools for data analysis and statistical "
            "modelling, e.g. Python and R.",
        ],
        "key_terms": [
            "linear regression", "ANOVA", "general linear model",
            "logistic regression", "hypothesis testing", "p-value",
        ],
    },
]
