"""
Hands-on, interactive practice for Unit 4: data wrangling and exploratory
data analysis (EDA) -- cleaning messy data, descriptive statistics,
correlation, and PCA.

Ships with a small built-in synthetic "messy" dataset so it works with no
setup; students can also upload their own CSV. Everything runs locally
with NumPy/Pandas -- no external calls, no cost.
"""

import numpy as np
import pandas as pd
import streamlit as st


def _messy_sample_df() -> pd.DataFrame:
    """A small synthetic 'messy' dataset with duplicates, missing values,
    and inconsistent text -- deliberately, so there's something real to
    clean."""
    rng = np.random.default_rng(7)
    n = 24
    names = [f"Student {i+1}" for i in range(n)]
    study_hours = np.round(rng.normal(6, 2, n).clip(0, 14), 1)
    attendance = np.round(rng.normal(80, 12, n).clip(30, 100), 0)
    exam_score = np.round(
        30 + 6 * study_hours + 0.3 * attendance + rng.normal(0, 8, n), 1
    ).clip(0, 100)
    grade_label = rng.choice(["pass", "Pass", "PASS", "fail", "Fail"], size=n)

    df = pd.DataFrame(
        {
            "student": names,
            "study_hours": study_hours,
            "attendance_pct": attendance,
            "exam_score": exam_score,
            "grade_label": grade_label,
        }
    )

    # Inject missing values
    for col in ["study_hours", "attendance_pct", "exam_score"]:
        idx = rng.choice(n, size=2, replace=False)
        df.loc[idx, col] = np.nan

    # Inject exact duplicate rows
    df = pd.concat([df, df.iloc[[2, 9]]], ignore_index=True)

    return df


def render_cleaning_lab() -> None:
    st.subheader("Clean the Data")
    st.caption(
        "A small synthetic 'messy' dataset -- notice the duplicate rows, "
        "missing values, and inconsistent text in `grade_label`. Try the "
        "cleaning steps below and watch the data change."
    )

    if "messy_df" not in st.session_state:
        st.session_state.messy_df = _messy_sample_df()

    df = st.session_state.messy_df
    st.markdown(f"**Raw data** ({len(df)} rows)")
    st.dataframe(df, height=250)

    col1, col2, col3 = st.columns(3)
    with col1:
        drop_dupes = st.checkbox("Drop duplicate rows", value=False)
    with col2:
        drop_na = st.checkbox("Drop rows with missing values", value=False)
    with col3:
        normalize_text = st.checkbox("Normalise grade_label to lowercase", value=False)

    cleaned = df.copy()
    if normalize_text:
        cleaned["grade_label"] = cleaned["grade_label"].str.lower()
    if drop_dupes:
        cleaned = cleaned.drop_duplicates()
    if drop_na:
        cleaned = cleaned.dropna()

    st.markdown(f"**Cleaned data** ({len(cleaned)} rows)")
    st.dataframe(cleaned, height=250)

    st.caption(
        f"Started with {len(df)} rows and {df.duplicated().sum()} exact "
        f"duplicates, {df.isna().any(axis=1).sum()} rows with at least one "
        f"missing value, and {df['grade_label'].nunique()} distinct spellings "
        "of grade_label. This is exactly the kind of cleanup 'data wrangling' "
        "refers to before any analysis can be trusted."
    )

    if st.button("Reset sample data"):
        st.session_state.messy_df = _messy_sample_df()
        st.rerun()


def _get_working_df(key_suffix: str) -> pd.DataFrame:
    st.markdown("Use the cleaned sample data, or upload your own CSV.")
    uploaded = st.file_uploader(
        "Upload a CSV (optional)", type=["csv"], key=f"eda_upload_{key_suffix}"
    )
    if uploaded is not None:
        return pd.read_csv(uploaded)
    df = st.session_state.get("messy_df", _messy_sample_df())
    return df.drop_duplicates().dropna()


def render_descriptive_lab() -> None:
    st.subheader("Descriptive Statistics & Correlation")
    df = _get_working_df(key_suffix="descriptive")
    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.empty:
        st.info("No numeric columns found in this data.")
        return

    st.markdown("**Descriptive statistics**")
    st.dataframe(numeric_df.describe().round(3))

    if numeric_df.shape[1] >= 2:
        st.markdown("**Correlation matrix**")
        corr = numeric_df.corr().round(3)
        try:
            st.dataframe(corr.style.background_gradient(cmap="coolwarm", vmin=-1, vmax=1))
        except Exception:
            st.dataframe(corr)
        st.caption(
            "Values near +1 or -1 indicate a strong linear relationship; "
            "values near 0 indicate little linear relationship (see the "
            "Practice Quiz question on this)."
        )
    else:
        st.info("Need at least 2 numeric columns to compute correlations.")


def render_pca_lab() -> None:
    st.subheader("PCA Explorer")
    st.caption(
        "Principal Components Analysis projects multivariate data onto the "
        "directions of greatest variance -- useful for visualising "
        "high-dimensional data in 2D."
    )
    df = _get_working_df(key_suffix="pca")
    numeric_df = df.select_dtypes(include=[np.number]).dropna()

    if numeric_df.shape[1] < 2 or numeric_df.shape[0] < 3:
        st.info("Need at least 2 numeric columns and 3 rows to run PCA.")
        return

    X = numeric_df.to_numpy(dtype=float)
    X_centered = X - X.mean(axis=0)
    X_scaled = X_centered / (X_centered.std(axis=0) + 1e-12)

    U, S, Vt = np.linalg.svd(X_scaled, full_matrices=False)
    explained_variance = (S ** 2) / (X_scaled.shape[0] - 1)
    explained_ratio = explained_variance / explained_variance.sum()

    scores = X_scaled @ Vt.T
    n_components = min(2, scores.shape[1])
    pc_df = pd.DataFrame(
        scores[:, :n_components],
        columns=[f"PC{i+1}" for i in range(n_components)],
    )

    if n_components == 2:
        st.scatter_chart(pc_df, x="PC1", y="PC2")
    else:
        st.line_chart(pc_df)

    st.markdown("**Variance explained by each component**")
    st.bar_chart(
        pd.DataFrame(
            {"variance explained": explained_ratio[: min(5, len(explained_ratio))]},
            index=[f"PC{i+1}" for i in range(min(5, len(explained_ratio)))],
        )
    )
    st.caption(
        f"The first component alone explains "
        f"{explained_ratio[0]:.1%} of the total variance in the numeric "
        f"columns of this data."
    )
