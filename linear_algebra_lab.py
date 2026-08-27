"""
Hands-on, interactive practice for Unit 1 & 2 linear algebra concepts:
vector space, linear independence, basis, determinant, rank, eigenvalues/
eigenvectors, orthogonality, and least squares.

Everything here runs locally with NumPy -- no external calls, no cost.
"""

import numpy as np
import pandas as pd
import streamlit as st


def render_matrix_lab() -> None:
    st.subheader("Matrix Explorer")
    st.caption(
        "Edit the matrix below, then see its determinant, rank, and "
        "eigenvalues/eigenvectors computed live."
    )
    default = pd.DataFrame(
        [[2.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]],
        columns=["c1", "c2", "c3"],
    )
    edited = st.data_editor(default, key="matrix_editor", num_rows="fixed")
    A = edited.to_numpy(dtype=float)

    rank = int(np.linalg.matrix_rank(A))
    st.metric("Rank", rank)
    if rank == min(A.shape):
        st.caption("Full rank -> the rows/columns are linearly independent.")
    else:
        st.caption(
            f"Rank {rank} < {min(A.shape)} -> the rows/columns are linearly "
            "*dependent* (at least one is redundant)."
        )

    if A.shape[0] != A.shape[1]:
        st.info("Determinant and eigenvalues need a square matrix -- add/remove a row to match the columns.")
        return

    det = float(np.linalg.det(A))
    st.metric("Determinant", f"{det:.4f}")
    if abs(det) < 1e-9:
        st.caption(
            "Determinant is approximately 0 -> this matrix is *singular* "
            "(not invertible); its columns are linearly dependent."
        )

    eigvals, eigvecs = np.linalg.eig(A)
    st.markdown("**Eigenvalues:**")
    formatted = [
        round(v.real, 4) if abs(v.imag) < 1e-9 else complex(round(v.real, 4), round(v.imag, 4))
        for v in eigvals
    ]
    st.write(formatted)
    st.markdown("**Eigenvectors (one per column, matching each eigenvalue above):**")
    st.dataframe(pd.DataFrame(np.round(eigvecs.real, 4)))
    st.caption("Verify it yourself: for eigenvalue lambda and eigenvector v, A.v should equal lambda.v.")


def render_independence_lab() -> None:
    st.subheader("Linear Independence, Basis & Orthogonality Checker")
    st.caption(
        "Enter 2 or more vectors (one per row) to check independence, whether "
        "they form a basis, and whether pairs are orthogonal."
    )
    default = pd.DataFrame(
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]],
        index=["v1", "v2", "v3"],
        columns=["x", "y", "z"],
    )
    edited = st.data_editor(default, key="vectors_editor", num_rows="dynamic")
    V = edited.to_numpy(dtype=float)
    n_vectors, dim = V.shape

    if n_vectors == 0:
        st.info("Add at least one vector.")
        return

    rank = int(np.linalg.matrix_rank(V))
    col1, col2 = st.columns(2)
    col1.metric("Number of vectors", n_vectors)
    col2.metric("Rank of the set", rank)

    if rank == n_vectors:
        st.success(f"These {n_vectors} vectors are linearly independent.")
        if n_vectors == dim:
            st.info(
                f"Since there are {n_vectors} independent vectors in a "
                f"{dim}-dimensional space, they form a **basis** for it."
            )
        elif n_vectors < dim:
            st.caption(
                f"{n_vectors} independent vectors in {dim}-dimensional space -- "
                "independent, but not enough of them to be a basis on their own."
            )
    else:
        st.error(
            f"These vectors are linearly *dependent* -- only {rank} of the "
            f"{n_vectors} are actually independent (at least one can be written "
            "as a combination of the others)."
        )

    if n_vectors >= 2:
        st.markdown("**Pairwise dot products** (0 means orthogonal):")
        labels = edited.index.astype(str).tolist()
        rows = []
        for i in range(n_vectors):
            for j in range(i + 1, n_vectors):
                dot = float(np.dot(V[i], V[j]))
                rows.append(
                    {
                        "pair": f"{labels[i]} . {labels[j]}",
                        "dot product": round(dot, 4),
                        "orthogonal?": "Yes" if abs(dot) < 1e-9 else "No",
                    }
                )
        st.dataframe(pd.DataFrame(rows), hide_index=True)


def render_least_squares_lab() -> None:
    st.subheader("Least Squares Fit")
    st.caption(
        "Edit the data points below to fit the best straight line y = mx + c "
        "through them -- the same idea behind simple linear regression in Unit 5."
    )
    default = pd.DataFrame(
        {"x": [1.0, 2.0, 3.0, 4.0, 5.0], "y": [2.1, 3.9, 6.2, 7.8, 10.1]}
    )
    edited = st.data_editor(default, key="lsq_editor", num_rows="dynamic")
    x = edited["x"].to_numpy(dtype=float)
    y = edited["y"].to_numpy(dtype=float)

    if len(x) < 2:
        st.info("Add at least 2 points to fit a line.")
        return

    A = np.vstack([x, np.ones_like(x)]).T
    (m, c), _residuals, _rank, _sv = np.linalg.lstsq(A, y, rcond=None)

    col1, col2 = st.columns(2)
    col1.metric("Slope (m)", f"{m:.4f}")
    col2.metric("Intercept (c)", f"{c:.4f}")

    chart_df = pd.DataFrame({"x": x, "actual y": y, "fitted y": m * x + c}).set_index("x")
    st.line_chart(chart_df)
    st.caption(
        f"Fitted line: y = {m:.3f}x + {c:.3f} -- found by minimising the sum "
        "of squared errors between the fitted line and the actual points."
    )
