import os
from openai import OpenAI

class TokenFactoryNemotronClient:
    def __init__(self, api_key=None, base_url=None):
        # Default to Token Factory endpoint if not provided
        self.api_key = api_key or os.getenv("TOKEN_FACTORY_API_KEY", "tf-default-key")
        self.base_url = base_url or os.getenv("TOKEN_FACTORY_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
        
        # Initialize primary client
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        # Fallback local Ollama client
        self.fallback_client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")

    def chat_completion(self, messages, tier="super", temperature=0.2, max_tokens=250, stream=False):
        """
        Routes chat completion through Token Factory Nemotron models based on tier.
        Tiers: 
          - 'nano': Fast parsing & structured extraction (Nemotron-3-Nano)
          - 'super' / 'ultra': Deep clinical reasoning & synthesis (Nemotron-3-Super / Ultra)
        """
        model_mapping = {
            "nano": "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
            "super": "nvidia/nemotron-3-super-120b-a12b",
            "ultra": "nvidia/Nemotron-3-Ultra-550b-a55b"
        }
        model_name = model_mapping.get(tier, model_mapping["super"])

        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            return response
        except Exception as e:
            # Fallback to local Ollama if Token Factory API fails or network is offline
            print(f"[Warning] Token Factory Nemotron ({tier}) failed: {str(e)}. Falling back to local Ollama (llama3.1)...")
            fallback_res = self.fallback_client.chat.completions.create(
                model="llama3.1",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            return fallback_res