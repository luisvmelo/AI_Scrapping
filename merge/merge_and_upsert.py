"""
Módulo para fazer merge e upsert das ferramentas de AI no Supabase
"""

import os
import hashlib
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
from scrapers.common import AITool
from datetime import datetime

# Carrega variáveis de ambiente
load_dotenv()

class SupabaseMerger:
    """Classe para fazer merge e upsert das ferramentas no Supabase"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados no .env")
        
        self.supabase: Client = create_client(self.url, self.key)
        print(f"✅ Conectado ao Supabase: {self.url}")
    
    def merge_and_upsert_tools(self, tools: List[AITool]) -> Dict[str, int]:
        """
        Faz merge e upsert das ferramentas no Supabase com deduplicação avançada
        
        Args:
            tools: Lista de ferramentas para inserir/atualizar
            
        Returns:
            Dict com estatísticas: {'inserted': n, 'updated': n, 'errors': n, 'merged': n}
        """
        stats = {'inserted': 0, 'updated': 0, 'errors': 0, 'merged': 0}
        
        if not tools:
            print("⚠️ Nenhuma ferramenta para processar")
            return stats
        
        print(f"🔄 Processando {len(tools)} ferramentas com deduplicação avançada...")
        
        # Primeiro, deduplica dentro do batch de entrada
        deduplicated_tools = self._deduplicate_tools_batch(tools)
        print(f"🧹 Deduplicação interna: {len(tools)} -> {len(deduplicated_tools)} ferramentas")
        
        for i, tool in enumerate(deduplicated_tools):
            try:
                # Atualiza timestamp de scraping
                tool.last_scraped = datetime.now()
                
                # Gera hash único para detectar mudanças
                content_hash = self._generate_content_hash(tool)
                
                # Busca por ferramentas duplicadas no banco (por URL ou nome)
                existing_tool = self._find_duplicate_tool(tool)
                
                if existing_tool:
                    # Faz merge inteligente dos dados
                    merged_tool = self._merge_tool_data(existing_tool, tool)
                    
                    # Verifica se houve mudanças após o merge
                    merged_hash = self._generate_content_hash(merged_tool)
                    if existing_tool.get('content_hash') != merged_hash:
                        # Atualiza ferramenta existente com dados merged
                        self._update_tool(existing_tool['id'], merged_tool, merged_hash)
                        stats['updated'] += 1
                        print(f"🔄 [{i+1}/{len(deduplicated_tools)}] Atualizado (merged): {tool.name}")
                    else:
                        # Mesmo sem mudanças no conteúdo, atualiza last_scraped
                        self._update_last_scraped(existing_tool['id'])
                        stats['merged'] += 1
                        print(f"⏭️ [{i+1}/{len(deduplicated_tools)}] Sem mudanças (timestamp atualizado): {tool.name}")
                else:
                    # Insere nova ferramenta
                    self._insert_tool(tool, content_hash)
                    stats['inserted'] += 1
                    print(f"✅ [{i+1}/{len(deduplicated_tools)}] Inserido: {tool.name}")
                
            except Exception as e:
                stats['errors'] += 1
                print(f"❌ [{i+1}/{len(deduplicated_tools)}] Erro ao processar {tool.name}: {e}")
                continue
        
        print(f"\n📊 Resultados: {stats['inserted']} inseridas, {stats['updated']} atualizadas, {stats['merged']} merged, {stats['errors']} erros")
        return stats
    
    def _get_existing_tool(self, ext_id: str, source: str) -> Optional[Dict[str, Any]]:
        """Busca ferramenta existente por ext_id e source"""
        try:
            response = self.supabase.table('ai_tool').select('*').eq('ext_id', ext_id).eq('source', source).execute()
            
            if response.data:
                return response.data[0]
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar ferramenta existente {ext_id}: {e}")
            return None
    
    def _insert_tool(self, tool: AITool, content_hash: str) -> None:
        """Insere nova ferramenta"""
        tool_data = {
            'ext_id': tool.ext_id,
            'name': tool.name,
            'description': tool.description,
            'price': tool.price,
            'popularity': tool.popularity,
            'categories': tool.categories,
            'source': tool.source,
            'macro_domain': tool.macro_domain,
            'content_hash': content_hash,
            # Enhanced fields
            'url': tool.url,
            'logo_url': tool.logo_url,
            'rank': tool.rank,
            'upvotes': tool.upvotes,
            'monthly_users': tool.monthly_users,
            'editor_score': tool.editor_score,
            'maturity': tool.maturity,
            'platform': tool.platform,
            'features': tool.features,
            'last_scraped': tool.last_scraped.isoformat() if tool.last_scraped else None
        }
        
        response = self.supabase.table('ai_tool').insert(tool_data).execute()
        
        if not response.data:
            raise Exception("Falha ao inserir ferramenta")
    
    def _update_tool(self, tool_id: int, tool: AITool, content_hash: str) -> None:
        """Atualiza ferramenta existente"""
        tool_data = {
            'name': tool.name,
            'description': tool.description,
            'price': tool.price,
            'popularity': tool.popularity,
            'categories': tool.categories,
            'macro_domain': tool.macro_domain,
            'content_hash': content_hash,
            'updated_at': 'now()',
            # Enhanced fields
            'url': tool.url,
            'logo_url': tool.logo_url,
            'rank': tool.rank,
            'upvotes': tool.upvotes,
            'monthly_users': tool.monthly_users,
            'editor_score': tool.editor_score,
            'maturity': tool.maturity,
            'platform': tool.platform,
            'features': tool.features,
            'last_scraped': tool.last_scraped.isoformat() if tool.last_scraped else None
        }
        
        response = self.supabase.table('ai_tool').update(tool_data).eq('id', tool_id).execute()
        
        if not response.data:
            raise Exception("Falha ao atualizar ferramenta")
    
    def _generate_content_hash(self, tool: AITool) -> str:
        """Gera hash do conteúdo da ferramenta para detectar mudanças"""
        # Include all significant fields in hash calculation
        content_parts = [
            tool.name or "",
            tool.description or "",
            tool.price or "",
            str(tool.popularity),
            '|'.join(sorted(tool.categories)),
            tool.url or "",
            tool.logo_url or "",
            str(tool.rank) if tool.rank else "",
            str(tool.upvotes) if tool.upvotes else "",
            str(tool.monthly_users) if tool.monthly_users else "",
            str(tool.editor_score) if tool.editor_score else "",
            tool.maturity or "",
            '|'.join(sorted(tool.platform)) if tool.platform else "",
            str(tool.features) if tool.features else ""
        ]
        content = "|".join(content_parts)
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _deduplicate_tools_batch(self, tools: List[AITool]) -> List[AITool]:
        """Deduplica ferramentas dentro do batch por URL ou nome"""
        seen_tools = {}
        deduplicated = []
        
        for tool in tools:
            # Chaves de deduplicação
            url_key = tool.url.lower().strip() if tool.url else None
            name_key = tool.name.lower().strip() if tool.name else None
            
            # Procura por duplicatas
            duplicate_key = None
            if url_key and url_key in seen_tools:
                duplicate_key = url_key
            elif name_key and name_key in seen_tools:
                duplicate_key = name_key
            
            if duplicate_key:
                # Faz merge com o duplicado existente
                existing_tool = seen_tools[duplicate_key]
                merged_tool = self._merge_tool_objects(existing_tool, tool)
                seen_tools[duplicate_key] = merged_tool
                
                # Atualiza na lista deduplicated
                for i, existing in enumerate(deduplicated):
                    if existing == existing_tool:
                        deduplicated[i] = merged_tool
                        break
            else:
                # Adiciona nova ferramenta
                if url_key:
                    seen_tools[url_key] = tool
                if name_key:
                    seen_tools[name_key] = tool
                deduplicated.append(tool)
        
        return deduplicated
    
    def _find_duplicate_tool(self, tool: AITool) -> Optional[Dict[str, Any]]:
        """Busca por ferramenta duplicada no banco por URL ou nome"""
        try:
            # Busca por URL primeiro (mais específico)
            if tool.url:
                url_clean = tool.url.lower().strip()
                response = self.supabase.table('ai_tool').select('*').ilike('url', url_clean).execute()
                if response.data:
                    return response.data[0]
            
            # Busca por nome se não achou por URL
            if tool.name:
                name_clean = tool.name.lower().strip()
                response = self.supabase.table('ai_tool').select('*').ilike('name', name_clean).execute()
                if response.data:
                    return response.data[0]
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar ferramenta duplicada: {e}")
            return None
    
    def _merge_tool_data(self, existing_dict: Dict[str, Any], new_tool: AITool) -> AITool:
        """Faz merge inteligente dos dados da ferramenta"""
        # Converte dict existente para AITool
        existing_tool = self._dict_to_aitool(existing_dict)
        
        # Faz merge
        return self._merge_tool_objects(existing_tool, new_tool)
    
    def _merge_tool_objects(self, existing: AITool, new: AITool) -> AITool:
        """Faz merge entre dois objetos AITool"""
        # Escolhe a descrição mais longa
        description = new.description if (new.description and len(new.description) > len(existing.description or "")) else existing.description
        
        # Para valores numéricos, mantém o maior (exceto rank, onde menor é melhor)
        popularity = max(existing.popularity, new.popularity)
        rank = self._min_optional(existing.rank, new.rank)  # Menor rank é melhor
        upvotes = self._max_optional(existing.upvotes, new.upvotes)
        monthly_users = self._max_optional(existing.monthly_users, new.monthly_users)
        editor_score = self._max_optional(existing.editor_score, new.editor_score)
        
        # Combina listas (platform, categories)
        categories = list(set((existing.categories or []) + (new.categories or [])))
        platform = list(set((existing.platform or []) + (new.platform or [])))
        
        # Combina features
        features = {}
        if existing.features:
            features.update(existing.features)
        if new.features:
            features.update(new.features)
        
        # Prefere dados mais recentes para outros campos
        return AITool(
            ext_id=existing.ext_id,  # Mantém o ID original
            name=new.name or existing.name,
            description=description,
            price=new.price or existing.price,
            popularity=popularity,
            categories=categories,
            source=existing.source,  # Mantém source original
            macro_domain=new.macro_domain or existing.macro_domain,
            url=new.url or existing.url,
            logo_url=new.logo_url or existing.logo_url,
            rank=rank,
            upvotes=upvotes,
            monthly_users=monthly_users,
            editor_score=editor_score,
            maturity=new.maturity or existing.maturity,
            platform=platform,
            features=features if features else None,
            last_scraped=new.last_scraped or existing.last_scraped
        )
    
    def _dict_to_aitool(self, data: Dict[str, Any]) -> AITool:
        """Converte dict do Supabase para AITool"""
        return AITool(
            ext_id=data.get('ext_id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            price=data.get('price', ''),
            popularity=data.get('popularity', 0),
            categories=data.get('categories', []),
            source=data.get('source', ''),
            macro_domain=data.get('macro_domain', 'OTHER'),
            url=data.get('url'),
            logo_url=data.get('logo_url'),
            rank=data.get('rank'),
            upvotes=data.get('upvotes'),
            monthly_users=data.get('monthly_users'),
            editor_score=data.get('editor_score'),
            maturity=data.get('maturity'),
            platform=data.get('platform', []),
            features=data.get('features'),
            last_scraped=datetime.fromisoformat(data.get('last_scraped')) if data.get('last_scraped') else None
        )
    
    def _max_optional(self, val1: Optional[int], val2: Optional[int]) -> Optional[int]:
        """Retorna o maior valor entre dois opcionais"""
        if val1 is None and val2 is None:
            return None
        if val1 is None:
            return val2
        if val2 is None:
            return val1
        return max(val1, val2)
    
    def _min_optional(self, val1: Optional[int], val2: Optional[int]) -> Optional[int]:
        """Retorna o menor valor entre dois opcionais"""
        if val1 is None and val2 is None:
            return None
        if val1 is None:
            return val2
        if val2 is None:
            return val1
        return min(val1, val2)
    
    def _update_last_scraped(self, tool_id: int) -> None:
        """Atualiza apenas o timestamp de last_scraped"""
        try:
            self.supabase.table('ai_tool').update({
                'last_scraped': datetime.now().isoformat(),
                'updated_at': 'now()'
            }).eq('id', tool_id).execute()
        except Exception as e:
            print(f"❌ Erro ao atualizar timestamp: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do banco de dados"""
        try:
            # Total de ferramentas
            total_response = self.supabase.table('ai_tool').select('id', count='exact').execute()
            total_tools = total_response.count
            
            # Por fonte
            by_source_response = self.supabase.table('ai_tool').select('source', count='exact').execute()
            by_source = {}
            for item in by_source_response.data:
                source = item['source']
                by_source[source] = by_source.get(source, 0) + 1
            
            # Por macro domínio
            by_domain_response = self.supabase.table('ai_tool').select('macro_domain', count='exact').execute()
            by_domain = {}
            for item in by_domain_response.data:
                domain = item['macro_domain']
                by_domain[domain] = by_domain.get(domain, 0) + 1
            
            return {
                'total_tools': total_tools,
                'by_source': by_source,
                'by_domain': by_domain
            }
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {e}")
            return {}
    
    def cleanup_duplicates(self) -> int:
        """Remove ferramentas duplicadas baseado em ext_id e source"""
        try:
            print("🧹 Iniciando limpeza de duplicatas...")
            
            # Busca duplicatas
            response = self.supabase.table('ai_tool').select('ext_id, source, id').execute()
            
            tools_map = {}
            duplicates_to_remove = []
            
            for tool in response.data:
                key = f"{tool['ext_id']}_{tool['source']}"
                if key in tools_map:
                    # É uma duplicata - mantém o mais antigo (ID menor)
                    if tool['id'] > tools_map[key]['id']:
                        duplicates_to_remove.append(tool['id'])
                    else:
                        duplicates_to_remove.append(tools_map[key]['id'])
                        tools_map[key] = tool
                else:
                    tools_map[key] = tool
            
            # Remove duplicatas
            removed_count = 0
            for duplicate_id in duplicates_to_remove:
                try:
                    self.supabase.table('ai_tool').delete().eq('id', duplicate_id).execute()
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Erro ao remover duplicata ID {duplicate_id}: {e}")
            
            print(f"✅ Removidas {removed_count} duplicatas")
            return removed_count
            
        except Exception as e:
            print(f"❌ Erro na limpeza de duplicatas: {e}")
            return 0
    
    def validate_no_duplicates(self) -> Dict[str, Any]:
        """Valida que não existem duplicatas no banco por URL ou nome"""
        try:
            print("🔍 Validando duplicatas no banco de dados...")
            
            # Busca todas as ferramentas
            response = self.supabase.table('ai_tool').select('id, name, url').execute()
            tools = response.data
            
            # Verifica duplicatas por URL
            url_duplicates = {}
            url_conflicts = []
            
            for tool in tools:
                if tool.get('url'):
                    url_clean = tool['url'].lower().strip()
                    if url_clean in url_duplicates:
                        url_conflicts.append({
                            'url': url_clean,
                            'tools': [url_duplicates[url_clean], tool]
                        })
                    else:
                        url_duplicates[url_clean] = tool
            
            # Verifica duplicatas por nome
            name_duplicates = {}
            name_conflicts = []
            
            for tool in tools:
                if tool.get('name'):
                    name_clean = tool['name'].lower().strip()
                    if name_clean in name_duplicates:
                        name_conflicts.append({
                            'name': name_clean,
                            'tools': [name_duplicates[name_clean], tool]
                        })
                    else:
                        name_duplicates[name_clean] = tool
            
            validation_result = {
                'total_tools': len(tools),
                'url_duplicates': len(url_conflicts),
                'name_duplicates': len(name_conflicts),
                'url_conflicts': url_conflicts[:10],  # Primeiros 10 conflitos
                'name_conflicts': name_conflicts[:10],  # Primeiros 10 conflitos
                'is_clean': len(url_conflicts) == 0 and len(name_conflicts) == 0
            }
            
            if validation_result['is_clean']:
                print("✅ Validação concluída: Nenhuma duplicata encontrada!")
            else:
                print(f"⚠️ Encontradas {len(url_conflicts)} duplicatas por URL e {len(name_conflicts)} por nome")
            
            return validation_result
            
        except Exception as e:
            print(f"❌ Erro na validação de duplicatas: {e}")
            return {'error': str(e)}


def merge_tools_to_supabase(tools: List[AITool]) -> Dict[str, int]:
    """
    Função de conveniência para fazer merge das ferramentas no Supabase
    
    Args:
        tools: Lista de ferramentas para inserir/atualizar
        
    Returns:
        Dict com estatísticas da operação
    """
    merger = SupabaseMerger()
    return merger.merge_and_upsert_tools(tools)


def get_supabase_statistics() -> Dict[str, Any]:
    """
    Função de conveniência para obter estatísticas do Supabase
    
    Returns:
        Dict com estatísticas do banco
    """
    merger = SupabaseMerger()
    return merger.get_statistics()


def cleanup_supabase_duplicates() -> int:
    """
    Função de conveniência para limpar duplicatas do Supabase
    
    Returns:
        Número de duplicatas removidas
    """
    merger = SupabaseMerger()
    return merger.cleanup_duplicates()


def validate_supabase_no_duplicates() -> Dict[str, Any]:
    """
    Função de conveniência para validar que não há duplicatas no Supabase
    
    Returns:
        Dict com resultado da validação
    """
    merger = SupabaseMerger()
    return merger.validate_no_duplicates()