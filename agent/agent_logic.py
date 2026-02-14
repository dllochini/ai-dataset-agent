import re
import json
from agent.actions import KNOWN_ACTIONS
from openai import OpenAI

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")


client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


SYSTEM_PROMPT = """
You are a dataset analysis AI agent.

You operate strictly in the following loop:

Thought -> Action -> PAUSE -> Observation -> Thought -> ... -> Answer

GENERAL RULES :

1. You must either:
   - Call exactly ONE Action and then output PAUSE
   OR
   - Output a final Answer.

2. After calling an Action, you MUST format it exactly as:

Action: <action_name>[: <column_name_if_required>]
PAUSE

3. After PAUSE, you will receive:
Observation: <tool_output>

4. After receiving an Observation:
   - You MUST continue reasoning.
   - If the observation already contains all information required to answer the user's question,
     you MUST immediately output:

Answer: <final result>

   - Do NOT call additional actions if the answer can already be produced.
   - Do NOT recompute values that are already present in the Observation.
   - Do NOT repeat the same action unless absolutely necessary.

5. Never output an empty message.
6. Never output PAUSE unless you are calling an Action.
7. Never output Observation yourself.
8. Use exact column names when required.
9. Only perform actions directly necessary to answer the question.
10. If a single action provides enough information, immediately produce Answer.

SPECIAL RULES :

• If the user asks for an overview:
  - Only call dataset_overview.
  - After receiving the observation, immediately produce Answer.

• If the user asks for a statistical summary:
  - Only call statistical_summary.
  - After receiving the observation, immediately produce Answer.
  - Do NOT call column_mean or other actions afterward.

AVAILABLE ACTIONS:

dataset_overview
statistical_summary
missing_values
duplicate_count
column_mean: <column_name>
column_min: <column_name>
column_max: <column_name>
value_counts: <column_name>
correlation_matrix
number_of_rows
number_of_columns
plot_numeric_columns
"""

class Agent:
    def __init__(self, system_prompt):
        self.messages = [{"role": "system", "content": system_prompt}]
    
    def __call__(self, message):
        if not API_KEY:
            return "Error: GROQ_API_KEY not set in .env file."
        
        self.messages.append({"role": "user", "content": message})
        
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=self.messages,
            )
            content = response.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM API: {e}"
        
        self.messages.append({"role": "assistant", "content": content})
        return content


action_re = re.compile(r"Action:\s*(\w+)(?::\s*(.*))?")

def query_loop(question, df, max_iters=8):
    agent = Agent(SYSTEM_PROMPT)
    reasoning_steps = []
    next_input = question
    images = None

    for _ in range(max_iters):
        output = agent(next_input)
        reasoning_steps.append(output)
        
        if not output.strip():
            return "Model returned empty response.", reasoning_steps, images
            
        if "Answer:" in output:
            final_answer = output.split("Answer:", 1)[1].strip()
            return final_answer, reasoning_steps, images
            
        match = action_re.search(output)

        if match:
          
            if "PAUSE" not in output:
                return "Protocol error: Model must output PAUSE after Action.", reasoning_steps, images

            action_name = match.group(1).strip().lower()
            action_input = match.group(2).strip() if match.group(2) else None
            
            if action_name not in KNOWN_ACTIONS:
                message = f"Unable to perform action '{action_name}' — this action is not supported."
                reasoning_steps.append(message)
                next_input = f"Observation: {message}"
                continue
                
            observation = KNOWN_ACTIONS[action_name](df, action_input)
            
            if action_name == "plot_numeric_columns":
                images = observation
                
            try:
                serialized = json.dumps(observation, default=str)
            except:
                serialized = str(observation)

            reasoning_steps.append(f"Observation (JSON): {serialized}")
            next_input = f"Observation: {serialized}"
            continue
            
    return (
        "The agent stopped after too many reasoning steps. "
        "This query may not be supported yet. Please try one of the available actions above.",
        reasoning_steps,
        images
    )

