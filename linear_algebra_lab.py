"""
Hands-on, interactive practice for Unit 1 & 2 linear algebra concepts:
vector space, linear independence, basis, determinant, rank, eigenvalues/
eigenvectors, orthogonality, least squares, linear transformations, systems
of linear equations, and singular value decomposition (SVD).

Everything here runs locally with NumPy/Matplotlib -- no external calls,
no cost.
"""

import matplotlib.pyplot as plt
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
    st.caption("Verify it yourself: for eigenvalue λ and eigenvector v, A·v should equal λ·v.")


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


def _draw_arrow(ax, v, color, label) -> None:
    ax.annotate(
        "",
        xy=(v[0], v[1]),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", color=color, lw=2),
    )
    ax.text(v[0] * 1.05, v[1] * 1.05, label, color=color, fontsize=10)


def render_vector_ops_lab() -> None:
    st.subheader("Vector Operations & Visualization (2D)")
    st.caption(
        "Build intuition for vector addition, scalar multiplication, dot "
        "product, magnitude, and the angle between vectors -- all core to "
        "the idea of a vector space."
    )
    col1, col2 = st.columns(2)
    with col1:
        v1x = st.number_input("v1 . x", value=3.0, step=0.5, key="vecop_v1x")
        v1y = st.number_input("v1 . y", value=1.0, step=0.5, key="vecop_v1y")
    with col2:
        v2x = st.number_input("v2 . x", value=1.0, step=0.5, key="vecop_v2x")
        v2y = st.number_input("v2 . y", value=2.0, step=0.5, key="vecop_v2y")
    c = st.slider("scalar c (applied to v1)", -3.0, 3.0, 2.0, step=0.5)

    v1 = np.array([v1x, v1y])
    v2 = np.array([v2x, v2y])
    v_sum = v1 + v2
    v_scaled = c * v1
    dot = float(np.dot(v1, v2))
    mag1 = float(np.linalg.norm(v1))
    mag2 = float(np.linalg.norm(v2))
    if mag1 > 0 and mag2 > 0:
        cos_theta = float(np.clip(dot / (mag1 * mag2), -1.0, 1.0))
        angle_deg = float(np.degrees(np.arccos(cos_theta)))
    else:
        angle_deg = float("nan")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("|v1|", f"{mag1:.3f}")
    col2.metric("|v2|", f"{mag2:.3f}")
    col3.metric("v1 . v2 (dot)", f"{dot:.3f}")
    col4.metric(
        "angle between",
        f"{angle_deg:.1f} deg" if not np.isnan(angle_deg) else "n/a",
    )

    fig, ax = plt.subplots(figsize=(5, 5))
    _draw_arrow(ax, v1, "tab:blue", "v1")
    _draw_arrow(ax, v2, "tab:orange", "v2")
    _draw_arrow(ax, v_sum, "tab:green", "v1+v2")
    _draw_arrow(ax, v_scaled, "tab:red", f"{c:g}*v1")

    all_pts = np.array([v1, v2, v_sum, v_scaled, [0.0, 0.0]])
    lim = max(1.0, float(np.abs(all_pts).max()) * 1.3)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.axhline(0, color="gray", lw=0.5)
    ax.axvline(0, color="gray", lw=0.5)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_aspect("equal")
    ax.set_title("Vectors in R^2")
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Blue/orange are the vectors you entered; green is their sum "
        "(tip-to-tail); red is a scalar multiple of v1. A dot product near "
        "0 means the vectors are close to orthogonal (perpendicular)."
    )


def render_transformation_lab() -> None:
    st.subheader("Matrix Transformation Visualizer")
    st.caption(
        "See how a 2x2 matrix transforms the plane -- the unit square and "
        "the standard basis vectors e1=(1,0), e2=(0,1) get mapped to new "
        "positions. The determinant tells you the area scale factor (and "
        "whether orientation flips)."
    )
    default = pd.DataFrame([[2.0, 1.0], [1.0, 2.0]], columns=["col 1", "col 2"])
    edited = st.data_editor(default, key="transform_editor", num_rows="fixed")
    A = edited.to_numpy(dtype=float)
    if A.shape != (2, 2):
        st.info("Please keep this a 2x2 matrix.")
        return

    det = float(np.linalg.det(A))
    e1, e2 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    Ae1, Ae2 = A @ e1, A @ e2

    square = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]])
    transformed = square @ A.T

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(square[:, 0], square[:, 1], "--", color="gray", label="unit square")
    ax.fill(transformed[:, 0], transformed[:, 1], alpha=0.3, color="tab:blue")
    ax.plot(transformed[:, 0], transformed[:, 1], "-", color="tab:blue", label="transformed")

    _draw_arrow(ax, e1, "gray", "e1")
    _draw_arrow(ax, e2, "gray", "e2")
    _draw_arrow(ax, Ae1, "tab:red", "A*e1")
    _draw_arrow(ax, Ae2, "tab:green", "A*e2")

    all_pts = np.vstack([square, transformed, [Ae1, Ae2]])
    lim = max(1.0, float(np.abs(all_pts).max()) * 1.3)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.axhline(0, color="gray", lw=0.5)
    ax.axvline(0, color="gray", lw=0.5)
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_title("Unit square before / after A")
    st.pyplot(fig)
    plt.close(fig)

    col1, col2 = st.columns(2)
    col1.metric("Determinant", f"{det:.4f}")
    col2.metric("Area scale factor", f"{abs(det):.4f}")
    if abs(det) < 1e-9:
        st.warning(
            "Determinant is ~0: this matrix squashes the plane onto a line "
            "(or point) -- it's singular / not invertible."
        )
    elif det < 0:
        st.info("Negative determinant: orientation is flipped (like a mirror image) as well as scaled.")
    else:
        st.info("Positive determinant: orientation is preserved.")


def render_linear_system_lab() -> None:
    st.subheader("Systems of Linear Equations")
    st.caption(
        "Edit the coefficients to solve Ax = b. For two equations in two "
        "unknowns, each equation is also drawn as a line -- the solution "
        "is where the lines cross."
    )
    default = pd.DataFrame(
        {"x coeff": [2.0, 1.0], "y coeff": [1.0, -1.0], "= b": [8.0, 1.0]}
    )
    edited = st.data_editor(default, key="linsys_editor", num_rows="dynamic")
    data = edited.to_numpy(dtype=float)
    if data.shape[0] < 1 or data.shape[1] < 2:
        st.info("Add at least one equation with at least one variable.")
        return

    A = data[:, :-1]
    b = data[:, -1]
    n_eqs, n_vars = A.shape

    rank_A = int(np.linalg.matrix_rank(A))
    aug = np.column_stack([A, b])
    rank_aug = int(np.linalg.matrix_rank(aug))

    if rank_A < rank_aug:
        st.error("No solution -- the system is inconsistent (rank(A) < rank([A|b])).")
    elif rank_A == n_vars:
        x, *_ = np.linalg.lstsq(A, b, rcond=None)
        st.success("Unique solution:")
        for i, xi in enumerate(x):
            st.write(f"x{i + 1} = {xi:.4f}")
    else:
        x, *_ = np.linalg.lstsq(A, b, rcond=None)
        st.warning(
            f"Infinitely many solutions -- rank(A) = {rank_A} is less than "
            f"the number of variables ({n_vars})."
        )
        st.caption("One particular (minimum-norm) solution:")
        for i, xi in enumerate(x):
            st.write(f"x{i + 1} ~ {xi:.4f}")

    if n_vars == 2:
        fig, ax = plt.subplots(figsize=(5, 5))
        xs = np.linspace(-10, 10, 200)
        for i in range(n_eqs):
            a1, a2, bi = A[i, 0], A[i, 1], b[i]
            if abs(a2) > 1e-9:
                ys = (bi - a1 * xs) / a2
                ax.plot(xs, ys, label=f"eq {i + 1}")
            elif abs(a1) > 1e-9:
                ax.axvline(bi / a1, label=f"eq {i + 1}")
        if rank_A == rank_aug == 2:
            x, *_ = np.linalg.lstsq(A, b, rcond=None)
            ax.plot(x[0], x[1], "ko", markersize=8, label="solution")
        ax.axhline(0, color="gray", lw=0.5)
        ax.axvline(0, color="gray", lw=0.5)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend()
        ax.set_title("Equations as lines in the xy-plane")
        st.pyplot(fig)
        plt.close(fig)


def render_svd_lab() -> None:
    st.subheader("Singular Value Decomposition (SVD)")
    st.caption(
        "Every matrix A can be decomposed as A = U * Sigma * V^T -- a "
        "rotation/reflection, then a scaling along orthogonal axes, then "
        "another rotation/reflection. This is the engine behind PCA (see "
        "the Data Wrangling & EDA Lab)."
    )
    default = pd.DataFrame([[3.0, 0.0], [4.0, 5.0]], columns=["col 1", "col 2"])
    edited = st.data_editor(default, key="svd_editor", num_rows="dynamic")
    A = edited.to_numpy(dtype=float)
    if A.shape[0] < 1 or A.shape[1] < 1:
        st.info("Enter a non-empty matrix.")
        return

    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    st.markdown("**U** (left singular vectors)")
    st.dataframe(pd.DataFrame(U).round(4))
    st.markdown("**Singular values (diagonal of Sigma)**")
    st.dataframe(pd.DataFrame({"singular value": S}).round(4))
    st.markdown("**V^T** (right singular vectors, transposed)")
    st.dataframe(pd.DataFrame(Vt).round(4))

    reconstructed = U @ np.diag(S) @ Vt
    max_err = float(np.max(np.abs(A - reconstructed)))
    st.caption(f"Reconstruction check: max |A - U*Sigma*V^T| = {max_err:.2e} (should be ~0).")

    if A.shape == (2, 2):
        theta = np.linspace(0, 2 * np.pi, 100)
        circle = np.stack([np.cos(theta), np.sin(theta)])
        after_A = A @ circle

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.plot(circle[0], circle[1], "--", color="gray", label="unit circle")
        ax.plot(after_A[0], after_A[1], "-", color="tab:blue", label="A * unit circle")
        for i in range(min(2, len(S))):
            axis_vec = S[i] * U[:, i]
            ax.annotate(
                "",
                xy=(axis_vec[0], axis_vec[1]),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="tab:red", lw=2),
            )
        ax.axhline(0, color="gray", lw=0.5)
        ax.axvline(0, color="gray", lw=0.5)
        lim = max(1.0, float(np.abs(after_A).max()) * 1.3)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend()
        ax.set_title("A maps the unit circle to an ellipse")
        st.pyplot(fig)
        plt.close(fig)
        st.caption(
            "The red arrows are the semi-axes of the resulting ellipse, "
            "with lengths equal to the singular values -- this is exactly "
            "why SVD is described as rotate, then stretch along orthogonal "
            "axes, then rotate again."
        )
