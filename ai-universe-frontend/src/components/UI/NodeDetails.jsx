import React from 'react';

export default function NodeDetails({ node, onClose }) {
  if (!node) return null;

  const formatNumber = (num) => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`;
    }
    return num?.toString() || 'N/A';
  };

  const getRankSuffix = (rank) => {
    if (rank % 10 === 1 && rank % 100 !== 11) return 'st';
    if (rank % 10 === 2 && rank % 100 !== 12) return 'nd';
    if (rank % 10 === 3 && rank % 100 !== 13) return 'rd';
    return 'th';
  };

  return (
    <div className="node-details-overlay">
      <div className="node-details-panel">
        {/* Header */}
        <div className="details-header">
          <div className="node-avatar" style={{ backgroundColor: node.color }}>
            <span className="node-initial">{node.name.charAt(0)}</span>
          </div>
          <div className="header-content">
            <h2>{node.name}</h2>
            <p className="category-badge" style={{ backgroundColor: node.color }}>
              {node.category}
            </p>
          </div>
          <button className="close-button" onClick={onClose}>
            ×
          </button>
        </div>

        {/* Description */}
        <div className="details-section">
          <h3>Descrição</h3>
          <p>{node.description}</p>
        </div>

        {/* Statistics */}
        <div className="details-section">
          <h3>Estatísticas</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Popularidade</span>
              <div className="stat-value">
                <div className="popularity-bar">
                  <div 
                    className="popularity-fill" 
                    style={{ 
                      width: `${node.popularity}%`,
                      backgroundColor: node.color 
                    }}
                  ></div>
                </div>
                <span>{Math.round(node.popularity)}%</span>
              </div>
            </div>

            <div className="stat-item">
              <span className="stat-label">Conexões</span>
              <span className="stat-value">{node.connections}</span>
            </div>

            <div className="stat-item">
              <span className="stat-label">Usuários Mensais</span>
              <span className="stat-value">{formatNumber(node.monthly_users)}</span>
            </div>

            <div className="stat-item">
              <span className="stat-label">Ranking</span>
              <span className="stat-value">
                #{node.rank}{getRankSuffix(node.rank)}
              </span>
            </div>
          </div>
        </div>

        {/* Links */}
        <div className="details-section">
          <h3>Links</h3>
          <div className="links-container">
            {node.url && node.url !== '#' && (
              <a 
                href={node.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="external-link"
              >
                <span className="link-icon">🔗</span>
                Visitar Website
              </a>
            )}
            <button className="action-button secondary">
              <span className="link-icon">📊</span>
              Ver Análise Completa
            </button>
            <button className="action-button secondary">
              <span className="link-icon">🔄</span>
              Ver Conexões
            </button>
          </div>
        </div>

        {/* Node Position Info (Debug) */}
        {process.env.NODE_ENV === 'development' && (
          <div className="details-section debug">
            <h3>Debug Info</h3>
            <div className="debug-info">
              <p>ID: {node.id}</p>
              <p>Size: {node.size?.toFixed(2)}</p>
              <p>Position: x:{node.x?.toFixed(1)}, y:{node.y?.toFixed(1)}, z:{node.z?.toFixed(1)}</p>
              <p>Color: {node.color}</p>
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        .node-details-overlay {
          position: fixed;
          top: 0;
          right: 0;
          width: 400px;
          height: 100vh;
          background: rgba(0, 0, 0, 0.95);
          backdrop-filter: blur(10px);
          border-left: 1px solid rgba(255, 255, 255, 0.1);
          z-index: 1000;
          animation: slideIn 0.3s ease-out;
          overflow-y: auto;
        }

        @keyframes slideIn {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }

        .node-details-panel {
          padding: 2rem;
          color: white;
          font-family: 'Arial', sans-serif;
        }

        .details-header {
          display: flex;
          align-items: center;
          margin-bottom: 2rem;
          padding-bottom: 1rem;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .node-avatar {
          width: 50px;
          height: 50px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-right: 1rem;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        .node-initial {
          font-size: 1.5rem;
          font-weight: bold;
          color: white;
          text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
        }

        .header-content {
          flex: 1;
        }

        .header-content h2 {
          margin: 0;
          font-size: 1.5rem;
          margin-bottom: 0.5rem;
        }

        .category-badge {
          display: inline-block;
          padding: 0.25rem 0.75rem;
          border-radius: 1rem;
          font-size: 0.8rem;
          font-weight: bold;
          color: white;
          text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
        }

        .close-button {
          background: none;
          border: none;
          color: white;
          font-size: 1.5rem;
          cursor: pointer;
          padding: 0.5rem;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background-color 0.2s;
        }

        .close-button:hover {
          background: rgba(255, 255, 255, 0.1);
        }

        .details-section {
          margin-bottom: 2rem;
        }

        .details-section h3 {
          margin: 0 0 1rem 0;
          font-size: 1.1rem;
          color: #a1a1aa;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .details-section p {
          margin: 0;
          line-height: 1.6;
          color: #d4d4d8;
        }

        .stats-grid {
          display: grid;
          gap: 1rem;
        }

        .stat-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 0.5rem;
          border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .stat-label {
          font-size: 0.9rem;
          color: #a1a1aa;
        }

        .stat-value {
          font-weight: bold;
          color: white;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .popularity-bar {
          width: 100px;
          height: 6px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 3px;
          overflow: hidden;
        }

        .popularity-fill {
          height: 100%;
          border-radius: 3px;
          transition: width 0.5s ease;
        }

        .links-container {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .external-link, .action-button {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1rem;
          background: rgba(79, 70, 229, 0.2);
          border: 1px solid rgba(79, 70, 229, 0.4);
          border-radius: 0.5rem;
          color: white;
          text-decoration: none;
          transition: all 0.2s;
          cursor: pointer;
        }

        .action-button.secondary {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .external-link:hover, .action-button:hover {
          background: rgba(79, 70, 229, 0.3);
          border-color: rgba(79, 70, 229, 0.6);
          transform: translateY(-1px);
        }

        .action-button.secondary:hover {
          background: rgba(255, 255, 255, 0.1);
          border-color: rgba(255, 255, 255, 0.2);
        }

        .link-icon {
          font-size: 1rem;
        }

        .debug {
          opacity: 0.7;
          font-size: 0.8rem;
        }

        .debug-info p {
          margin: 0.25rem 0;
          font-family: monospace;
          color: #6b7280;
        }

        /* Responsivo */
        @media (max-width: 768px) {
          .node-details-overlay {
            width: 100vw;
            height: 100vh;
          }
        }
      `}</style>
    </div>
  );
}