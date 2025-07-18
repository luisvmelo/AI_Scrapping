import { useState, useEffect } from 'react';
import { getGraphData } from '../data/mockData200';

// Hook simplificado para gerenciar dados das AIs
export const useAIData = (apiMode = false) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // API endpoint do nosso backend SQLite
  const API_BASE_URL = 'http://localhost:5000/api';

  // Função para buscar dados da API real
  const fetchFromAPI = async () => {
    try {
      setLoading(true);
      console.log('Fetching from API...');
      
      // Busca nodes da API
      const nodesResponse = await fetch(`${API_BASE_URL}/graph/nodes?limit=100`);
      if (!nodesResponse.ok) {
        throw new Error('Failed to fetch nodes from API');
      }
      const nodesData = await nodesResponse.json();
      console.log('API Nodes data:', nodesData);
      
      // Busca edges da API (conexões/sinergias)
      const edgesResponse = await fetch(`${API_BASE_URL}/graph/edges?limit=200`);
      if (!edgesResponse.ok) {
        throw new Error('Failed to fetch edges from API');
      }
      const edgesData = await edgesResponse.json();
      console.log('API Edges data:', edgesData);
      
      // Transforma dados da API para formato do grafo
      const transformedData = transformAPIData(nodesData.nodes, edgesData.edges);
      console.log('Transformed API data:', transformedData);
      setData(transformedData);
      setError(null);
      
    } catch (err) {
      console.error('Error fetching from API:', err);
      setError(err.message);
      // Fallback para dados mock
      console.log('Falling back to mock data');
      setData(getGraphData());
    } finally {
      setLoading(false);
    }
  };

  // Função para transformar dados da API para formato do grafo
  const transformAPIData = (apiNodes, apiEdges) => {
    console.log('Transforming API data...', apiNodes, apiEdges);
    
    // Mapeamento de categorias para cores
    const categoryColors = {
      'NLP': '#4f46e5',
      'COMPUTER_VISION': '#dc2626', 
      'CODING': '#059669',
      'OTHER': '#7c3aed'
    };

    // Transforma nodes da API
    const nodes = apiNodes.map((node, index) => ({
      id: node.id,
      name: node.name,
      description: node.description || 'AI Tool',
      category: node.macro_domain || 'OTHER',
      popularity: node.popularity || 50,
      connections: node.degree || 5,
      monthly_users: node.monthly_users || 100000,
      url: node.url || '#',
      rank: index + 1,
      size: calculateNodeSize(node.popularity || 50, node.degree || 5),
      color: categoryColors[node.macro_domain] || '#6B7280',
    }));

    // Transforma edges da API (se disponível)
    const links = apiEdges?.map(edge => ({
      source: edge.tool_id_1,
      target: edge.tool_id_2,
      strength: edge.strength || 0.5,
      type: edge.edge_type || 'functional',
      color: 'rgba(255, 255, 255, 0.3)'
    })) || [];

    return { nodes, links };
  };

  // Função para calcular tamanho do nó
  const calculateNodeSize = (popularity, connections) => {
    const baseSize = 1;
    const popularityFactor = (popularity / 100) * 2;
    const connectionsFactor = Math.log(connections + 1) * 0.5;
    return Math.max(0.5, baseSize + popularityFactor + connectionsFactor);
  };

  // Effect para carregar dados
  useEffect(() => {
    console.log('useAIData useEffect, apiMode:', apiMode);
    
    if (apiMode) {
      fetchFromAPI();
    } else {
      // Check if we should use real data (if database has enough tools)
      checkRealDataAvailability();
    }
  }, [apiMode]);

  // Function to check if real data is available
  const checkRealDataAvailability = async () => {
    try {
      console.log('Checking real data availability...');
      const response = await fetch(`${API_BASE_URL}/graph/nodes?limit=5`);
      
      if (response.ok) {
        const result = await response.json();
        const toolCount = result.nodes ? result.nodes.length : 0;
        
        console.log(`Found ${toolCount} tools in database`);
        
        // If we have at least 50 real tools, use them instead of mock data
        if (toolCount >= 50) {
          console.log('Using real scraped data!');
          fetchFromAPI();
          return;
        }
      }
      
      // Fallback to mock data
      console.log('Using mock data (insufficient real data)');
      setTimeout(() => {
        const mockData = getGraphData();
        console.log('Mock data loaded:', mockData);
        setData(mockData);
        setLoading(false);
      }, 500);
      
    } catch (error) {
      console.log('API not available, using mock data');
      setTimeout(() => {
        const mockData = getGraphData();
        console.log('Mock data loaded:', mockData);
        setData(mockData);
        setLoading(false);
      }, 500);
    }
  };

  console.log('useAIData returning:', { data, loading, error });

  return {
    data,
    loading,
    error,
    refetch: apiMode ? fetchFromAPI : () => {}
  };
};