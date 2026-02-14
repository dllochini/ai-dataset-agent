# AI Dataset Analysis Agent

**An interactive AI agent for analyzing CSV datasets using LLM-driven reasoning.**  

This project demonstrates an agent that can explore, summarize, and visualize datasets while reasoning step-by-step using a Thought → Action → PAUSE → Observation → Answer loop.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Supported Queries](#supported-queries)


---

## Project Overview

The AI Dataset Analysis Agent:

- Processes user queries about datasets.
- Selects actions such as overview, statistical summary, missing values, correlation analysis, or numeric plots.
- Executes actions on the dataset and provides structured observations.
- Returns a final answer after reasoning, or continues the loop if further steps are required.

This approach demonstrates **agentic behavior** and modular design using Python and Gradio.

---

## Features

- Interactive web interface using **Gradio**.
- Dataset exploration:
  - Overview: rows, columns, column names, data types.
  - Statistical summaries of numeric columns.
  - Check for missing values and duplicate rows.
  - Column-specific insights: mean, min, max, value counts.
  - Correlation matrix of numeric columns.
  - Histogram plots for numeric columns.
- LLM integration via **Groq/OpenAI API**.

---

## Project Structure
```
ai-dataset-agent/
├── app.py # Main entry point (Gradio UI)
├── agent/
│ ├── init.py
│ ├── actions.py # Dataset analysis functions
│ └── agent_logic.py # Agent class + query loop
├── notebooks/ # Optional Colab notebooks for testing
│ └── demo.ipynb
├── data/
│ └── sample.csv # Example dataset
├── plots/ # Generated plots (ignored in Git)
├── .env # API key (ignored in Git)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup & Installation

1. Clone the repository

```bash
git clone https://github.com/<your-username>/ai-dataset-agent.git
cd ai-dataset-agent
```
2. Create a virtual environment

```bash
python -m venv venv
# Windows CMD
venv\Scripts\activate.bat
# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate
```
3. Install dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
4. Add API key

Create a .env file in the project root:
```bash
GROQ_API_KEY=your_api_key_here
```
Usage
Run the Gradio app:

```bash
python app.py
```
- Open the URL shown in the terminal (usually http://127.0.0.1:7860).
- Upload a CSV dataset.
- Ask questions about the dataset — the agent will answer and generate plots if applicable.

## Supported Queries
- Dataset overview: `"Show me an overview of the dataset"`
- Statistical summary: `"Statistical summary"`
- Missing values: `"Check missing values"`
- Duplicate count: `"Count duplicates"`
- Column statistics: `"Mean of column age", "Max of column salary"`
- Value counts: `"Value counts of column department"`
- Correlation matrix: `"Correlation matrix"`
- Numeric plots: `"Plot numeric columns"`

Column names must exactly match the CSV headers.