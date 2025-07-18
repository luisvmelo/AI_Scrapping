import React from 'react';
import AIUniverse from './components/Graph/AIUniverse';

function App() {
  return (
    <div style={{ margin: 0, padding: 0, overflow: 'hidden' }}>
      <AIUniverse apiMode={false} />
    </div>
  );
}

export default App;
