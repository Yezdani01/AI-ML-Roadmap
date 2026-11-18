
import streamlit as st
import ast
import json
import ollama
from ollama import chat

# -----------------------------------------
# File Paths
# -----------------------------------------

BACKEND_FILE = "/Users/hamzahamza/Desktop/Roadmap/day35/hamzaa.py"

DATA_FILE = "/Users/hamzahamza/Desktop/Roadmap/day35/data.json"

RESPONSE_FILE = "/Users/hamzahamza/Desktop/Roadmap/day35/response.txt"


# -----------------------------------------
# Load Backend Functions
# -----------------------------------------

with open(BACKEND_FILE, "r", encoding="utf-8") as file:
    source_code = file.read()

tree = ast.parse(source_code)

functions = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef)
]

filtered_tree = ast.Module(
    body=functions,
    type_ignores=[]
)

compiled_code = compile(
    filtered_tree,
    BACKEND_FILE,
    "exec"
)

# IMPORTANT: Provide the imports required by hamzaa.py
backend_namespace = {
    "ollama": ollama,
    "chat": chat
}

exec(compiled_code, backend_namespace)

llm_response = backend_namespace["llm_response"]
embeddings = backend_namespace["embeddings"]


# -----------------------------------------
# Streamlit Configuration
# -----------------------------------------

st.set_page_config(
    page_title="Hamza's Python Trainer",
    page_icon="🐍",
    layout="wide"
)


# -----------------------------------------
# Custom Styling
# -----------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #ffffff;
}

.main-title {
    font-size: 36px;
    font-weight: bold;
    color: white;
}

.subtitle {
    color: #a0a0a0;
    font-size: 16px;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# Sidebar
# -----------------------------------------

with st.sidebar:

    st.title("🐍 Python Trainer")

    st.caption("Your personal AI Python tutor")

    st.divider()

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("Model Information")

    st.success("Ollama Connected")
    st.write("LLM: llama3:8b")
    st.write("Embeddings: bge-m3")

    st.divider()

    st.caption("Built by Hamza")


# -----------------------------------------
# Session State
# -----------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------------
# Main UI
# -----------------------------------------

st.markdown(
    '<div class="main-title">🐍 Hamza\'s Python Trainer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Learn Python with your personal AI trainer.</div>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------------------
# Display Previous Messages
# -----------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "user":
            st.markdown(message["content"])

        else:
            st.markdown(message["answer"])

            if message.get("example"):
                with st.expander("💡 View Example"):
                    st.code(message["example"], language="python")


# -----------------------------------------
# Chat Input
# -----------------------------------------

user_input = st.chat_input("Ask me anything about Python...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Your Python Trainer is thinking..."):

            try:

                prompt = f"""Hey you are a professional python trainer for the freshers and this is the question asked by the student {user_input} the student is a fresher graduate and has basic knowledge, answer in a professional manner and return the answer in the json format strictly like this 
                    {{"chat title": "A short 2-3 words of summary of the user's query",
                    "answer":"your detailed, begineer friendly explanation here",
                    "an example":"a small example to help the understanding"
                    }}
                    Follow these important instructions:
                    1.donot answer anything unrelated to python, anything the user asks should be strictly related to the python, programming languages, and computer science only AND if the user asks something which is not related to one of these reply this "Ask related to python and computer science"
                    2. if user greets , greet back and ask for the questions regarding python
                
                    
                """

                # Call existing backend function
                a = llm_response(prompt)

                if a is not None:

                    start_index = a.find("{")
                    end_index = a.rfind("}") + 1

                    if start_index == -1 or end_index == 0:
                        raise ValueError("The model did not return valid JSON.")

                    response = json.loads(a[start_index:end_index])

                    embedding = 'None for now'

                    chunk_data = {
                        "User_input": user_input,
                        "LLM-Response": str(response),
                        "Vector-embeddings": embedding
                    }

                    # Save JSON
                    with open(DATA_FILE, "w", encoding="utf-8") as json_file:
                        json.dump(chunk_data, json_file, indent=4)

                    # Save original response
                    with open(RESPONSE_FILE, "w", encoding="utf-8") as f:
                        f.write(a)

                    # Display response
                    answer = response["answer"]
                    example = response["an example"]

                    st.markdown(answer)

                    with st.expander("💡 View Example"):
                        st.code(example, language="python")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "answer": answer,
                        "example": example
                    })

                else:
                    st.error("No response was generated.")

            except Exception as e:
                st.error(f"Error: {str(e)}")

                st.exception(e)
