"""
Módulo para calcular sinergias entre ferramentas de IA
"""

import os
import math
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class SynergyBuilder:
    """Classe para calcular e armazenar sinergias entre ferramentas de IA"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados no .env")
        
        self.supabase: Client = create_client(self.url, self.key)
        print(f"✅ Conectado ao Supabase para cálculo de sinergias")
        
        # Pesos para diferentes fatores de sinergia
        self.weights = {
            'category_overlap': 0.3,      # Sobreposição de categorias
            'domain_compatibility': 0.25, # Compatibilidade de domínios
            'workflow_synergy': 0.2,      # Sinergia de workflow
            'price_compatibility': 0.15,  # Compatibilidade de preço
            'popularity_boost': 0.1       # Boost de popularidade
        }
    
    def calculate_all_synergies(self, batch_size: int = 100) -> Dict[str, int]:
        """
        Calcula sinergias para todas as ferramentas no banco
        
        Args:
            batch_size: Tamanho do lote para processamento
            
        Returns:
            Dict com estatísticas da operação
        """
        stats = {'calculated': 0, 'inserted': 0, 'errors': 0}
        
        print("🔄 Iniciando cálculo de sinergias...")
        
        # Busca todas as ferramentas
        tools = self._get_all_tools()
        if not tools:
            print("⚠️ Nenhuma ferramenta encontrada")
            return stats
        
        print(f"📊 Encontradas {len(tools)} ferramentas para análise")
        
        # Limpa sinergias existentes (opcional)
        self._cleanup_existing_synergies()
        
        # Calcula sinergias em lotes
        total_combinations = len(tools) * (len(tools) - 1) // 2
        processed = 0
        
        for i in range(0, len(tools), batch_size):
            batch = tools[i:i + batch_size]
            batch_stats = self._calculate_batch_synergies(batch, tools)
            
            stats['calculated'] += batch_stats['calculated']
            stats['inserted'] += batch_stats['inserted']
            stats['errors'] += batch_stats['errors']
            
            processed += len(batch)
            progress = (processed / len(tools)) * 100
            print(f"📈 Progresso: {progress:.1f}% ({processed}/{len(tools)} ferramentas)")
        
        print(f"\n🎯 Sinergias calculadas: {stats['calculated']}")
        print(f"💾 Sinergias inseridas: {stats['inserted']}")
        print(f"❌ Erros: {stats['errors']}")
        
        return stats
    
    def _get_all_tools(self) -> List[Dict[str, Any]]:
        """Busca todas as ferramentas do banco"""
        try:
            response = self.supabase.table('ai_tool').select('*').execute()
            return response.data
        except Exception as e:
            print(f"❌ Erro ao buscar ferramentas: {e}")
            return []
    
    def _cleanup_existing_synergies(self) -> None:
        """Remove sinergias existentes para recalcular"""
        try:
            print("🧹 Limpando sinergias existentes...")
            self.supabase.table('ai_synergy').delete().gte('id', 0).execute()
            print("✅ Sinergias limpas")
        except Exception as e:
            print(f"⚠️ Erro na limpeza (continuando): {e}")
    
    def _calculate_batch_synergies(self, batch: List[Dict], all_tools: List[Dict]) -> Dict[str, int]:
        """Calcula sinergias para um lote de ferramentas"""
        stats = {'calculated': 0, 'inserted': 0, 'errors': 0}
        
        for tool1 in batch:
            for tool2 in all_tools:
                if tool1['id'] >= tool2['id']:  # Evita duplicatas e auto-comparação
                    continue
                
                try:
                    synergy_score = self._calculate_synergy_score(tool1, tool2)
                    stats['calculated'] += 1
                    
                    if synergy_score > 0.1:  # Só armazena sinergias significativas
                        self._insert_synergy(tool1['id'], tool2['id'], synergy_score)
                        stats['inserted'] += 1
                        
                except Exception as e:
                    stats['errors'] += 1
                    continue
        
        return stats
    
    def _calculate_synergy_score(self, tool1: Dict, tool2: Dict) -> float:
        """
        Calcula o score de sinergia entre duas ferramentas
        
        Args:
            tool1, tool2: Dicionários com dados das ferramentas
            
        Returns:
            Score de sinergia entre 0 e 1
        """
        scores = {}
        
        # 1. Sobreposição de categorias
        scores['category_overlap'] = self._calculate_category_overlap(
            tool1.get('categories', []), 
            tool2.get('categories', [])
        )
        
        # 2. Compatibilidade de domínios
        scores['domain_compatibility'] = self._calculate_domain_compatibility(
            tool1.get('macro_domain', ''), 
            tool2.get('macro_domain', '')
        )
        
        # 3. Sinergia de workflow
        scores['workflow_synergy'] = self._calculate_workflow_synergy(tool1, tool2)
        
        # 4. Compatibilidade de preço
        scores['price_compatibility'] = self._calculate_price_compatibility(
            tool1.get('price', ''), 
            tool2.get('price', '')
        )
        
        # 5. Boost de popularidade
        scores['popularity_boost'] = self._calculate_popularity_boost(
            tool1.get('popularity', 0), 
            tool2.get('popularity', 0)
        )
        
        # Calcula score final ponderado
        final_score = sum(
            scores[factor] * self.weights[factor] 
            for factor in scores
        )
        
        # Aplica função sigmoide para suavizar
        return self._sigmoid(final_score)
    
    def _calculate_category_overlap(self, categories1: List[str], categories2: List[str]) -> float:
        """Calcula sobreposição de categorias"""
        if not categories1 or not categories2:
            return 0.0
        
        set1 = set(cat.lower() for cat in categories1)
        set2 = set(cat.lower() for cat in categories2)
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _calculate_domain_compatibility(self, domain1: str, domain2: str) -> float:
        """Calcula compatibilidade entre domínios"""
        if not domain1 or not domain2:
            return 0.0
        
        # Matriz de compatibilidade entre domínios
        compatibility_matrix = {
            'NLP': {
                'NLP': 1.0, 'GENERATIVE_AI': 0.8, 'CHATBOT': 0.9, 
                'AUTOMATION': 0.6, 'BUSINESS': 0.5, 'CODING': 0.4
            },
            'COMPUTER_VISION': {
                'COMPUTER_VISION': 1.0, 'GENERATIVE_AI': 0.7, 'DESIGN': 0.6,
                'VIDEO': 0.8, 'AUTOMATION': 0.5
            },
            'GENERATIVE_AI': {
                'GENERATIVE_AI': 1.0, 'NLP': 0.8, 'COMPUTER_VISION': 0.7,
                'DESIGN': 0.6, 'CODING': 0.5, 'BUSINESS': 0.4
            },
            'AUTOMATION': {
                'AUTOMATION': 1.0, 'BUSINESS': 0.8, 'CODING': 0.7,
                'DATA_ANALYSIS': 0.6, 'NLP': 0.6
            },
            'BUSINESS': {
                'BUSINESS': 1.0, 'AUTOMATION': 0.8, 'DATA_ANALYSIS': 0.7,
                'NLP': 0.5, 'GENERATIVE_AI': 0.4
            },
            'CODING': {
                'CODING': 1.0, 'AUTOMATION': 0.7, 'ML_FRAMEWORKS': 0.8,
                'DATA_ANALYSIS': 0.6, 'NLP': 0.4
            },
            'DATA_ANALYSIS': {
                'DATA_ANALYSIS': 1.0, 'BUSINESS': 0.7, 'ML_FRAMEWORKS': 0.8,
                'AUTOMATION': 0.6, 'CODING': 0.6
            },
            'DESIGN': {
                'DESIGN': 1.0, 'COMPUTER_VISION': 0.6, 'GENERATIVE_AI': 0.6,
                'VIDEO': 0.5
            }
        }
        
        # Busca compatibilidade na matriz
        if domain1 in compatibility_matrix:
            return compatibility_matrix[domain1].get(domain2, 0.2)
        elif domain2 in compatibility_matrix:
            return compatibility_matrix[domain2].get(domain1, 0.2)
        
        # Se são iguais mas não estão na matriz
        return 1.0 if domain1 == domain2 else 0.2
    
    def _calculate_workflow_synergy(self, tool1: Dict, tool2: Dict) -> float:
        """Calcula sinergia de workflow baseado em descrições"""
        desc1 = tool1.get('description', '').lower()
        desc2 = tool2.get('description', '').lower()
        
        if not desc1 or not desc2:
            return 0.0
        
        # Palavras-chave que indicam workflows complementares
        workflow_keywords = {
            'input_output': {
                'generates': ['creates', 'writes', 'analyzes', 'processes'],
                'consumes': ['edits', 'reviews', 'improves', 'optimizes']
            },
            'process_stages': {
                'early': ['brainstorm', 'ideate', 'plan', 'draft'],
                'middle': ['develop', 'create', 'build', 'generate'],
                'late': ['review', 'edit', 'polish', 'optimize']
            }
        }
        
        synergy_score = 0.0
        
        # Verifica complementaridade input/output
        generates_in_1 = any(keyword in desc1 for keyword in workflow_keywords['input_output']['generates'])
        consumes_in_2 = any(keyword in desc2 for keyword in workflow_keywords['input_output']['consumes'])
        
        if generates_in_1 and consumes_in_2:
            synergy_score += 0.5
        
        # Verifica estágios sequenciais do processo
        for stage, keywords in workflow_keywords['process_stages'].items():
            if any(keyword in desc1 for keyword in keywords):
                for other_stage, other_keywords in workflow_keywords['process_stages'].items():
                    if stage != other_stage and any(keyword in desc2 for keyword in other_keywords):
                        synergy_score += 0.3
        
        return min(synergy_score, 1.0)
    
    def _calculate_price_compatibility(self, price1: str, price2: str) -> float:
        """Calcula compatibilidade de preços"""
        if not price1 or not price2:
            return 0.5
        
        # Normaliza preços
        price1 = price1.lower().strip()
        price2 = price2.lower().strip()
        
        # Matriz de compatibilidade de preços
        compatibility = {
            'free': {'free': 1.0, 'freemium': 0.8, 'paid': 0.6, 'unknown': 0.5},
            'freemium': {'free': 0.8, 'freemium': 1.0, 'paid': 0.9, 'unknown': 0.7},
            'paid': {'free': 0.6, 'freemium': 0.9, 'paid': 1.0, 'unknown': 0.7},
            'unknown': {'free': 0.5, 'freemium': 0.7, 'paid': 0.7, 'unknown': 0.5}
        }
        
        return compatibility.get(price1, {}).get(price2, 0.5)
    
    def _calculate_popularity_boost(self, pop1: float, pop2: float) -> float:
        """Calcula boost baseado na popularidade das ferramentas"""
        if pop1 <= 0 or pop2 <= 0:
            return 0.0
        
        # Ferramentas mais populares têm potencial de sinergia maior
        avg_popularity = (pop1 + pop2) / 2
        normalized_pop = min(avg_popularity / 100, 1.0)
        
        return math.sqrt(normalized_pop)
    
    def _sigmoid(self, x: float) -> float:
        """Função sigmoide para suavizar scores"""
        return 1 / (1 + math.exp(-10 * (x - 0.5)))
    
    def _insert_synergy(self, tool1_id: int, tool2_id: int, synergy_score: float) -> None:
        """Insere sinergia no banco"""
        synergy_data = {
            'tool1_id': tool1_id,
            'tool2_id': tool2_id,
            'synergy_score': round(synergy_score, 4)
        }
        
        self.supabase.table('ai_synergy').insert(synergy_data).execute()
    
    def get_tool_synergies(self, tool_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca sinergias de uma ferramenta específica
        
        Args:
            tool_id: ID da ferramenta
            limit: Número máximo de sinergias a retornar
            
        Returns:
            Lista de sinergias ordenadas por score
        """
        try:
            # Busca sinergias onde a ferramenta aparece como tool1 ou tool2
            response1 = self.supabase.table('ai_synergy').select(
                'synergy_score, tool2_id, ai_tool!ai_synergy_tool2_id_fkey(name, description)'
            ).eq('tool1_id', tool_id).order('synergy_score', desc=True).limit(limit).execute()
            
            response2 = self.supabase.table('ai_synergy').select(
                'synergy_score, tool1_id, ai_tool!ai_synergy_tool1_id_fkey(name, description)'
            ).eq('tool2_id', tool_id).order('synergy_score', desc=True).limit(limit).execute()
            
            synergies = []
            
            # Processa resultados onde a ferramenta é tool1
            for item in response1.data:
                synergies.append({
                    'synergy_score': item['synergy_score'],
                    'related_tool_id': item['tool2_id'],
                    'related_tool': item['ai_tool']
                })
            
            # Processa resultados onde a ferramenta é tool2
            for item in response2.data:
                synergies.append({
                    'synergy_score': item['synergy_score'],
                    'related_tool_id': item['tool1_id'],
                    'related_tool': item['ai_tool']
                })
            
            # Ordena por score e retorna top N
            synergies.sort(key=lambda x: x['synergy_score'], reverse=True)
            return synergies[:limit]
            
        except Exception as e:
            print(f"❌ Erro ao buscar sinergias da ferramenta {tool_id}: {e}")
            return []
    
    def get_synergy_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas das sinergias"""
        try:
            # Total de sinergias
            total_response = self.supabase.table('ai_synergy').select('id', count='exact').execute()
            total_synergies = total_response.count
            
            # Estatísticas de scores
            scores_response = self.supabase.table('ai_synergy').select('synergy_score').execute()
            scores = [item['synergy_score'] for item in scores_response.data]
            
            if scores:
                avg_score = sum(scores) / len(scores)
                max_score = max(scores)
                min_score = min(scores)
                
                # Distribuição por faixas
                high_synergy = len([s for s in scores if s >= 0.7])
                medium_synergy = len([s for s in scores if 0.4 <= s < 0.7])
                low_synergy = len([s for s in scores if s < 0.4])
            else:
                avg_score = max_score = min_score = 0
                high_synergy = medium_synergy = low_synergy = 0
            
            return {
                'total_synergies': total_synergies,
                'avg_score': round(avg_score, 4),
                'max_score': round(max_score, 4),
                'min_score': round(min_score, 4),
                'distribution': {
                    'high_synergy': high_synergy,    # >= 0.7
                    'medium_synergy': medium_synergy, # 0.4 - 0.7
                    'low_synergy': low_synergy       # < 0.4
                }
            }
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas de sinergias: {e}")
            return {}


def build_synergies() -> Dict[str, int]:
    """
    Função de conveniência para calcular todas as sinergias
    
    Returns:
        Dict com estatísticas da operação
    """
    builder = SynergyBuilder()
    return builder.calculate_all_synergies()


def get_synergy_stats() -> Dict[str, Any]:
    """
    Função de conveniência para obter estatísticas de sinergias
    
    Returns:
        Dict com estatísticas das sinergias
    """
    builder = SynergyBuilder()
    return builder.get_synergy_statistics()


def get_tool_synergies(tool_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Função de conveniência para buscar sinergias de uma ferramenta
    
    Args:
        tool_id: ID da ferramenta
        limit: Número máximo de sinergias
        
    Returns:
        Lista de sinergias da ferramenta
    """
    builder = SynergyBuilder()
    return builder.get_tool_synergies(tool_id, limit)