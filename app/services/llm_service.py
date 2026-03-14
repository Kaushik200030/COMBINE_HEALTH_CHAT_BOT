"""LLM service using free models (Ollama or Hugging Face)."""
from typing import List, Dict
import requests
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class OllamaLLM:
    """LLM service using Ollama (free, local)."""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self._check_ollama()
    
    def _check_ollama(self):
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info(f"Ollama connected. Using model: {self.model}")
            else:
                logger.warning(f"Ollama not responding. Status: {response.status_code}")
        except Exception as e:
            logger.warning(f"Could not connect to Ollama: {e}")
            logger.warning("Make sure Ollama is installed and running: https://ollama.ai")
    
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.1, max_tokens: int = 1000) -> str:
        """Generate response using Ollama."""
        try:
            # Convert messages to Ollama format
            prompt = self._format_messages(messages)
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=180  # Increased timeout for large models
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama: {e}")
            raise Exception(f"Ollama API error: {str(e)}")
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Format messages for Ollama prompt."""
        formatted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                formatted.append(f"System: {content}")
            elif role == "user":
                formatted.append(f"User: {content}")
            elif role == "assistant":
                formatted.append(f"Assistant: {content}")
        
        return "\n\n".join(formatted) + "\n\nAssistant:"


class HuggingFaceLLM:
    """LLM service using Hugging Face transformers (free, local)."""
    
    def __init__(self):
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
        except ImportError:
            raise ImportError("transformers and torch are required for Hugging Face LLM. Install with: pip install transformers torch")
        
        self.model_name = settings.hf_model
        self.device = settings.hf_device
        self.torch = torch
        logger.info(f"Loading Hugging Face model: {self.model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            if self.device == "cpu":
                self.model = self.model.to("cpu")
            logger.info("Hugging Face model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Hugging Face model: {e}")
            raise
    
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.1, max_tokens: int = 1000) -> str:
        """Generate response using Hugging Face model."""
        try:
            # Format messages
            prompt = self._format_messages(messages)
            
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            if self.device == "cuda":
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            # Generate
            with self.torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature if temperature > 0 else 1.0,
                    do_sample=temperature > 0,
                    pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id
                )
            
            # Decode
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the new generated text
            response = response[len(prompt):].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating with Hugging Face: {e}")
            raise
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Format messages for model prompt."""
        formatted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                formatted.append(f"System: {content}")
            elif role == "user":
                formatted.append(f"User: {content}")
            elif role == "assistant":
                formatted.append(f"Assistant: {content}")
        
        return "\n\n".join(formatted) + "\n\nAssistant:"


class LLMService:
    """Unified LLM service that supports multiple free providers."""
    
    def __init__(self):
        provider = settings.llm_provider.lower()
        
        if provider == "ollama":
            try:
                self.llm = OllamaLLM()
                logger.info("Using Ollama for LLM")
            except Exception as e:
                logger.warning(f"Failed to initialize Ollama: {e}")
                logger.info("Falling back to simple template-based responses")
                self.llm = None
        elif provider == "huggingface":
            try:
                self.llm = HuggingFaceLLM()
                logger.info("Using Hugging Face for LLM")
            except Exception as e:
                logger.warning(f"Failed to initialize Hugging Face: {e}")
                logger.info("Falling back to simple template-based responses")
                self.llm = None
        else:
            logger.warning(f"Unknown LLM provider: {provider}. Using template-based responses")
            self.llm = None
    
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.1, max_tokens: int = 1000) -> str:
        """Generate response using configured LLM."""
        if self.llm:
            return self.llm.generate(messages, temperature, max_tokens)
        else:
            # Fallback to simple template-based response
            return self._template_response(messages)
    
    def _template_response(self, messages: List[Dict[str, str]]) -> str:
        """Simple template-based response when LLM is not available."""
        user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        if not user_message:
            return "I'm sorry, I couldn't understand your question."
        
        # Extract context from system message
        context = ""
        for msg in messages:
            if msg.get("role") == "system":
                context = msg.get("content", "")
                break
        
        # Simple response template
        return f"""Based on the provided policy documents, here is information relevant to your question: "{user_message}"

Please review the source documents listed below for detailed information. The policy documents contain the specific coverage criteria, documentation requirements, and applicable procedure codes.

Note: This is a template response. For full functionality, please set up Ollama (recommended) or Hugging Face models. See README for setup instructions."""
