"""
Hands-on, interactive practice for Unit 5: statistical modelling --
simple linear regression (with R^2 and residuals), logistic regression,
hypothesis testing (two-sample t-test), and ANOVA.

Everything here runs locally with NumPy/Pandas/SciPy -- no external
calls, no cost.
"""

import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats


def render_linear_regression_lab() -> None:
    st.subheader("Simple Linear Regression")
    st.caption(
        "Edit the data points, fit y = mx + c, and see R^2 plus a residual "
        "plot -- a curved/patterned residual plot is a warning sign the "
        "linear model may be missing structure (see the Practice Quiz)."
    )
    default = pd.DataFrame(
        {
            "x (study hours)": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
            "y (exam score)": [42.0, 48.0, 55.0, 58.0, 68.0, 71.0, 80.0, 84.0],
        }
    )
    edited = st.data_editor(default, key="linreg_editor", num_rows="dynamic")
    x = edited.iloc[:, 0].to_numpy(dtype=float)
    y = edited.iloc[:, 1].to_numpy(dtype=float)

    if len(x) < 3:
        st.info("Add at least 3 points to fit a meaningful regression.")
        return

    A = np.vstack([x, np.ones_like(x)]).T
    (m, c), *_ = np.linalg.lstsq(A, y, rcond=None)
    y_pred = m * x + c
    residuals = y - y_pred

    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    col1, col2, col3 = st.columns(3)
    col1.metric("Slope (m)", f"{m:.4f}")
    col2.metric("Intercept (c)", f"{c:.4f}")
    col3.metric("R-squared", f"{r_squared:.4f}")

    fit_df = pd.DataFrame({"x": x, "actual y": y, "fitted y": y_pred}).set_index("x")
    st.markdown("**Fit**")
    st.line_chart(fit_df)

    st.markdown("**Residuals (actual - fitted)**")
    resid_df = pd.DataFrame({"x": x, "residual": residuals})
    st.scatter_chart(resid_df, x="x", y="residual")
    st.caption(
        "Residuals scattered randomly around 0 with no pattern is what you "
        "want; a curve or funnel shape suggests the linear model doesn't "
        "fully capture the relationship."
    )


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def _fit_logistic(x: np.ndarray, y: np.ndarray, lr: float = 0.1, iters: int = 2000):
    x_std = (x - x.mean()) / (x.std() + 1e-12)
    w, b = 0.0, 0.0
    n = len(x)
    for _ in range(iters):
        z = w * x_std + b
        p = _sigmoid(z)
        grad_w = np.mean((p - y) * x_std)
        grad_b = np.mean(p - y)
        w -= lr * grad_w
        b -= lr * grad_b
    return w, b, x.mean(), x.std() + 1e-12


def render_logistic_regression_lab() -> None:
    st.subheader("Logistic Regression")
    st.caption(
        "Edit the data (x = study hours, y = 1 for pass / 0 for fail), fit "
        "a logistic curve, and see predicted probabilities plus a confusion "
        "matrix at a chosen threshold."
    )
    default = pd.DataFrame(
        {
            "x (study hours)": [1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9],
            "y (1=pass, 0=fail)": [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
        }
    )
    edited = st.data_editor(default, key="logreg_editor", num_rows="dynamic")
    x = edited.iloc[:, 0].to_numpy(dtype=float)
    y = edited.iloc[:, 1].to_numpy(dtype=float)

    if len(x) < 4 or len(np.unique(y)) < 2:
        st.info("Add at least a few points with both 0 and 1 outcomes present.")
        return

    w, b, x_mean, x_std = _fit_logistic(x, y)

    x_grid = np.linspace(x.min(), x.max(), 100)
    x_grid_std = (x_grid - x_mean) / x_std
    p_grid = _sigmoid(w * x_grid_std + b)

    curve_df = pd.DataFrame({"x": x_grid, "P(pass)": p_grid}).set_index("x")
    st.line_chart(curve_df)

    threshold = st.slider("Decision threshold", 0.0, 1.0, 0.5, step=0.05)
    x_std_pts = (x - x_mean) / x_std
    p_pts = _sigmoid(w * x_std_pts + b)
    pred = (p_pts >= threshold).astype(int)

    tp = int(np.sum((pred == 1) & (y == 1)))
    tn = int(np.sum((pred == 0) & (y == 0)))
    fp = int(np.sum((pred == 1) & (y == 0)))
    fn = int(np.sum((pred == 0) & (y == 1)))

    st.markdown("**Confusion matrix** (rows = actual, columns = predicted)")
    cm = pd.DataFrame(
        [[tn, fp], [fn, tp]],
        index=["actual: fail (0)", "actual: pass (1)"],
        columns=["predicted: fail (0)", "predicted: pass (1)"],
    )
    st.dataframe(cm)
    accuracy = (tp + tn) / len(y)
    st.metric("Accuracy at this threshold", f"{accuracy:.1%}")


def render_hypothesis_testing_lab() -> None:
    st.subheader("Two-Sample t-test")
    st.caption("Edit the two groups' values and see whether their means differ significantly.")

    col1, col2 = st.columns(2)
    with col1:
        group_a = st.data_editor(
            pd.DataFrame({"Group A": [72.0, 75.0, 68.0, 80.0, 77.0, 74.0]}),
            key="ttest_a",
            num_rows="dynamic",
        )
    with col2:
        group_b = st.data_editor(
            pd.DataFrame({"Group B": [65.0, 70.0, 62.0, 69.0, 66.0, 71.0]}),
            key="ttest_b",
            num_rows="dynamic",
        )

    a = group_a.iloc[:, 0].dropna().to_numpy(dtype=float)
    b = group_b.iloc[:, 0].dropna().to_numpy(dtype=float)

    if len(a) < 2 or len(b) < 2:
        st.info("Add at least 2 values in each group.")
        return

    t_stat, p_value = stats.ttest_ind(a, b)

    col1, col2, col3 = st.columns(3)
    col1.metric("Mean A", f"{a.mean():.2f}")
    col2.metric("Mean B", f"{b.mean():.2f}")
    col3.metric("p-value", f"{p_value:.4f}")

    alpha = 0.05
    if p_value < alpha:
        st.success(
            f"p = {p_value:.4f} < {alpha} -> reject the null hypothesis: "
            "there's a statistically significant difference between the group means."
        )
    else:
        st.info(
            f"p = {p_value:.4f} >= {alpha} -> fail to reject the null "
            "hypothesis: not enough evidence of a real difference between the group means."
        )

    st.divider()
    st.subheader("One-Way ANOVA (3+ groups)")
    st.caption("Compare means across three groups at once.")
    groups_df = st.data_editor(
        pd.DataFrame(
            {
                "Group 1": [72.0, 75.0, 68.0, 80.0, 77.0],
                "Group 2": [65.0, 70.0, 62.0, 69.0, 66.0],
                "Group 3": [80.0, 85.0, 78.0, 90.0, 82.0],
            }
        ),
        key="anova_editor",
        num_rows="dynamic",
    )
    group_arrays = [groups_df[col].dropna().to_numpy(dtype=float) for col in groups_df.columns]
    group_arrays = [g for g in group_arrays if len(g) >= 2]

    if len(group_arrays) < 2:
        st.info("Need at least 2 groups with 2+ values each.")
        return

    f_stat, p_value_anova = stats.f_oneway(*group_arrays)
    col1, col2 = st.columns(2)
    col1.metric("F-statistic", f"{f_stat:.4f}")
    col2.metric("p-value", f"{p_value_anova:.4f}")

    if p_value_anova < alpha:
        st.success(
            f"p = {p_value_anova:.4f} < {alpha} -> at least one group mean "
            "differs significantly from the others."
        )
    else:
        st.info(
            f"p = {p_value_anova:.4f} >= {alpha} -> not enough evidence that "
            "the group means differ."
        )
