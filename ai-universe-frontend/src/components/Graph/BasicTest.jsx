import React from 'react';

export default function BasicTest() {
  console.log('BasicTest component rendering');
  
  return (
    <div style={{ 
      width: '100vw', 
      height: '100vh', 
      backgroundColor: 'black',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      color: 'white'
    }}>
      <div>
        <h1>Basic Test - React Working!</h1>
        <p>If you see this, React is working fine.</p>
        <div style={{
          width: '50px',
          height: '50px',
          backgroundColor: 'red',
          borderRadius: '50%',
          margin: '20px auto'
        }}></div>
        <p>Red circle above simulates a node</p>
      </div>
    </div>
  );
}