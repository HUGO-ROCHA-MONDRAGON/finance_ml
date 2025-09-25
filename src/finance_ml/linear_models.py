import numpy as np

class LinearRegression: 
    def __init__(self, use_intercept, coef):
        self.use_intercept = use_intercept
        self.coef = coef
    
    def fit(self, X, Y):#On fait notre beta
        if self.use_intercept:
            ones = np.ones((X.shape[0],1))
            X = np.hstack([ones, X])  # ajoute une colonne de 1 pour l’intercept
        XtX_inv = np.linalg.inv(X.T @ X)
        self.coef = XtX_inv @ X.T @ Y
        return self 
    
    def predict(self, X):#On calcule notre Y chap en utilisant X et beta
        if self.use_intercept:
            ones = np.ones((X.shape[0],1))
            X = np.hstack([ones, X])  # ajoute une colonne de 1 pour l’intercept
        return X @ self.coef
    

