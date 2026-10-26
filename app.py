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

        retry_label = (
            "🔄 Try Full Mock Test Again"
            if st.session_state.week == "Full Mock Test"
            else "🔄 Try This Week Again"
        )
        if st.button(
            retry_label,
            type="primary",
            use_container_width=True
        ):
            if st.session_state.week == "Full Mock Test":
                start_quiz(st.session_state.course, full_mock=True)
            else:
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
