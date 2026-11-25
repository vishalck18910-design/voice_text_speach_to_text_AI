
import streamlit as st

from newv2_TEXT import process_audio


# ----------------------------------
# 1. PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🤖",
    layout="centered"
)


# ----------------------------------
# 2. APPLICATION TITLE
# ----------------------------------

st.title("🤖 AI Voice Assistant")

st.write(
    "Talk to your AI assistant. Ask a question "
    "and listen to its response."
)

st.divider()


# ----------------------------------
# 3. SESSION STATE
# ----------------------------------

if "user_text" not in st.session_state:
    st.session_state.user_text = ""

if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

if "response_audio" not in st.session_state:
    st.session_state.response_audio = None


# ----------------------------------
# 4. RECORD USER VOICE
# ----------------------------------

st.subheader("🎤 Speak to Your Assistant")

audio_input = st.audio_input(
    "Click here to record your question",
    sample_rate=16000
)


# ----------------------------------
# 5. PROCESS USER VOICE
# ----------------------------------

if audio_input is not None:

    st.audio(audio_input)

    if st.button("Ask AI Assistant", type="primary"):

        try:

            with st.spinner(
                "Listening and understanding your question..."
            ):

                audio_bytes = audio_input.getvalue()

                user_text, ai_response, response_audio = (
                    process_audio(audio_bytes)
                )

                st.session_state.user_text = user_text
                st.session_state.ai_response = ai_response
                st.session_state.response_audio = response_audio

            st.success("Your question has been processed!")

        except Exception as error:

            st.error(f"An error occurred: {error}")


# ----------------------------------
# 6. DISPLAY USER QUESTION
# ----------------------------------

if st.session_state.user_text:

    st.divider()

    st.subheader("📝 You Asked")

    st.write(st.session_state.user_text)


# ----------------------------------
# 7. DISPLAY AI RESPONSE
# ----------------------------------

if st.session_state.ai_response:

    st.subheader("🤖 AI Assistant Response")

    st.write(st.session_state.ai_response)


# ----------------------------------
# 8. PLAY AI VOICE
# ----------------------------------

if st.session_state.response_audio:

    st.subheader("🔊 Listen to AI Assistant")

    st.audio(
        st.session_state.response_audio,
        format="audio/mp3"
    )

    st.download_button(
        label="Download AI Voice",
        data=st.session_state.response_audio,
        file_name="ai_response.mp3",
        mime="audio/mp3"
    )


# ----------------------------------
# 9. RESET CONVERSATION
# ----------------------------------

if st.button("Clear Conversation"):

    st.session_state.user_text = ""
    st.session_state.ai_response = ""
    st.session_state.response_audio = None

    st.rerun()


# ----------------------------------
# 10. FOOTER
# ----------------------------------

st.divider()

st.caption(
    "Powered by Groq Whisper, Groq AI and Google Text-to-Speech"
)
