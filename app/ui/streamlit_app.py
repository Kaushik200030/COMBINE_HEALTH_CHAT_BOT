"""Streamlit frontend for the insurance chatbot."""
import streamlit as st
import requests
from typing import Dict, List
import time

# Page configuration
st.set_page_config(
    page_title="UHC Policy Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .source-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .disclaimer {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border-left: 4px solid #ffc107;
    }
    .confidence-high {
        color: #28a745;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .confidence-low {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def query_api(question: str) -> Dict:
    """Query the API for an answer."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat/query",
            json={"question": question},
            timeout=120  # Increased timeout for LLM calls
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "answer": f"Error connecting to API: {str(e)}",
            "sources": [],
            "confidence": "low",
            "disclaimer": "Please check your API connection."
        }


def display_source(source: Dict):
    """Display a source card."""
    st.markdown(f"""
    <div class="source-card">
        <strong>Policy:</strong> {source.get('policy_title', 'Unknown')}<br>
        <strong>Section:</strong> {source.get('section_name', 'N/A')}<br>
        <strong>Effective Date:</strong> {source.get('effective_date', 'N/A')}<br>
        <strong>Source:</strong> <a href="{source.get('source_url', '#')}" target="_blank">{source.get('source_url', 'N/A')}</a>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main Streamlit application."""
    # Header
    st.markdown('<div class="main-header">🏥 UnitedHealthcare Policy Chatbot</div>', unsafe_allow_html=True)
    st.markdown("Ask questions about UHC commercial medical and drug policies")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This chatbot helps healthcare providers understand:
        - Coverage criteria
        - Documentation requirements
        - Applicable procedure codes
        - Policy guidance
        
        **Note:** Coverage depends on member-specific benefit plans.
        """)
        
        st.header("Example Questions")
        example_questions = [
            "What does the spinal pain ablation policy say?",
            "What procedures are covered for uterine fibroids?",
            "What documentation is required for spinal pain ablation?",
            "Which CPT codes are mentioned in the policy?",
            "Is prior authorization required?"
        ]
        
        for q in example_questions:
            if st.button(q, key=f"example_{q}", use_container_width=True):
                st.session_state.example_question = q
        
        # API Status
        st.header("API Status")
        try:
            health_response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
            if health_response.status_code == 200:
                health_data = health_response.json()
                st.success("✅ API Connected")
                st.info(f"Chunks loaded: {health_data.get('vector_db', {}).get('chunks', 0)}")
            else:
                st.error("❌ API Error")
        except:
            st.error("❌ API Unavailable")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Sources", expanded=False):
                    for source in message.get("sources", []):
                        display_source(source)
                
                # Display disclaimer
                if "disclaimer" in message:
                    st.markdown(f'<div class="disclaimer">⚠️ {message["disclaimer"]}</div>', unsafe_allow_html=True)
    
    # Handle example question
    if "example_question" in st.session_state:
        question = st.session_state.example_question
        del st.session_state.example_question
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Searching policies..."):
                response = query_api(question)
                
                # Display answer
                st.markdown(response["answer"])
                
                # Display confidence
                confidence_class = f"confidence-{response.get('confidence', 'low')}"
                st.markdown(f'<p class="{confidence_class}">Confidence: {response.get("confidence", "low").upper()}</p>', unsafe_allow_html=True)
                
                # Display sources
                if response.get("sources"):
                    with st.expander("📚 Sources", expanded=True):
                        for source in response["sources"]:
                            display_source(source)
                
                # Display disclaimer
                if response.get("disclaimer"):
                    st.markdown(f'<div class="disclaimer">⚠️ {response["disclaimer"]}</div>', unsafe_allow_html=True)
                
                # Store in history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "sources": response.get("sources", []),
                    "disclaimer": response.get("disclaimer", ""),
                    "confidence": response.get("confidence", "low")
                })
        
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about UHC policies..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)
        
        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Searching policies..."):
                response = query_api(prompt)
                
                # Display answer
                st.markdown(response["answer"])
                
                # Display confidence
                confidence_class = f"confidence-{response.get('confidence', 'low')}"
                st.markdown(f'<p class="{confidence_class}">Confidence: {response.get("confidence", "low").upper()}</p>', unsafe_allow_html=True)
                
                # Display sources
                if response.get("sources"):
                    with st.expander("📚 Sources", expanded=True):
                        for source in response["sources"]:
                            display_source(source)
                
                # Display disclaimer
                if response.get("disclaimer"):
                    st.markdown(f'<div class="disclaimer">⚠️ {response["disclaimer"]}</div>', unsafe_allow_html=True)
                
                # Store in history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "sources": response.get("sources", []),
                    "disclaimer": response.get("disclaimer", ""),
                    "confidence": response.get("confidence", "low")
                })


if __name__ == "__main__":
    main()
