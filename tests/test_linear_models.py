from finance_ml.linear_models import LinearRegression
import numpy as np
import pytest

def test_linear_regression():
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    y = np.array([3, 5, 7, 9])
    model1 = LinearRegression(use_intercept=True)
    model1.fit(X, y)
    preds1 = model1.predict(X)
    # Expect slope ≈ 2, intercept ≈ 0
    assert np.allclose(model1.coef_[0], 0, atol=1e-6)   # intercept
    assert np.allclose(model1.coef_[1], 2, atol=1e-6)   # slope
    assert np.allclose(preds1, y, atol=1e-6)

    # Case 2: Without intercept
    model2 = LinearRegression(use_intercept=False, coef=None)
    model2.fit(X, y)
    preds2 = model2.predict(X)
    # Expect slope ≈ 2 (since intercept is forced to 0)
    assert np.allclose(model2.coef_[0], 2, atol=1e-6)
    assert np.allclose(preds2, y, atol=1e-6)

    #assert is a keyword used to check if a condition is true.
    #atol = absolute tolerance (marge d'erreur) 