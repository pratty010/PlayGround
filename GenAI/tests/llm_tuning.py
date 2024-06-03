import ollama
from time import time

# Set environment variables for GPU selection
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use only the first GPU

# Set performance parameters
response = ollama.chat(
    model='mistral',
    messages=[{'role': 'user', 'content': 'What is the employement post for the person?: /home/ace/PlayGround/GenAI/opt/Alumni_Employment_Verification_Letter.pdf'}],
    options={
        'temperature': 0.7,  # Adjust creativity
        'top_p': 0.9,        # Nucleus sampling
        'num_thread': 8      # Number of threads
        # Add other parameters as needed
    }
)

st = time()
print(response['message']['content'])

et =time()

print(et-st)