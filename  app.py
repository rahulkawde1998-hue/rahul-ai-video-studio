
import streamlit as st
import anthropic
import json

st.set_page_config(
    page_title="Rahul AI Video Studio",
    page_icon="🎬"
)

st.title("🎬 Rahul AI Video Studio")
st.subheader("One Command Hindi AI Video Generator")

api_key = st.text_input(
    "Anthropic API Key",
    type="password"
)

topic = st.text_area(
    "अपनी वीडियो का कमांड लिखें",
    placeholder="भगवद्गीता पर 30 सेकंड की हिंदी वीडियो बनाओ"
)

duration = st.selectbox(
    "वीडियो की लंबाई",
    [15, 30, 60, 90]
)

ratio = st.selectbox(
    "वीडियो फॉर्मेट",
    ["9:16", "16:9", "1:1"]
)

if st.button("🚀 Generate Video Script"):

    if not api_key or not topic:
        st.error("API Key और Topic डालें")

    else:
        try:
            client = anthropic.Anthropic(
                api_key=api_key
            )

            with st.spinner("आपकी वीडियो तैयार हो रही है..."):

                response = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=4000,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
                            Create a Hindi cinematic video plan.

                            Topic: {topic}
                            Duration: {duration} seconds
                            Format: {ratio}

                            Return JSON containing:
                            title,
                            hindi_voiceover,
                            scenes,
                            image_prompt,
                            video_prompt,
                            camera_movement,
                            music_prompt.

                            Make it cinematic and emotional.
                            Return valid JSON only.
                            """
                        }
                    ]
                )

                result = response.content[0].text

                start = result.find("{")
                end = result.rfind("}") + 1

                data = json.loads(result[start:end])

            st.success("वीडियो प्लान तैयार है!")

            st.header(data["title"])

            st.subheader("Hindi Voiceover")
            st.write(data["hindi_voiceover"])

            st.subheader("Video Scenes")
            st.json(data["scenes"])

            st.download_button(
                "Download Video Plan",
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=2
                ),
                file_name="video_plan.json"
            )

        except Exception as e:
            st.error(f"Error: {e}")
