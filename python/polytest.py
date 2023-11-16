import matplotlib.pyplot as plt

# Function to perform polynomial regression using the least squares method
def polynomial_regression(x, y, degree):
    n = len(x)
    
    # Create the Vandermonde matrix
    X = [[x_i ** d for d in range(degree + 1)] for x_i in x]

    # Transpose the matrix
    X_T = [[X[j][i] for j in range(n)] for i in range(degree + 1)]

    # Multiply X_T with X
    X_T_X = [[sum(a * b for a, b in zip(row_X_T, col_X)) for col_X in zip(*X)] for row_X_T in X_T]

    # Add regularization term to the diagonal elements
    for i in range(degree + 1):
        X_T_X[i][i] += 1e-5
    
    # Multiply X_T with y
    X_T_y = [sum(a * b for a, b in zip(row_X_T, y)) for row_X_T in X_T]

    # Solve the system of linear equations to find the coefficients
    coefficients = solve_system(X_T_X, X_T_y)

    return coefficients

# Function to solve a system of linear equations
def solve_system(A, b):
    n = len(A)

    # Forward elimination
    for i in range(n):
        # Make the diagonal element 1
        diag_value = A[i][i]
        A[i] = [a / diag_value for a in A[i]]
        b[i] /= diag_value

        # Make the elements below the diagonal 0
        for j in range(i + 1, n):
            factor = A[j][i]
            A[j] = [a - factor * b for a, b in zip(A[j], A[i])]
            b[j] -= factor * b[i]

    # Backward substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]

    return x



import math
import random

def easeInOutQuad(t):
    t *= 2
    if t < 1:
        return t * t / 2
    else:
        t -= 1
        return -(t * (t - 2) - 1) / 2

# Generate some sample data
points = 8
x = [i/(points-1) for i in range(points)]
print(x)
y = [easeInOutQuad(i/points) for i in range(points)]
# y = [(math.cos((i/points)*3.1415*4.0)) for i in range(points)]
# y = [120.0,121.5,123.5,126.9,130.0]

# Specify the degree of the polynomial
degree = 8

# Perform polynomial regression
coefficients = polynomial_regression(x, y, degree)

# Print the coefficients
print("Coefficients:", coefficients)

# Generate points for the polynomial curve
res = 120.0
x_curve = [i/(res-1) for i in range(int(min(x)*res), int(max(x)*res))]
print("getting curve")
y_curve = [sum(c * (xi ** d) for d, c in enumerate(coefficients)) for xi in x_curve]
print("got curve")

# Plot the data points and the polynomial curve
plt.scatter(x, y, label='Data Points')
plt.plot(x_curve, y_curve, label=f'Polynomial Regression (Degree {degree})', color='red')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()