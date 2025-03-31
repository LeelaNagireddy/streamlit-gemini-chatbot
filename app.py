import streamlit as st
import google.generativeai as genai

# Configure page
st.set_page_config(page_title="Gemini ChatBot 🤖", page_icon="🤖")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None

if not GEMINI_API_KEY:
    st.error("❌ API Key missing. Add it to secrets.toml or input below:")
    key_input = st.text_input("Enter Gemini API Key (will not be saved)", type="password")
    if key_input:
        GEMINI_API_KEY = key_input
        genai.configure(api_key=GEMINI_API_KEY)
        st.success("✅ Key loaded for this session!")
    else:
        st.stop()
else:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Chat Logic ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me anything."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                temperature = 0.7  
                max_tokens = 1000
                model = genai.GenerativeModel("gemini-1.5-pro-latest")
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens
                    )
                )
                full_response = response.text
            except Exception as e:
                full_response = f"⚠️ Error: {str(e)}"
                st.error(full_response)
                        # Aligned with 'except'
        
        st.write(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})