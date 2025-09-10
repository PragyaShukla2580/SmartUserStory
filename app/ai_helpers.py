from app.templates import STARTER_TEMPLATES
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import ast
import re
# --- BASIC DEMO LOGIC ---
import json
import os

# Go up one directory from /app to project root, then into /config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")

# Normalize the path so it works cross-platform
CONFIG_PATH = os.path.normpath(CONFIG_PATH)

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

# Now you can access values
API_KEY = config.get("api_key")
MODEL_NAME = config.get("model_name")
BASE_URL = config.get("base_url")
llm = ChatOpenAI(
    openai_api_base=BASE_URL,
    openai_api_key=API_KEY,
    model_name=MODEL_NAME,
    max_tokens=1000,
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0.2
)

def generate_response(title, description, acceptance_criteria):
    user_input = f"Userstory title: {title}, Userstory description: {description}, Acceptance criteria: {acceptance_criteria}"
    system_prompt = """You are an assistant that helps refine and break down user stories for agile development. 
    Your task is to carefully read a user story (title, description, and acceptance criteria) and then produce a structured response.

    Follow these steps:
    1. Understand the details of the user story based on the given title, description, and acceptance criteria.
    2. Rate the user story on its clarity, completeness, and level of detail. The rating must be a score from 0 to 10.
    3. Provide a short reasoning (2-3 sentences) that explains why you gave this rating.
    4. Estimate the number of story points for the user story. The number must be an integer and should reflect its complexity.
    5. Rewrite and improve the user story description using the given title, description, and acceptance criteria.
    6. Generate a list of high-value sub-tasks needed to complete the user story. The number of sub-tasks should depend on the story’s complexity.
    7. Decide whether the user story requires coding. If yes, provide a few useful, high-level helper code snippets relevant to completing the story. If no, say there is no code for this userstory.

    Note: Response Format (must strictly follow this dictionary structure, with no extra text):
    {0}"""
    response_format = '''{{
    'user story rating': <integer between 0 and 10>,
    'rating reasoning': '<2-3 sentence explanation>',
    'story points': <integer>,
    'improved user story description': '<rewritten description>',
    'sub tasks': ["<sub task 1>", "<sub task 2>", ...],
    'useful code snippets': """<multi-line string of code snippets>"""
    }}'''

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt.format(response_format)),
        ("user", "{input}")
    ])

    chain = prompt | llm
    response = chain.invoke({"input": user_input}).content


    match = re.search(r"\{(.*)\}", response, re.DOTALL)
    if match:
        result = "{" + match.group(1) + "}"
    print(result)

    response_dict = ast.literal_eval(result)
    return response_dict

def suggest_story_points(title, description, acceptance_criteria):
    """Very simple heuristic: Longer stories => higher points"""
    text = f"{title} {description} {acceptance_criteria}"
    n_words = len(text.split())
    # Fibonacci bucket: 1 (tiny), 2 (small), 3 (medium), 5 (large), 8+ (epic)
    if n_words < 15:
        return 1
    elif n_words < 40:
        return 2
    elif n_words < 80:
        return 3
    elif n_words < 160:
        return 5
    else:
        return 8

def extract_subtasks(title, description, acceptance_criteria):
    """Extract possible sub-tasks based on keywords and templates."""
    subtasks = []
    # Demo rules - expand as logic grows!
    if any(k in title.lower() or description.lower() for k in ["login", "authenticate"]):
        subtasks += ["Build login form", "Backend login logic", "Tests for login", "Update user doc"]
    if any(k in title.lower() or description.lower() for k in ["api", "endpoint"]):
        subtasks += ["Develop endpoint", "Write API tests", "Document API usage"]
    if "test" in title.lower() or "test" in description.lower():
        subtasks += ["Create test skeleton", "Write unit tests", "Document tests"]
    # Always include generic subtasks
    if not subtasks:
        subtasks = ["Design", "Develop", "Test", "Document"]
    return subtasks

def score_story_health(title, description, acceptance_criteria):
    """Check for typical user story completeness: Role, Action, Value, and acceptance criteria"""
    missing = []
    # Role check (As a...), Action check (I want...), Value check (so that...)
    role_present = "as a" in (title + description).lower()
    action_present = "i want" in (title + description).lower()
    value_present = "so that" in (title + description).lower()
    criteria_present = bool(acceptance_criteria.strip())

    if not role_present:
        missing.append("persona/role")
    if not action_present:
        missing.append("goal/action")
    if not value_present:
        missing.append("business value")
    if not criteria_present:
        missing.append("acceptance criteria")
    
    if missing:
        health = "Weak"
        explanation = f"Missing: {', '.join(missing)}."
    else:
        health = "Strong"
        explanation = "All core story elements are present."
    return health, explanation

def suggest_starter_code(subtasks):
    """Return code snippets for known subtasks from predefined templates."""
    output = {}
    for task in subtasks:
        for keyword in STARTER_TEMPLATES:
            if keyword in task.lower():
                output[task] = STARTER_TEMPLATES[keyword]
    return output if output else {"": "No code suggestions available for these sub-tasks."}
