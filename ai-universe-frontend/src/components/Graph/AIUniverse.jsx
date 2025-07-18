import React, { useRef, useCallback, useState } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import { useAIData } from '../../hooks/useAIData';
import { CATEGORIES } from '../../data/mockData200';

export default function AIUniverse({ apiMode = false }) {
  const { data, loading, error } = useAIData(apiMode);
  const [selectedNode, setSelectedNode] = useState(null);
  const [selectedLink, setSelectedLink] = useState(null);
  const graphRef = useRef();

  // Handler para click em nó
  const handleNodeClick = useCallback((node) => {
    if (!node) return;
    setSelectedNode(node);
    setSelectedLink(null); // Clear link selection when node is clicked
    console.log('Node clicked:', node.name);
  }, []);

  // Handler para click em link
  const handleLinkClick = useCallback((link) => {
    if (!link) return;
    setSelectedLink(link);
    setSelectedNode(null); // Clear node selection when link is clicked
    console.log('Link clicked:', link);
  }, []);

  // Handler para hover em nó
  const handleNodeHover = useCallback((node) => {
    document.body.style.cursor = node ? 'pointer' : 'default';
  }, []);

  // Handler para hover em link
  const handleLinkHover = useCallback((link) => {
    document.body.style.cursor = link ? 'pointer' : 'default';
  }, []);

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh', 
        color: 'white',
        backgroundColor: 'black'
      }}>
        <h2>Carregando...</h2>
      </div>
    );
  }
  
  if (error) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh', 
        color: 'white',
        backgroundColor: 'black'
      }}>
        <div>
          <h2>Erro: {error}</h2>
          <button onClick={() => window.location.reload()}>
            Tentar novamente
          </button>
        </div>
      </div>
    );
  }

  if (!data || !data.nodes || data.nodes.length === 0) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh', 
        color: 'white',
        backgroundColor: 'black'
      }}>
        <div>
          <h2>Nenhum dado encontrado</h2>
          <p>Dados: {data ? JSON.stringify(data, null, 2) : 'null'}</p>
        </div>
      </div>
    );
  }

  console.log('Rendering graph with data:', data);

  return (
    <div style={{ width: '100vw', height: '100vh', backgroundColor: 'black' }}>
      <ForceGraph3D
        ref={graphRef}
        graphData={data}
        
        // Configurações básicas do nó
        nodeVal={node => Math.max(1, (node.val || 1))}
        nodeColor={node => node.color || '#4f46e5'} // Dynamic color by category
        nodeLabel={node => `${node.name} (${node.category})`}
        nodeOpacity={1}
        
        // Configurações básicas do link
        linkColor={link => link.color || 'rgba(255, 255, 255, 0.3)'}
        linkWidth={link => Math.max(0.5, (link.strength || 0.5) * 2)}
        
        // Eventos básicos
        onNodeClick={handleNodeClick}
        onNodeHover={handleNodeHover}
        onLinkClick={handleLinkClick}
        onLinkHover={handleLinkHover}
        
        // Configurações da simulação
        d3AlphaDecay={0.01}
        d3VelocityDecay={0.08}
        
        // Configurações básicas
        numDimensions={3}
        enableNodeDrag={true}
        enableNavigationControls={true}
        
        // Background preto
        backgroundColor="black"
        
        // Configurações de controle
        controlType="orbit"
        
        width={window.innerWidth}
        height={window.innerHeight}
      />
      
      {/* Info básica do nó selecionado */}
      {selectedNode && (
        <div style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          background: 'rgba(0, 0, 0, 0.8)',
          color: 'white',
          padding: '20px',
          borderRadius: '8px',
          border: '1px solid #333',
          maxWidth: '300px'
        }}>
          <h3 style={{ color: selectedNode.color }}>{selectedNode.name}</h3>
          <p>{selectedNode.description}</p>
          <p><strong>Categoria:</strong> {selectedNode.category}</p>
          <p><strong>Popularidade:</strong> {Math.round(selectedNode.popularity)}%</p>
          <p><strong>Conexões:</strong> {selectedNode.connections}</p>
          <p><strong>Usuários mensais:</strong> {(selectedNode.monthly_users / 1000000).toFixed(1)}M</p>
          
          {selectedNode.possibleConnections && selectedNode.possibleConnections.length > 0 && (
            <div style={{ marginTop: '15px' }}>
              <h4 style={{ margin: '0 0 8px 0', fontSize: '14px' }}>Possíveis Conexões:</h4>
              <div style={{ maxHeight: '120px', overflowY: 'auto' }}>
                {selectedNode.possibleConnections.slice(0, 5).map((conn, index) => (
                  <div key={index} style={{ marginBottom: '5px', fontSize: '12px' }}>
                    <strong>{conn.name}</strong> - {conn.type}
                  </div>
                ))}
                {selectedNode.possibleConnections.length > 5 && (
                  <p style={{ fontSize: '11px', fontStyle: 'italic' }}>
                    +{selectedNode.possibleConnections.length - 5} mais conexões
                  </p>
                )}
              </div>
            </div>
          )}
          <button 
            onClick={() => setSelectedNode(null)}
            style={{
              background: '#4f46e5',
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Fechar
          </button>
        </div>
      )}
      
      {/* Link details panel */}
      {selectedLink && (
        <div style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          background: 'rgba(0, 0, 0, 0.8)',
          color: 'white',
          padding: '20px',
          borderRadius: '8px',
          border: '1px solid #333',
          maxWidth: '300px'
        }}>
          <h3 style={{ color: selectedLink.color, margin: '0 0 10px 0' }}>Conexão</h3>
          <p><strong>Tipo:</strong> {selectedLink.type}</p>
          <p><strong>Força:</strong> {Math.round((selectedLink.strength || 0.5) * 100)}%</p>
          {selectedLink.description && (
            <div style={{ marginTop: '10px' }}>
              <p style={{ fontSize: '14px', lineHeight: '1.4' }}>
                <strong>Relação:</strong> {selectedLink.description}
              </p>
            </div>
          )}
          <button 
            onClick={() => setSelectedLink(null)}
            style={{
              background: '#4f46e5',
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              borderRadius: '4px',
              cursor: 'pointer',
              marginTop: '10px'
            }}
          >
            Fechar
          </button>
        </div>
      )}
      
      {/* Legend for categories */}
      <div style={{
        position: 'fixed',
        bottom: '20px',
        left: '20px',
        background: 'rgba(0, 0, 0, 0.8)',
        color: 'white',
        padding: '15px',
        borderRadius: '8px',
        border: '1px solid #333',
        fontSize: '12px'
      }}>
        <h4 style={{ margin: '0 0 10px 0' }}>Categorias:</h4>
        {Object.entries(CATEGORIES).map(([key, category]) => (
          <div key={key} style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
            <div style={{
              width: '12px',
              height: '12px',
              backgroundColor: category.color,
              borderRadius: '50%',
              marginRight: '8px'
            }}></div>
            <span>{category.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}