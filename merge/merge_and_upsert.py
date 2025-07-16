"""
Módulo para fazer merge e upsert das ferramentas de AI no Supabase
"""

import os
import hashlib
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
from scrapers.common import AITool

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
        Faz merge e upsert das ferramentas no Supabase
        
        Args:
            tools: Lista de ferramentas para inserir/atualizar
            
        Returns:
            Dict com estatísticas: {'inserted': n, 'updated': n, 'errors': n}
        """
        stats = {'inserted': 0, 'updated': 0, 'errors': 0}
        
        if not tools:
            print("⚠️ Nenhuma ferramenta para processar")
            return stats
        
        print(f"🔄 Processando {len(tools)} ferramentas...")
        
        for i, tool in enumerate(tools):
            try:
                # Gera hash único para detectar mudanças
                content_hash = self._generate_content_hash(tool)
                
                # Verifica se a ferramenta já existe
                existing_tool = self._get_existing_tool(tool.ext_id, tool.source)
                
                if existing_tool:
                    # Verifica se houve mudanças
                    if existing_tool.get('content_hash') != content_hash:
                        # Atualiza ferramenta existente
                        self._update_tool(existing_tool['id'], tool, content_hash)
                        stats['updated'] += 1
                        print(f"🔄 [{i+1}/{len(tools)}] Atualizado: {tool.name}")
                    else:
                        print(f"⏭️ [{i+1}/{len(tools)}] Sem mudanças: {tool.name}")
                else:
                    # Insere nova ferramenta
                    self._insert_tool(tool, content_hash)
                    stats['inserted'] += 1
                    print(f"✅ [{i+1}/{len(tools)}] Inserido: {tool.name}")
                
            except Exception as e:
                stats['errors'] += 1
                print(f"❌ [{i+1}/{len(tools)}] Erro ao processar {tool.name}: {e}")
                continue
        
        print(f"\n📊 Resultados: {stats['inserted']} inseridas, {stats['updated']} atualizadas, {stats['errors']} erros")
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
            'content_hash': content_hash
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
            'updated_at': 'now()'
        }
        
        response = self.supabase.table('ai_tool').update(tool_data).eq('id', tool_id).execute()
        
        if not response.data:
            raise Exception("Falha ao atualizar ferramenta")
    
    def _generate_content_hash(self, tool: AITool) -> str:
        """Gera hash do conteúdo da ferramenta para detectar mudanças"""
        content = f"{tool.name}|{tool.description}|{tool.price}|{tool.popularity}|{'|'.join(sorted(tool.categories))}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
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