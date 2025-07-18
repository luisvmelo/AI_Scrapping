import React, { useEffect, useState } from 'react';
import ForceGraph3D from 'react-force-graph-3d';

// Dados mínimos para teste
const debugData = {
  nodes: [
    { id: 1, name: 'Test Node 1', val: 10 },
    { id: 2, name: 'Test Node 2', val: 15 }, 
    { id: 3, name: 'Test Node 3', val: 20 }
  ],
  links: [
    { source: 1, target: 2 },
    { source: 2, target: 3 }
  ]
};

export default function AIUniverseDebug() {
  const [forceGraphLoaded, setForceGraphLoaded] = useState(false);
  
  useEffect(() => {
    console.log('AIUniverseDebug mounted with data:', debugData);
    console.log('Window dimensions:', window.innerWidth, window.innerHeight);
    
    // Check if ForceGraph3D loaded
    setTimeout(() => {
      setForceGraphLoaded(true);
      console.log('ForceGraph3D should be loaded now');
    }, 1000);
  }, []);

  console.log('AIUniverseDebug rendering, forceGraphLoaded:', forceGraphLoaded);

  return (
    <div style={{ width: '100vw', height: '100vh', backgroundColor: 'black', position: 'relative' }}>
      <div style={{ 
        color: 'white', 
        position: 'absolute', 
        top: 10, 
        left: 10, 
        zIndex: 1000,
        backgroundColor: 'rgba(0,0,0,0.8)',
        padding: '10px',
        borderRadius: '5px'
      }}>
        <h3>Debug Mode</h3>
        <p>Should see 3 red nodes</p>
        <p>ForceGraph loaded: {forceGraphLoaded ? 'Yes' : 'Loading...'}</p>
        <p>Nodes: {debugData.nodes.length}</p>
        <p>Links: {debugData.links.length}</p>
      </div>
      
      <ForceGraph3D
        graphData={debugData}
        nodeVal={node => node.val || 10}
        nodeColor={() => '#ff0000'} // Bright red for visibility
        nodeOpacity={1}
        backgroundColor="black"
        width={window.innerWidth}
        height={window.innerHeight}
        nodeLabel={node => `${node.id}: ${node.name}`}
        onNodeClick={(node) => {
          console.log('Clicked node:', node);
          alert(`Clicked: ${node.name}`);
        }}
        linkColor={() => '#ffffff'}
        linkOpacity={0.8}
        linkWidth={2}
        enableNodeDrag={true}
        enableNavigationControls={true}
        showNavInfo={true}
      />
    </div>
  );
}