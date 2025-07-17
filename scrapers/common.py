import requests
import time
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

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
    # New enhanced fields
    url: Optional[str] = None
    logo_url: Optional[str] = None
    rank: Optional[int] = None
    upvotes: Optional[int] = None
    monthly_users: Optional[int] = None
    editor_score: Optional[float] = None
    maturity: Optional[str] = None
    platform: Optional[List[str]] = None
    features: Optional[Dict[str, Any]] = None
    last_scraped: Optional[datetime] = None

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
    
    def extract_logo_url(self, element, tool_url: str = "") -> Optional[str]:
        """Extrai URL do logo da ferramenta"""
        # Busca por imagens no elemento
        img_selectors = ['img', 'img[alt*="logo"]', '[class*="logo"] img', '[class*="icon"] img']
        
        for selector in img_selectors:
            img = element.select_one(selector)
            if img:
                src = img.get('src') or img.get('data-src') or img.get('data-lazy')
                if src:
                    # Torna URL absoluta se necessário
                    if src.startswith('/'):
                        return self.base_url + src
                    elif src.startswith('http'):
                        return src
                    elif tool_url:
                        # Tenta construir URL baseada na URL da ferramenta
                        from urllib.parse import urljoin
                        return urljoin(tool_url, src)
        
        return None
    
    def extract_platform_info(self, element, text: str = "") -> List[str]:
        """Extrai informações de plataforma"""
        platforms = []
        combined_text = (element.get_text() if hasattr(element, 'get_text') else str(element)) + " " + text
        combined_text = combined_text.lower()
        
        platform_keywords = {
            'web': ['web', 'browser', 'online', 'website'],
            'ios': ['ios', 'iphone', 'ipad', 'app store'],
            'android': ['android', 'google play', 'play store'],
            'mac': ['mac', 'macos', 'apple'],
            'windows': ['windows', 'pc', 'microsoft'],
            'linux': ['linux', 'ubuntu'],
            'api': ['api', 'integration', 'webhook'],
            'chrome': ['chrome extension', 'chrome', 'browser extension'],
            'slack': ['slack', 'slack bot'],
            'discord': ['discord', 'discord bot']
        }
        
        for platform, keywords in platform_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                platforms.append(platform)
        
        return platforms if platforms else ['web']  # Default to web
    
    def extract_numeric_value(self, text: str, patterns: List[str]) -> Optional[int]:
        """Extrai valores numéricos usando regex patterns"""
        import re
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    # Remove vírgulas e converte
                    value_str = match.group(1).replace(',', '').replace('.', '')
                    return int(value_str)
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def extract_features(self, element, description: str = "") -> Dict[str, Any]:
        """Extrai features/características da ferramenta"""
        features = {}
        
        # Busca por badges/tags que indicam features
        feature_selectors = ['.tag', '.badge', '.feature', '[class*="tag"]', '[class*="badge"]']
        
        feature_tags = []
        for selector in feature_selectors:
            tags = element.select(selector)
            for tag in tags:
                tag_text = tag.get_text().strip()
                if tag_text and len(tag_text) < 30:  # Evita textos muito longos
                    feature_tags.append(tag_text)
        
        if feature_tags:
            features['tags'] = feature_tags
        
        # Extrai características do texto/descrição
        text_content = (element.get_text() if hasattr(element, 'get_text') else str(element)) + " " + description
        text_lower = text_content.lower()
        
        # Features comuns de ferramentas AI
        feature_checks = {
            'free_tier': any(term in text_lower for term in ['free', 'free tier', 'freemium']),
            'api_available': any(term in text_lower for term in ['api', 'integration', 'webhook']),
            'no_code': any(term in text_lower for term in ['no code', 'no-code', 'drag and drop']),
            'open_source': any(term in text_lower for term in ['open source', 'github', 'open-source']),
            'enterprise': any(term in text_lower for term in ['enterprise', 'business', 'team']),
            'real_time': any(term in text_lower for term in ['real time', 'real-time', 'live']),
            'mobile_app': any(term in text_lower for term in ['mobile app', 'ios', 'android']),
            'collaboration': any(term in text_lower for term in ['collaboration', 'team', 'share'])
        }
        
        # Adiciona apenas features que são True
        for feature, is_present in feature_checks.items():
            if is_present:
                features[feature] = True
        
        return features if features else None