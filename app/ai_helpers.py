from app.templates import STARTER_TEMPLATES

# --- BASIC DEMO LOGIC ---

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
