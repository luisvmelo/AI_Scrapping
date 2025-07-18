import React, { useState } from 'react';
import { CATEGORIES } from '../../data/mockData';

export default function GraphControls({ 
  filters, 
  updateFilters, 
  resetFilters, 
  statistics, 
  showStats, 
  setShowStats 
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleCategoryToggle = (category) => {
    const newCategories = filters.categories.includes(category)
      ? filters.categories.filter(c => c !== category)
      : [...filters.categories, category];
    
    updateFilters({ categories: newCategories });
  };

  const handlePopularityChange = (value, index) => {
    const newRange = [...filters.popularityRange];
    newRange[index] = value;
    updateFilters({ popularityRange: newRange });
  };

  const handleConnectionsChange = (value, index) => {
    const newRange = [...filters.connectionsRange];
    newRange[index] = value;
    updateFilters({ connectionsRange: newRange });
  };

  const handleSearchChange = (e) => {
    updateFilters({ searchTerm: e.target.value });
  };

  return (
    <div className={`graph-controls ${isExpanded ? 'expanded' : 'collapsed'}`}>
      {/* Toggle Button */}
      <button 
        className="controls-toggle"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <span className="toggle-icon">{isExpanded ? '←' : '→'}</span>
        <span className="toggle-text">Controles</span>
      </button>

      {/* Controls Panel */}
      <div className="controls-panel">
        {/* Header */}
        <div className="controls-header">
          <h3>AI Universe</h3>
          <div className="header-stats">
            <span className="stat">
              {statistics?.filteredCount || 0} / {statistics?.totalNodes || 0} nós
            </span>
          </div>
        </div>

        {/* Search */}
        <div className="control-section">
          <label>Buscar</label>
          <input
            type="text"
            placeholder="Nome ou descrição..."
            value={filters.searchTerm}
            onChange={handleSearchChange}
            className="search-input"
          />
        </div>

        {/* Category Filters */}
        <div className="control-section">
          <label>Categorias</label>
          <div className="category-filters">
            {Object.entries(CATEGORIES).map(([key, category]) => (
              <button
                key={key}
                className={`category-filter ${filters.categories.includes(key) ? 'active' : ''}`}
                style={{
                  borderColor: category.color,
                  backgroundColor: filters.categories.includes(key) ? category.color : 'transparent',
                  color: filters.categories.includes(key) ? 'white' : category.color
                }}
                onClick={() => handleCategoryToggle(key)}
              >
                <span className="category-dot" style={{ backgroundColor: category.color }}></span>
                {key}
              </button>
            ))}
          </div>
        </div>

        {/* Popularity Range */}
        <div className="control-section">
          <label>
            Popularidade ({filters.popularityRange[0]}% - {filters.popularityRange[1]}%)
          </label>
          <div className="range-container">
            <input
              type="range"
              min="0"
              max="100"
              value={filters.popularityRange[0]}
              onChange={(e) => handlePopularityChange(parseInt(e.target.value), 0)}
              className="range-slider min"
            />
            <input
              type="range"
              min="0"
              max="100"
              value={filters.popularityRange[1]}
              onChange={(e) => handlePopularityChange(parseInt(e.target.value), 1)}
              className="range-slider max"
            />
          </div>
        </div>

        {/* Connections Range */}
        <div className="control-section">
          <label>
            Conexões ({filters.connectionsRange[0]} - {filters.connectionsRange[1]})
          </label>
          <div className="range-container">
            <input
              type="range"
              min="0"
              max="50"
              value={filters.connectionsRange[0]}
              onChange={(e) => handleConnectionsChange(parseInt(e.target.value), 0)}
              className="range-slider min"
            />
            <input
              type="range"
              min="0"
              max="50"
              value={filters.connectionsRange[1]}
              onChange={(e) => handleConnectionsChange(parseInt(e.target.value), 1)}
              className="range-slider max"
            />
          </div>
        </div>

        {/* Actions */}
        <div className="control-section">
          <div className="action-buttons">
            <button className="action-btn reset" onClick={resetFilters}>
              🔄 Reset
            </button>
            <button 
              className={`action-btn stats ${showStats ? 'active' : ''}`}
              onClick={() => setShowStats(!showStats)}
            >
              📊 Stats
            </button>
          </div>
        </div>

        {/* Statistics Panel */}
        {statistics && (
          <div className="control-section">
            <label>Estatísticas</label>
            <div className="stats-panel">
              <div className="stat-row">
                <span>Total de nós:</span>
                <span>{statistics.totalNodes}</span>
              </div>
              <div className="stat-row">
                <span>Conexões:</span>
                <span>{statistics.totalLinks}</span>
              </div>
              <div className="stat-row">
                <span>Pop. média:</span>
                <span>{statistics.avgPopularity}%</span>
              </div>
              <div className="stat-row">
                <span>Conn. média:</span>
                <span>{statistics.avgConnections}</span>
              </div>
            </div>

            {/* Category Distribution */}
            <div className="category-distribution">
              <h4>Distribuição por Categoria</h4>
              {Object.entries(statistics.categoryDistribution || {}).map(([category, count]) => (
                <div key={category} className="category-stat">
                  <div className="category-info">
                    <span 
                      className="category-color" 
                      style={{ backgroundColor: CATEGORIES[category]?.color || '#6B7280' }}
                    ></span>
                    <span className="category-name">{category}</span>
                  </div>
                  <span className="category-count">{count}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        .graph-controls {
          position: fixed;
          top: 0;
          left: 0;
          height: 100vh;
          background: rgba(0, 0, 0, 0.9);
          backdrop-filter: blur(10px);
          border-right: 1px solid rgba(255, 255, 255, 0.1);
          z-index: 100;
          transition: transform 0.3s ease;
          display: flex;
          color: white;
          font-family: 'Arial', sans-serif;
        }

        .graph-controls.collapsed {
          transform: translateX(-300px);
        }

        .graph-controls.expanded {
          transform: translateX(0);
        }

        .controls-toggle {
          position: absolute;
          right: -50px;
          top: 50%;
          transform: translateY(-50%);
          background: rgba(0, 0, 0, 0.8);
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: white;
          padding: 1rem 0.5rem;
          border-radius: 0 8px 8px 0;
          cursor: pointer;
          writing-mode: vertical-rl;
          text-orientation: mixed;
          transition: all 0.3s ease;
          backdrop-filter: blur(10px);
        }

        .controls-toggle:hover {
          background: rgba(79, 70, 229, 0.8);
          border-color: rgba(79, 70, 229, 0.4);
        }

        .toggle-icon {
          font-size: 1.2rem;
          margin-bottom: 0.5rem;
        }

        .toggle-text {
          font-size: 0.8rem;
          font-weight: bold;
        }

        .controls-panel {
          width: 320px;
          padding: 1.5rem;
          overflow-y: auto;
          scrollbar-width: thin;
          scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
        }

        .controls-panel::-webkit-scrollbar {
          width: 4px;
        }

        .controls-panel::-webkit-scrollbar-track {
          background: transparent;
        }

        .controls-panel::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.2);
          border-radius: 2px;
        }

        .controls-header {
          margin-bottom: 2rem;
          padding-bottom: 1rem;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .controls-header h3 {
          margin: 0 0 0.5rem 0;
          font-size: 1.5rem;
          background: linear-gradient(45deg, #4f46e5, #7c3aed, #dc2626);
          background-clip: text;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .header-stats .stat {
          font-size: 0.9rem;
          color: #a1a1aa;
        }

        .control-section {
          margin-bottom: 1.5rem;
        }

        .control-section label {
          display: block;
          margin-bottom: 0.5rem;
          font-size: 0.9rem;
          color: #a1a1aa;
          font-weight: bold;
        }

        .search-input {
          width: 100%;
          padding: 0.75rem;
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 0.5rem;
          color: white;
          font-size: 0.9rem;
        }

        .search-input:focus {
          outline: none;
          border-color: #4f46e5;
          box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
        }

        .search-input::placeholder {
          color: #6b7280;
        }

        .category-filters {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }

        .category-filter {
          display: flex;
          align-items: center;
          gap: 0.3rem;
          padding: 0.4rem 0.8rem;
          border: 1px solid;
          border-radius: 1rem;
          background: transparent;
          cursor: pointer;
          font-size: 0.8rem;
          transition: all 0.2s;
          text-transform: uppercase;
          font-weight: bold;
        }

        .category-filter:hover {
          transform: translateY(-1px);
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }

        .category-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
        }

        .range-container {
          position: relative;
          height: 20px;
          margin: 0.5rem 0;
        }

        .range-slider {
          position: absolute;
          width: 100%;
          height: 4px;
          background: transparent;
          outline: none;
          -webkit-appearance: none;
          cursor: pointer;
        }

        .range-slider::-webkit-slider-track {
          height: 4px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 2px;
        }

        .range-slider::-webkit-slider-thumb {
          -webkit-appearance: none;
          width: 16px;
          height: 16px;
          background: #4f46e5;
          border-radius: 50%;
          cursor: pointer;
          box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.3);
        }

        .range-slider::-moz-range-track {
          height: 4px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 2px;
        }

        .range-slider::-moz-range-thumb {
          width: 16px;
          height: 16px;
          background: #4f46e5;
          border-radius: 50%;
          cursor: pointer;
          border: none;
          box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.3);
        }

        .action-buttons {
          display: flex;
          gap: 0.5rem;
        }

        .action-btn {
          flex: 1;
          padding: 0.75rem;
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 0.5rem;
          background: rgba(255, 255, 255, 0.05);
          color: white;
          cursor: pointer;
          font-size: 0.9rem;
          transition: all 0.2s;
        }

        .action-btn:hover {
          background: rgba(255, 255, 255, 0.1);
          transform: translateY(-1px);
        }

        .action-btn.active {
          background: #4f46e5;
          border-color: #4f46e5;
        }

        .action-btn.reset:hover {
          background: #dc2626;
          border-color: #dc2626;
        }

        .stats-panel {
          background: rgba(255, 255, 255, 0.05);
          border-radius: 0.5rem;
          padding: 1rem;
          margin-bottom: 1rem;
        }

        .stat-row {
          display: flex;
          justify-content: space-between;
          margin-bottom: 0.5rem;
          font-size: 0.9rem;
        }

        .stat-row span:first-child {
          color: #a1a1aa;
        }

        .stat-row span:last-child {
          color: white;
          font-weight: bold;
        }

        .category-distribution h4 {
          margin: 0 0 0.5rem 0;
          font-size: 0.9rem;
          color: #a1a1aa;
        }

        .category-stat {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.3rem;
          font-size: 0.8rem;
        }

        .category-info {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .category-color {
          width: 8px;
          height: 8px;
          border-radius: 50%;
        }

        .category-name {
          color: #d4d4d8;
        }

        .category-count {
          color: white;
          font-weight: bold;
        }
      `}</style>
    </div>
  );
}