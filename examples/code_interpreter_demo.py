from together import Together

client = Together()

# Create a code interpreter instance
code_interpreter = client.code_interpreter

# Example 1: Simple print statement
print("Example 1: Simple print")
response = code_interpreter.run(
    code='print("Hello from Together!")',
    language="python"
)
print(f"Status: {response.data.status}")
for output in response.data.outputs:
    print(f"{output.type}: {output.data}")
if response.data.errors:
    print(f"Errors: {response.data.errors}")
print("\n")

# Example 2: Using session for maintaining state
print("Example 2: Using session for state")
response1 = code_interpreter.run(
    code='x = 42',
    language="python"
)
session_id = response1.data.session_id

response2 = code_interpreter.run(
    code='print(f"The value of x is {x}")',
    language="python",
    session_id=session_id
)
for output in response2.data.outputs:
    print(f"{output.type}: {output.data}")
if response2.data.errors:
    print(f"Errors: {response2.data.errors}")
print("\n")

# Example 3: More complex computation
print("Example 3: Complex computation")
code = '''
!pip install numpy
import numpy as np

# Create a random matrix
matrix = np.random.rand(3, 3)
print("Random matrix:")
print(matrix)

# Calculate eigenvalues
eigenvalues = np.linalg.eigvals(matrix)
print("\\nEigenvalues:")
print(eigenvalues)
'''

response = code_interpreter.run(
    code=code,
    language="python"
)
for output in response.data.outputs:
    print(f"{output.type}: {output.data}")
if response.data.errors:
    print(f"Errors: {response.data.errors}")
