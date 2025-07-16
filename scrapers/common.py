import requests
import time
import random
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class AITool:
    ext_id: str
    name: str
    description: str
    price: str
    popularity: float
    categories: List[str]
    source: str
    macro_domain: str = "OTHER"

class BaseScraper:
    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_page(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """Faz requisição HTTP com retry e rate limiting"""
        for attempt in range(max_retries):
            try:
                time.sleep(random.uniform(1, 3))
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"Erro na tentativa {attempt + 1} para {url}: {e}")
                if attempt == max_retries - 1:
                    return None
                time.sleep(random.uniform(2, 5))
        return None
    
    def classify_domain(self, categories: List[str], description: str = "") -> str:
        """Classifica ferramenta em macro-domínio baseado em categorias e descrição"""
        text = " ".join(categories + [description]).lower()
        
        domain_keywords = {
            'NLP': ['nlp', 'text', 'language', 'chatbot', 'translation', 'sentiment', 'speech', 'voice', 'conversation'],
            'COMPUTER_VISION': ['vision', 'image', 'photo', 'visual', 'detection', 'recognition', 'opencv', 'face'],
            'AUDIO': ['audio', 'music', 'sound', 'voice', 'podcast', 'speech', 'acoustic', 'sound'],
            'VIDEO': ['video', 'film', 'movie', 'streaming', 'animation', 'editing', 'youtube'],
            'GENERATIVE_AI': ['generative', 'generate', 'gpt', 'dall-e', 'midjourney', 'stable diffusion', 'ai art', 'content generation'],
            'ML_FRAMEWORKS': ['tensorflow', 'pytorch', 'keras', 'framework', 'model', 'training', 'machine learning', 'neural network'],
            'DATA_ANALYSIS': ['data', 'analytics', 'visualization', 'dashboard', 'report', 'bi', 'database', 'sql', 'chart'],
            'AUTOMATION': ['automation', 'workflow', 'zapier', 'integration', 'api', 'webhook', 'bot', 'process'],
            'DESIGN': ['design', 'ui', 'ux', 'graphic', 'creative', 'adobe', 'figma', 'prototype'],
            'CODING': ['code', 'programming', 'development', 'github', 'ide', 'developer', 'software'],
            'BUSINESS': ['business', 'crm', 'sales', 'marketing', 'finance', 'productivity', 'management', 'enterprise']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in text for keyword in keywords):
                return domain
        
        return 'OTHER'