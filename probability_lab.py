"""
Hands-on, interactive practice for Unit 2 & 3 probability concepts:
Bayes' theorem, discrete/continuous probability distributions, and
simulation (Law of Large Numbers).

Everything here runs locally with NumPy -- no external calls, no cost.
"""

import numpy as np
import pandas as pd
import streamlit as st


def render_bayes_lab() -> None:
    st.subheader("Bayes' Theorem Calculator")
    st.caption(
        "Classic example: a medical test for a rare condition. Adjust the "
        "sliders and see how the probabilities combine via Bayes' theorem."
    )

    prior = st.slider(
        "P(A) -- prior probability someone has the condition", 0.0001, 1.0, 0.01, step=0.0001,
        format="%.4f",
    )
    sensitivity = st.slider(
        "P(B|A) -- probability the test is positive, given they have it (sensitivity)",
        0.0, 1.0, 0.99, step=0.001,
    )
    false_positive_rate = st.slider(
        "P(B|not A) -- probability the test is positive, given they DON'T have it (false positive rate)",
        0.0, 1.0, 0.05, step=0.001,
    )

    p_not_a = 1 - prior
    p_b = sensitivity * prior + false_positive_rate * p_not_a
    p_a_given_b = (sensitivity * prior / p_b) if p_b > 0 else 0.0

    st.markdown("**Bayes' theorem:** P(A|B) = P(B|A) x P(A) / P(B)")
    col1, col2, col3 = st.columns(3)
    col1.metric("P(B) -- overall chance of a positive test", f"{p_b:.4f}")
    col2.metric("P(A|B) -- chance they have it, given positive", f"{p_a_given_b:.2%}")
    col3.metric("P(A) -- prior (before testing)", f"{prior:.2%}")

    st.caption(
        "Notice: even with a 99% sensitive test, if the condition is rare "
        "(low prior), a positive result can still mean the true probability "
        "of having it is much lower than most people expect -- this is why "
        "the prior matters so much."
    )


def _binomial_pmf(n: int, p: float) -> tuple[np.ndarray, np.ndarray]:
    k = np.arange(0, n + 1)
    from math import comb

    pmf = np.array([comb(n, int(ki)) * (p ** ki) * ((1 - p) ** (n - ki)) for ki in k])
    return k, pmf


def _poisson_pmf(lam: float, k_max: int) -> tuple[np.ndarray, np.ndarray]:
    k = np.arange(0, k_max + 1)
    from math import exp, factorial

    pmf = np.array([(lam ** ki) * exp(-lam) / factorial(int(ki)) for ki in k])
    return k, pmf


def _normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    return (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def render_distribution_lab() -> None:
    st.subheader("Distribution Explorer")
    st.caption("Pick a distribution and its parameters to see its shape, mean, and variance.")

    dist = st.selectbox("Distribution", ["Binomial", "Poisson", "Normal"])

    if dist == "Binomial":
        n = st.slider("n (number of trials)", 1, 100, 20)
        p = st.slider("p (success probability)", 0.0, 1.0, 0.5, step=0.01)
        k, pmf = _binomial_pmf(n, p)
        mean, var = n * p, n * p * (1 - p)
        st.bar_chart(pd.DataFrame({"P(X = k)": pmf}, index=k))

    elif dist == "Poisson":
        lam = st.slider("lambda (average rate)", 0.1, 30.0, 4.0, step=0.1)
        k_max = int(min(60, lam * 4 + 10))
        k, pmf = _poisson_pmf(lam, k_max)
        mean, var = lam, lam
        st.bar_chart(pd.DataFrame({"P(X = k)": pmf}, index=k))

    else:  # Normal
        mu = st.slider("mean (mu)", -10.0, 10.0, 0.0, step=0.1)
        sigma = st.slider("std dev (sigma)", 0.1, 5.0, 1.0, step=0.1)
        x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 200)
        pdf = _normal_pdf(x, mu, sigma)
        mean, var = mu, sigma ** 2
        st.line_chart(pd.DataFrame({"density": pdf}, index=np.round(x, 3)))

    col1, col2 = st.columns(2)
    col1.metric("Mean E[X]", f"{mean:.4f}")
    col2.metric("Variance", f"{var:.4f}")


def render_simulation_lab() -> None:
    st.subheader("Law of Large Numbers -- Coin Flip Simulator")
    st.caption(
        "Flip a (possibly biased) coin many times and watch the running "
        "proportion of heads converge toward the true probability p."
    )

    p_true = st.slider("True probability of heads (p)", 0.0, 1.0, 0.5, step=0.01)
    n_flips = st.slider("Number of flips", 10, 5000, 500, step=10)
    seed = st.number_input("Random seed (change to reshuffle)", min_value=0, max_value=9999, value=42, step=1)

    rng = np.random.default_rng(int(seed))
    flips = rng.random(n_flips) < p_true
    running_mean = np.cumsum(flips) / np.arange(1, n_flips + 1)

    st.line_chart(
        pd.DataFrame({"running proportion of heads": running_mean, "true p": p_true})
    )
    final = running_mean[-1]
    st.metric(f"Proportion of heads after {n_flips} flips", f"{final:.4f}")
    st.caption(
        f"As the number of flips grows, the running proportion converges to "
        f"the true probability p = {p_true:.2f} -- this is the Law of Large "
        "Numbers, the same principle behind using simulation to approximate "
        "probabilities that are hard to compute analytically."
    )
