"""Test script to verify Hugging Face LLM works before deploying."""
import os
os.environ["LLM_PROVIDER"] = "huggingface"
os.environ["HF_MODEL"] = "microsoft/Phi-3-mini-4k-instruct"
os.environ["HF_DEVICE"] = "cpu"

from app.services.llm_service import LLMService

print("Testing Hugging Face LLM...")
print("This will download the model on first run (~2GB, takes 5-10 minutes)")
print("=" * 60)

try:
    llm = LLMService()
    print("✅ LLM Service initialized!")
    
    # Test generation
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello in one sentence."}
    ]
    
    print("\nGenerating test response...")
    response = llm.generate(messages, temperature=0.1, max_tokens=50)
    print(f"\n✅ Response: {response}")
    print("\n🎉 Hugging Face is working! Ready for cloud deployment.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure transformers is installed: pip install transformers torch")
    print("2. Check your internet connection (model needs to download)")
    print("3. Try a smaller model: export HF_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0")
