import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")
st.title("✍️ AI Content Assistant")
st.caption("Generate complete social posts tailored to your platform, audience, and tone.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key", type="password", help="Get a free key at console.groq.com")

# Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Twitter / X", "Facebook"])
        content_type = st.selectbox("Content Type", ["Educational", "Promotional", "Storytelling", "Thought Leadership"])
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Casual", "Enthusiastic", "Humorous", "Persuasive"])
        target_audience = st.text_input("Target Audience", placeholder="e.g., Tech Founders, Fitness Enthusiasts")

    topic = st.text_area("Topic / Main Idea", placeholder="e.g., Why early-stage startups should prioritize customer feedback")
    submit_btn = st.form_submit_button("Generate Content")

# Generation Logic
if submit_btn:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not topic or not target_audience:
        st.warning("Please fill in both Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""
            You are an expert social media manager. Create a high-engaging post based on the parameters below.

            - Platform: {platform}
            - Content Type: {content_type}
            - Tone: {tone}
            - Target Audience: {target_audience}
            - Main Topic: {topic}

            Format the output cleanly:
            1. Post Caption/Body (optimized with line breaks and appropriate emojis)
            2. Call to Action (CTA)
            3. 5-10 Relevant Hashtags
            """

            with st.spinner("Generating post..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                generated_content = response.choices[0].message.content

            st.success("Content Generated!")
            st.markdown("---")
            st.markdown(generated_content)

        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
