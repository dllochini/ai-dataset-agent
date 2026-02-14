import gradio as gr
import pandas as pd
from agent.agent_logic import query_loop

description = """
Welcome! This AI Dataset Analysis Agent helps you explore and analyze your datasets interactively.

You can ask it to:

- **Get an overview of the dataset**: rows, columns, column names, and data types.  
- **Generate a statistical summary** of numeric columns, including mean, standard deviation, min, max, and percentiles.  
- **Check for missing values** in any column.  
- **Count duplicate rows** in the dataset.  
- **Get column-specific insights** such as mean, min, max, or value counts.  
- **Compute the correlation matrix** between numeric columns.  
- **Get the total number of rows or columns**.  
- **Visualize numeric columns** with histograms (plots will appear in the gallery).

The agent uses step-by-step reasoning to answer your questions. Type your query about the dataset, and it will show its reasoning along with a final answer.  

*Note:* Only supported actions from the above list can be performed. Queries outside these actions may not be answered.
"""

current_df = None

def load_file(file):
    global current_df
    if file is None:
        return "No file uploaded.", None
    current_df = pd.read_csv(file) 
    return f"Dataset '{file}' loaded successfully with {current_df.shape[0]} rows and {current_df.shape[1]} columns.", None

def chat_interface(file, user_input):
    global current_df
    
    if current_df is None:
        if file is None:
            return "Please upload a dataset first.", None
        current_df = pd.read_csv(file)
        
    if not user_input:
        return "Please enter a question about the dataset.", None
        
    answer, reasoning, images = query_loop(user_input, current_df)
    return answer, images
    
demo = gr.Interface(
    fn=chat_interface,
    inputs=[
        gr.File(label="Upload your CSV dataset", type="filepath"),
        gr.Textbox(label="Ask a question about your dataset")
    ],
    outputs=[
        gr.Markdown(label="Agent Response"),
        gr.Gallery(label="Generated Plots")
    ],
    title="AI Dataset Analysis Agent",
    description=description
)


demo.launch(share=True)