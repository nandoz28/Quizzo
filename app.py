
import json
import random
import html
import streamlit as st

st.set_page_config(
    page_title="Quizzo - NPTEL Practice",
    page_icon="📝",
    layout="centered"
)

# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown("""
<style>
/* Main app spacing */
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Answer option spacing */
div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* Individual option boxes */
div[data-testid="stRadio"] div[role="radiogroup"] label {
    border: 1px solid #D1D5DB;
    border-radius: 12px;
    padding: 14px 16px;
    background-color: var(--secondary-background-color);
    cursor: pointer;
    transition: border-color 0.2s, background-color 0.2s;
    width: 100%;
    box-sizing: border-box;
}

/* Hover effect */
div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    border-color: #3984F7;
}

/* Selected option */
div[data-testid="stRadio"] div[role="radiogroup"]
label:has(input:checked) {
    border: 2px solid #3984F7;
    background-color: rgba(57, 132, 247, 0.12);
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 500;
}

/* Quiz question spacing */
.quiz-heading {
    padding: 8px 0;
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# LOAD QUESTION BANK
# -------------------------
try:
    with open("questions.json", "r", encoding="utf-8") as file:
        questions = json.load(file)

    if not isinstance(questions, list):
        st.error("questions.json must contain a JSON list of questions.")
        st.stop()

except FileNotFoundError:
    st.error("questions.json was not found. Place it in your Quizzo project folder.")
    st.stop()

except json.JSONDecodeError:
    st.error("questions.json is empty or contains invalid JSON.")
    st.stop()


# -------------------------
# INITIALIZE APP STATE
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "courses"

if "course" not in st.session_state:
    st.session_state.course = None

if "week" not in st.session_state:
    st.session_state.week = None

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "submitted" not in st.session_state:
    st.session_state.submitted = False


# -------------------------
# START QUIZ
# -------------------------
def start_quiz(course, week):
    pool = [
        q for q in questions
        if q["course"] == course and q["week"] == week
    ]

    if not pool:
        st.warning("No questions have been added for this week yet.")
        return

    st.session_state.course = course
    st.session_state.week = week
    st.session_state.quiz = random.sample(pool, len(pool))
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.page = "quiz"


# -------------------------
# PAGE 1: COURSES
# -------------------------
if st.session_state.page == "courses":

    st.title("📝 Quizzo")
    st.subheader("NPTEL Quiz Practice")

    st.write(
        "Welcome to Quizzo! Select a course and test your knowledge."
    )

    courses = sorted({
        q["course"] for q in questions
        if "course" in q
    })

    if not courses:
        st.info("Add courses and questions to questions.json first.")

    for course in courses:
        if st.button(
            f"📘  {course}",
            key=f"course_{course}",
            use_container_width=True
        ):
            st.session_state.course = course
            st.session_state.page = "weeks"
            st.rerun()


# -------------------------
# PAGE 2: WEEKS
# -------------------------
elif st.session_state.page == "weeks":

    st.title(f"📚 {st.session_state.course}")
    st.subheader("Select a Week")
    st.write("Choose a week to begin your practice quiz.")

    available_weeks = {
        q["week"] for q in questions
        if q.get("course") == st.session_state.course
    }

    # Display all 12 weeks in a three-column layout
    for start in range(1, 13, 3):
        columns = st.columns(3)

        for column, week in zip(
            columns,
            range(start, min(start + 3, 13))
        ):
            with column:
                if week in available_weeks:
                    label = f"📝 Week {week}"
                    disabled = False
                else:
                    label = f"🔒 Week {week}"
                    disabled = True

                if st.button(
                    label,
                    key=f"week_{week}",
                    disabled=disabled,
                    use_container_width=True
                ):
                    start_quiz(st.session_state.course, week)
                    st.rerun()

    st.write("")

    if st.button("← Back to Courses", use_container_width=True):
        st.session_state.page = "courses"
        st.rerun()


# -------------------------
# PAGE 3: QUIZ
# -------------------------
elif st.session_state.page == "quiz":

    quiz = st.session_state.quiz

    st.title("📝 Quizzo")
    st.subheader(
        f"{st.session_state.course} — Week {st.session_state.week}"
    )

    st.caption(f"{len(quiz)} questions in this quiz")

    if not st.session_state.submitted:

        # Overall completion progress
        answered_count = sum(
            q["id"] in st.session_state.answers
            for q in quiz
        )

        progress = answered_count / len(quiz) if quiz else 0
        st.progress(progress)
        st.caption(
            f"{answered_count} of {len(quiz)} questions answered"
        )

        for index, q in enumerate(quiz, start=1):

            st.markdown(
                f'<div class="quiz-heading"><h3>Question {index}</h3></div>',
                unsafe_allow_html=True
            )

            st.markdown(f"**{q['question']}**")

            options = list(q["options"].keys())
            previous = st.session_state.answers.get(q["id"])

            # Boxed, clickable radio options
            selected = st.radio(
                "Choose your answer:",
                options=options,
                format_func=lambda key, opts=q["options"]: (
                    f"{key}. {opts[key]}"
                ),
                index=(
                    options.index(previous)
                    if previous in options
                    else None
                ),
                key=f"question_{q['id']}",
                label_visibility="collapsed",
                disabled=False
            )

            if selected is not None:
                st.session_state.answers[q["id"]] = selected

            st.divider()

        st.write("")

        if st.button(
            "Submit Quiz",
            type="primary",
            use_container_width=True
        ):
            if len(st.session_state.answers) < len(quiz):
                st.warning(
                    "Please answer every question before submitting."
                )
            else:
                st.session_state.submitted = True
                st.rerun()

    # -------------------------
    # RESULTS AND ANSWER REVIEW
    # -------------------------
    else:

        score = sum(
            st.session_state.answers.get(q["id"]) == q["answer"]
            for q in quiz
        )

        total = len(quiz)
        accuracy = (score / total * 100) if total else 0

        st.success("🎉 Quiz completed!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Your Score", f"{score}/{total}")

        with col2:
            st.metric("Accuracy", f"{accuracy:.1f}%")

        st.progress(accuracy / 100)

        if accuracy >= 80:
            st.success("Excellent work! Keep it up.")
        elif accuracy >= 50:
            st.info("Good effort! Review the explanations to improve.")
        else:
            st.warning("Keep practising. You'll improve with every attempt.")

        st.subheader("📋 Answer Review")

        for index, q in enumerate(quiz, start=1):

            selected = st.session_state.answers.get(q["id"])
            correct = q["answer"]

            st.markdown(f"**Q{index}. {q['question']}**")

            if selected == correct:
                st.success(
                    f"✓ Your answer: {selected}. "
                    f"{q['options'][selected]}"
                )
            else:
                selected_text = (
                    q["options"].get(selected, "Not answered")
                    if selected is not None
                    else "Not answered"
                )

                st.error(
                    f"Your answer: {selected or '—'}. {selected_text}"
                )

                st.success(
                    f"Correct answer: {correct}. {q['options'][correct]}"
                )

            explanation = q.get("explanation", "").strip()

            if explanation:
                st.info(f"💡 Explanation: {explanation}")

            st.divider()

        if st.button(
            "🔄 Try This Week Again",
            type="primary",
            use_container_width=True
        ):
            start_quiz(
                st.session_state.course,
                st.session_state.week
            )
            st.rerun()

    # Back navigation
    st.write("")

    if st.button("← Back to Weeks", use_container_width=True):
        st.session_state.page = "weeks"
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.rerun()
