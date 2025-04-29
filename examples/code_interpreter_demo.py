from together import Together

client = Together()

# Create a code interpreter instance
code_interpreter = client.code_interpreter

# Example 1: Simple print statement
print("Example 1: Simple print")
response = code_interpreter.run(code='print("Hello from Together!")', language="python")
print(f"Status: {response.data.status}")
for output in response.data.outputs:
    print(f"{output.type}: {output.data}")
if response.data.errors:
    print(f"Errors: {response.data.errors}")
print("\n")

# Example 2: Using session for maintaining state
print("Example 2: Using session for state")
response1 = code_interpreter.run(code="x = 42", language="python")
session_id = response1.data.session_id

response2 = code_interpreter.run(
    code='print(f"The value of x is {x}")', language="python", session_id=session_id
)
for output in response2.data.outputs:
    print(f"{output.type}: {output.data}")
if response2.data.errors:
    print(f"Errors: {response2.data.errors}")
print("\n")

# Example 3: More complex computation
print("Example 3: Complex computation")
code = """
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
"""

response = code_interpreter.run(code=code, language="python")
for output in response.data.outputs:
    print(f"{output.type}: {output.data}")
if response.data.errors:
    print(f"Errors: {response.data.errors}")

# Example 4: Uploading and using a file
print("Example 4: Uploading and using a file")

# Define the file content and structure as a dictionary
file_to_upload = {
    "name": "data.txt",
    "encoding": "string",
    "content": "This is the content of the uploaded file.",
}

# Code to read the uploaded file
code_to_read_file = """
try:
    with open('data.txt', 'r') as f:
        content = f.read()
        print(f"Content read from data.txt: {content}")
except FileNotFoundError:
    print("Error: data.txt not found.")
"""

response = code_interpreter.run(
    code=code_to_read_file,
    language="python",
    files=[file_to_upload],  # Pass the file dictionary in a list
)

# Print results
print(f"Status: {response.data.status}")
for output in response.data.outputs:
    print(f"{output.type}: {output.data}")
if response.data.errors:
    print(f"Errors: {response.data.errors}")
print("\n")

# Example 5: Uploading a script and running it
print("Example 5: Uploading a python script and running it")

script_content = "import sys\nprint(f'Hello from {sys.argv[0]}!')"

# Define the script file as a dictionary
script_file = {
    "name": "myscript.py",
    "encoding": "string",
    "content": script_content,
}

code_to_run_script = "!python myscript.py"

response = code_interpreter.run(
    code=code_to_run_script,
    language="python",
    files=[script_file], # Pass the script dictionary in a list
)

# Print results
print(f"Status: {response.data.status}")
for output in response.data.outputs:
    print(f"{output.type}: {output.data}")
if response.data.errors:
    print(f"Errors: {response.data.errors}")
print("\n")

# Example 6: Uploading a base64 encoded image (simulated)

print("Example 6: Uploading a base64 encoded binary file (e.g., image)")

# Example: A tiny 1x1 black PNG image, base64 encoded
# In a real scenario, you would read your binary file and base64 encode its content
tiny_png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

image_file = {
    "name": "tiny.png",
    "encoding": "base64", # Use base64 encoding for binary files
    "content": tiny_png_base64,
}

# Code to check if the file exists and its size (Python doesn't inherently know image dimensions from bytes alone)
code_to_check_file = """
import os
import base64

file_path = 'tiny.png'
if os.path.exists(file_path):
    # Read the raw bytes back
    with open(file_path, 'rb') as f:
        raw_bytes = f.read()
    original_bytes = base64.b64decode('""" + tiny_png_base64 + """')
    print(f"File '{file_path}' exists.")
    print(f"Size on disk: {os.path.getsize(file_path)} bytes.")
    print(f"Size of original decoded base64 data: {len(original_bytes)} bytes.")

else:
    print(f"File '{file_path}' does not exist.")
"""

response = code_interpreter.run(
    code=code_to_check_file,
    language="python",
    files=[image_file],
)

# Print results
print(f"Status: {response.data.status}")
for output in response.data.outputs:
    print(f"{output.type}: {output.data}")
if response.data.errors:
    print(f"Errors: {response.data.errors}")
print("\n")
