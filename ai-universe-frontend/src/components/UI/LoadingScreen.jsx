import React from 'react';

export default function LoadingScreen() {
  return (
    <div className="loading-screen">
      <div className="loading-content">
        {/* Animação de esfera 3D CSS */}
        <div className="loading-sphere">
          <div className="sphere-ring"></div>
          <div className="sphere-ring"></div>
          <div className="sphere-ring"></div>
        </div>
        
        <h2>Carregando AI Universe</h2>
        <p>Preparando {Math.floor(Math.random() * 1000 + 6000)} ferramentas de IA...</p>
        
        {/* Barra de progresso animada */}
        <div className="progress-bar">
          <div className="progress-fill"></div>
        </div>
        
        <div className="loading-steps">
          <div className="step active">
            <span className="step-dot"></span>
            Conectando com base de dados
          </div>
          <div className="step active">
            <span className="step-dot"></span>
            Calculando sinergias entre AIs
          </div>
          <div className="step loading">
            <span className="step-dot"></span>
            Construindo universo 3D
          </div>
          <div className="step">
            <span className="step-dot"></span>
            Preparando navegação
          </div>
        </div>
      </div>
      
      <style jsx>{`
        .loading-screen {
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 9999;
          color: white;
          font-family: 'Arial', sans-serif;
        }
        
        .loading-content {
          text-align: center;
          max-width: 400px;
          padding: 2rem;
        }
        
        .loading-sphere {
          position: relative;
          width: 100px;
          height: 100px;
          margin: 0 auto 2rem;
        }
        
        .sphere-ring {
          position: absolute;
          top: 50%;
          left: 50%;
          border: 2px solid #4f46e5;
          border-radius: 50%;
          transform: translate(-50%, -50%);
          animation: rotate 2s linear infinite;
        }
        
        .sphere-ring:nth-child(1) {
          width: 40px;
          height: 40px;
          animation-delay: 0s;
          border-color: #4f46e5;
        }
        
        .sphere-ring:nth-child(2) {
          width: 60px;
          height: 60px;
          animation-delay: 0.5s;
          border-color: #7c3aed;
          border-top-color: transparent;
        }
        
        .sphere-ring:nth-child(3) {
          width: 80px;
          height: 80px;
          animation-delay: 1s;
          border-color: #dc2626;
          border-top-color: transparent;
          border-right-color: transparent;
        }
        
        @keyframes rotate {
          0% { transform: translate(-50%, -50%) rotate(0deg); }
          100% { transform: translate(-50%, -50%) rotate(360deg); }
        }
        
        h2 {
          font-size: 2rem;
          margin-bottom: 0.5rem;
          background: linear-gradient(45deg, #4f46e5, #7c3aed, #dc2626);
          background-clip: text;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
          from { filter: brightness(1); }
          to { filter: brightness(1.3); }
        }
        
        p {
          font-size: 1rem;
          opacity: 0.8;
          margin-bottom: 2rem;
        }
        
        .progress-bar {
          width: 100%;
          height: 4px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 2px;
          overflow: hidden;
          margin-bottom: 2rem;
        }
        
        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #4f46e5, #7c3aed, #dc2626);
          animation: progress 3s ease-in-out infinite;
          border-radius: 2px;
        }
        
        @keyframes progress {
          0% { width: 0%; transform: translateX(-100%); }
          50% { width: 100%; transform: translateX(0%); }
          100% { width: 100%; transform: translateX(100%); }
        }
        
        .loading-steps {
          text-align: left;
          margin-top: 2rem;
        }
        
        .step {
          display: flex;
          align-items: center;
          margin-bottom: 0.8rem;
          font-size: 0.9rem;
          opacity: 0.5;
          transition: opacity 0.3s ease;
        }
        
        .step.active {
          opacity: 1;
        }
        
        .step.loading {
          opacity: 1;
          animation: pulse 1s ease-in-out infinite;
        }
        
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
        
        .step-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #4f46e5;
          margin-right: 0.8rem;
          flex-shrink: 0;
        }
        
        .step.active .step-dot {
          background: #22c55e;
          box-shadow: 0 0 10px #22c55e;
        }
        
        .step.loading .step-dot {
          background: #f59e0b;
          animation: dot-pulse 1s ease-in-out infinite;
        }
        
        @keyframes dot-pulse {
          0%, 100% { 
            transform: scale(1);
            box-shadow: 0 0 5px #f59e0b;
          }
          50% { 
            transform: scale(1.2);
            box-shadow: 0 0 15px #f59e0b;
          }
        }
      `}</style>
    </div>
  );
}