"""Prompt templates for the chatbot."""
from typing import List, Dict


SYSTEM_PROMPT = """You are a helpful assistant that answers questions about UnitedHealthcare (UHC) commercial medical and drug policies. 
Your role is to help doctors, clinic staff, and hospital staff understand policy coverage, documentation requirements, and applicable procedure codes.

IMPORTANT GUIDELINES:
1. Only answer based on the provided policy documents. If information is not in the provided context, say so.
2. Always cite the specific policy name and source when providing answers.
3. Clearly state that coverage depends on member-specific benefit plan documents, which may override policy guidance.
4. Do NOT provide medical advice. These policies are informational only.
5. Prior authorization requirements are maintained separately and may not be in the policy documents.
6. If asked about prior authorization, indicate that separate prior-auth resources should be consulted.
7. If multiple policy versions exist, prioritize the most recent effective date.
8. If a procedure is not found, suggest checking the exact procedure name or related policies.

Be concise, accurate, and always include source citations."""


def build_user_prompt(query: str, context_chunks: List[Dict[str, str]]) -> str:
    """Build the user prompt with context chunks."""
    context_text = "\n\n---\n\n".join([
        f"Policy: {chunk.get('policy_title', 'Unknown')}\n"
        f"Section: {chunk.get('section_name', 'N/A')}\n"
        f"Effective Date: {chunk.get('effective_date', 'N/A')}\n"
        f"Source: {chunk.get('source_url', 'N/A')}\n"
        f"Content:\n{chunk.get('chunk_text', '')}"
        for chunk in context_chunks
    ])
    
    return f"""Based on the following UnitedHealthcare policy documents, answer the user's question.

POLICY DOCUMENTS:
{context_text}

USER QUESTION: {query}

Provide a clear, accurate answer with citations. If the information is not available in the provided documents, state that clearly."""


NO_RESULTS_PROMPT = """I couldn't find relevant policy information for your question. This could mean:
1. The procedure or service may not be covered under UHC commercial policies
2. The procedure name might be different in the policy documents
3. The information might be in a different policy category

Please try:
- Checking the exact procedure or service name
- Searching for related terms or procedure codes
- Consulting the UHC provider portal directly

Note: Coverage decisions ultimately depend on the member's specific benefit plan document."""


AMBIGUOUS_QUERY_PROMPT = """Your question could match multiple policies. Here are the most relevant options:

{policy_list}

Please refine your question with:
- Specific procedure codes (CPT/HCPCS)
- Specific condition or diagnosis
- Policy category (medical vs. drug policy)"""
