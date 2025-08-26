import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")


from app.ai_helpers import (
    suggest_story_points,
    extract_subtasks,
    score_story_health,
    suggest_starter_code
)

st.set_page_config(page_title="SmartUserStory AI", layout="wide")

st.title("SmartUserStory: AI-Powered User Story Generator")

# --- Basic layout similar to ADO 'New User Story' ---
with st.form("user_story_form"):
    st.header("Create New User Story")
    title = st.text_input("Title")
    description = st.text_area("Description", help="What is the user need, and why?")
    acceptance_criteria = st.text_area(
        "Acceptance Criteria", help="Conditions for success, e.g., 'Given, When, Then...'"
    )
    submitted = st.form_submit_button("Generate AI Suggestions")

if submitted:
    st.success("AI suggestions ready!")

    # AI logic, using backend helpers
    story_points = suggest_story_points(title, description, acceptance_criteria)
    subtasks = extract_subtasks(title, description, acceptance_criteria)
    health, health_explanation = score_story_health(title, description, acceptance_criteria)
    code_suggestions = suggest_starter_code(subtasks)

    st.header("AI Recommendations")
    st.subheader("Story Points Estimate")
    st.write(f"**Estimated Story Points:** {story_points}")

    st.subheader("Suggested Sub-Tasks")
    st.write(subtasks)

    st.subheader("Story Health Score")
    st.write(f"**{health}** — {health_explanation}")

    st.subheader("Starter Code / Commands")
    for task, code in code_suggestions.items():
        st.markdown(f"**{task}**")
        st.code(code, language="python" if "python" in code.lower() else "bash")

st.markdown("---")
st.caption("Demo • Streamlit + open source models • 2025")
