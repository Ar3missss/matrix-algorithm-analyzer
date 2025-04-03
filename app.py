from flask import Flask, render_template, jsonify,request
import numpy as np
import time

app = Flask(__name__)

def generate_matrix(n):
    return np.random.randint(0, 7, (n, n))

def add_matrix(A, B):
    return A + B

def sub_matrix(A, B):
    return A - B

def pad_matrix(A, target_size):
    n, m = A.shape
    new_A = np.zeros((target_size, target_size), dtype=int)
    new_A[:n, :m] = A
    return new_A

def standard_multiply(A, B):
    n = A.shape[0]
    if n <= 2:
        return np.dot(A, B)  
    mid = n // 2
    A11, A12, A21, A22 = A[:mid, :mid], A[:mid, mid:], A[mid:, :mid], A[mid:, mid:]
    B11, B12, B21, B22 = B[:mid, :mid], B[:mid, mid:], B[mid:, :mid], B[mid:, mid:]
    C11 = standard_multiply(A11, B11) + standard_multiply(A12, B21)
    C12 = standard_multiply(A11, B12) + standard_multiply(A12, B22)
    C21 = standard_multiply(A21, B11) + standard_multiply(A22, B21)
    C22 = standard_multiply(A21, B12) + standard_multiply(A22, B22)
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    return C

def strassen_multiply(A, B):
    n = A.shape[0]
    if n <= 2:
        return np.dot(A, B)  
    mid = n // 2
    A11, A12, A21, A22 = A[:mid, :mid], A[:mid, mid:], A[mid:, :mid], A[mid:, mid:]
    B11, B12, B21, B22 = B[:mid, :mid], B[:mid, mid:], B[mid:, :mid], B[mid:, mid:]
    P1 = strassen_multiply(A11, sub_matrix(B12, B22))
    P2 = strassen_multiply(add_matrix(A11, A12), B22)
    P3 = strassen_multiply(add_matrix(A21, A22), B11)
    P4 = strassen_multiply(A22, sub_matrix(B21, B11))
    P5 = strassen_multiply(add_matrix(A11, A22), add_matrix(B11, B22))
    P6 = strassen_multiply(sub_matrix(A12, A22), add_matrix(B21, B22))
    P7 = strassen_multiply(sub_matrix(A21, A11), add_matrix(B11, B12))
    C11 = add_matrix(sub_matrix(add_matrix(P5, P4), P2), P6)
    C12 = add_matrix(P1, P2)
    C21 = add_matrix(P3, P4)
    C22 = add_matrix(sub_matrix(add_matrix(P1, P5), P3), P7)
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    return C

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/multiply', methods=['POST'])
def multiply():
    # Get user input from the webpage
    n = int(request.form['size'])
    
    # Generate matrices
    M1 = generate_matrix(n)
    M2 = generate_matrix(n)
    new_size = 2**int(np.ceil(np.log2(n)))
    M1_padded = pad_matrix(M1, new_size)
    M2_padded = pad_matrix(M2, new_size)
    
    # Compute results and times
    start_standard = time.perf_counter()
    result_standard = standard_multiply(M1_padded, M2_padded)[:n, :n]
    end_standard = time.perf_counter()
    time_standard = end_standard - start_standard
    
    start_strassen = time.perf_counter()  # High-precision start
    result_strassen = strassen_multiply(M1_padded, M2_padded)[:n, :n]
    end_strassen = time.perf_counter()    # High-precision end
    time_strassen = end_strassen - start_strassen

    
    # Validate with numpy
    numpy_result = np.dot(M1, M2)
    is_correct = np.array_equal(result_standard, numpy_result) and np.array_equal(result_strassen, numpy_result)
    
    return jsonify({
        'matrix1': M1.tolist(),
        'matrix2': M2.tolist(),
        'standard_time': time_standard,
        'strassen_time': time_strassen,
        'is_correct': is_correct
    })

if __name__ == '__main__':
    app.run(debug=True)