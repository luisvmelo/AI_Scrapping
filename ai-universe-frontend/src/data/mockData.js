// Mock data para desenvolvimento do AI Universe
// Simulando dados das 87 ferramentas do nosso banco com estrutura otimizada para 3D

export const CATEGORIES = {
  NLP: { color: '#4F46E5', name: 'Natural Language Processing' },
  COMPUTER_VISION: { color: '#DC2626', name: 'Computer Vision' },
  CODING: { color: '#059669', name: 'Coding & Development' },
  OTHER: { color: '#7C3AED', name: 'Other AI Tools' },
  AUDIO: { color: '#EA580C', name: 'Audio & Music' },
  VIDEO: { color: '#DB2777', name: 'Video & Animation' },
  PRODUCTIVITY: { color: '#2563EB', name: 'Productivity' },
  BUSINESS: { color: '#0891B2', name: 'Business & Marketing' }
};

// Dados simulados baseados no nosso banco real - 200 AI tools
export const AI_TOOLS_MOCK = [
  // Top tier - Ferramentas mais famosas (1-20)
  {
    id: 1,
    name: "ChatGPT",
    description: "OpenAI's conversational AI assistant",
    category: "NLP",
    popularity: 98.0,
    connections: 45,
    monthly_users: 200000000,
    url: "https://chat.openai.com",
    rank: 1
  },
  {
    id: 2,
    name: "Bolt.new",
    description: "AI-powered full-stack web development platform",
    category: "CODING",
    popularity: 95.0,
    connections: 38,
    monthly_users: 2000000,
    url: "https://bolt.new",
    position: { x: 15, y: 10, z: -8 },
    rank: 2
  },
  {
    id: 3,
    name: "Claude",
    description: "Anthropic's AI assistant for conversations and text",
    category: "NLP",
    popularity: 92.0,
    connections: 42,
    monthly_users: 50000000,
    url: "https://claude.ai",
    position: { x: -12, y: 5, z: 15 },
    rank: 3
  },
  {
    id: 4,
    name: "Cursor",
    description: "AI-powered code editor",
    category: "CODING",
    popularity: 93.7,
    connections: 35,
    monthly_users: 3000000,
    url: "https://cursor.sh",
    position: { x: 20, y: -8, z: 12 },
    rank: 4
  },
  {
    id: 5,
    name: "Midjourney",
    description: "AI image generation platform",
    category: "COMPUTER_VISION",
    popularity: 90.0,
    connections: 40,
    monthly_users: 15000000,
    url: "https://midjourney.com",
    position: { x: -18, y: 12, z: -10 },
    rank: 5
  },
  {
    id: 6,
    name: "Lovable",
    description: "AI website builder that generates full applications",
    category: "CODING",
    popularity: 92.0,
    connections: 33,
    monthly_users: 1500000,
    url: "https://lovable.dev",
    position: { x: 25, y: 15, z: 5 },
    rank: 6
  },
  {
    id: 7,
    name: "DALL-E 2",
    description: "OpenAI's image generation model",
    category: "COMPUTER_VISION",
    popularity: 88.0,
    connections: 37,
    monthly_users: 8000000,
    url: "https://openai.com/dall-e-2",
    position: { x: -15, y: -10, z: 20 },
    rank: 7
  },
  {
    id: 8,
    name: "V0 by Vercel",
    description: "AI UI generator for React components",
    category: "CODING",
    popularity: 90.0,
    connections: 31,
    monthly_users: 1800000,
    url: "https://v0.dev",
    position: { x: 18, y: 8, z: -15 },
    rank: 8
  },
  {
    id: 9,
    name: "NotebookLM",
    description: "Google's AI research assistant for documents",
    category: "NLP",
    popularity: 88.0,
    connections: 29,
    monthly_users: 3000000,
    url: "https://notebooklm.google.com",
    position: { x: -8, y: 18, z: 8 },
    rank: 9
  },
  {
    id: 10,
    name: "Character.AI",
    description: "AI chatbots with distinct personalities",
    category: "NLP",
    popularity: 87.0,
    connections: 36,
    monthly_users: 8000000,
    url: "https://character.ai",
    position: { x: 10, y: -15, z: -12 },
    rank: 10
  },
  // Segundo tier - Ferramentas populares
  {
    id: 11,
    name: "Stable Diffusion",
    description: "Open-source image generation model",
    category: "COMPUTER_VISION",
    popularity: 85.0,
    connections: 34,
    monthly_users: 5000000,
    url: "https://stability.ai",
    position: { x: -22, y: 6, z: 18 },
    rank: 11
  },
  {
    id: 12,
    name: "GitHub Copilot",
    description: "AI coding assistant",
    category: "CODING",
    popularity: 88.0,
    connections: 39,
    monthly_users: 10000000,
    url: "https://github.com/features/copilot",
    position: { x: 12, y: 20, z: -5 },
    rank: 12
  },
  {
    id: 13,
    name: "ElevenLabs",
    description: "AI voice synthesis",
    category: "AUDIO",
    popularity: 84.0,
    connections: 28,
    monthly_users: 2000000,
    url: "https://elevenlabs.io",
    position: { x: -10, y: -12, z: 25 },
    rank: 13
  },
  {
    id: 14,
    name: "Suno AI",
    description: "AI music generation from text prompts",
    category: "AUDIO",
    popularity: 84.0,
    connections: 26,
    monthly_users: 2500000,
    url: "https://suno.ai",
    position: { x: 8, y: 25, z: 10 },
    rank: 14
  },
  {
    id: 15,
    name: "Runway ML",
    description: "AI video and image editing",
    category: "VIDEO",
    popularity: 82.0,
    connections: 30,
    monthly_users: 1800000,
    url: "https://runwayml.com",
    position: { x: -25, y: -8, z: -15 },
    rank: 15
  },
  {
    id: 16,
    name: "Poe",
    description: "AI chatbot platform by Quora with multiple models",
    category: "NLP",
    popularity: 85.0,
    connections: 32,
    monthly_users: 5000000,
    url: "https://poe.com",
    position: { x: 5, y: -20, z: 18 },
    rank: 16
  },
  {
    id: 17,
    name: "Luma AI",
    description: "AI 3D scene generation and video creation",
    category: "COMPUTER_VISION",
    popularity: 83.0,
    connections: 25,
    monthly_users: 1000000,
    url: "https://lumalabs.ai",
    position: { x: 30, y: 5, z: -8 },
    rank: 17
  },
  {
    id: 18,
    name: "Jasper",
    description: "AI content writing platform",
    category: "NLP",
    popularity: 81.0,
    connections: 27,
    monthly_users: 1500000,
    url: "https://jasper.ai",
    position: { x: -5, y: 22, z: -20 },
    rank: 18
  },
  {
    id: 19,
    name: "Copy.ai",
    description: "AI copywriting tool",
    category: "NLP",
    popularity: 79.0,
    connections: 24,
    monthly_users: 1200000,
    url: "https://copy.ai",
    position: { x: 22, y: -12, z: 8 },
    rank: 19
  },
  {
    id: 20,
    name: "Perplexity",
    description: "AI-powered search engine",
    category: "NLP",
    popularity: 86.0,
    connections: 33,
    monthly_users: 4000000,
    url: "https://perplexity.ai",
    position: { x: -18, y: 8, z: -25 },
    rank: 20
  }
];

// Conexões baseadas em sinergias reais entre as ferramentas
export const SYNERGIES_MOCK = [
  // ChatGPT como hub central conecta com muitas ferramentas
  { source: 1, target: 3, strength: 0.9, type: 'complementary' }, // ChatGPT ↔ Claude
  { source: 1, target: 9, strength: 0.8, type: 'functional' }, // ChatGPT ↔ NotebookLM
  { source: 1, target: 16, strength: 0.85, type: 'competitive' }, // ChatGPT ↔ Poe
  { source: 1, target: 18, strength: 0.7, type: 'functional' }, // ChatGPT ↔ Jasper
  
  // Coding tools conectam entre si
  { source: 2, target: 4, strength: 0.8, type: 'complementary' }, // Bolt ↔ Cursor
  { source: 2, target: 6, strength: 0.9, type: 'competitive' }, // Bolt ↔ Lovable
  { source: 2, target: 8, strength: 0.85, type: 'functional' }, // Bolt ↔ V0
  { source: 4, target: 12, strength: 0.9, type: 'complementary' }, // Cursor ↔ GitHub Copilot
  { source: 8, target: 12, strength: 0.7, type: 'functional' }, // V0 ↔ GitHub Copilot
  { source: 6, target: 8, strength: 0.8, type: 'competitive' }, // Lovable ↔ V0
  
  // Image generation tools
  { source: 5, target: 7, strength: 0.9, type: 'competitive' }, // Midjourney ↔ DALL-E
  { source: 5, target: 11, strength: 0.85, type: 'competitive' }, // Midjourney ↔ Stable Diffusion
  { source: 7, target: 11, strength: 0.8, type: 'competitive' }, // DALL-E ↔ Stable Diffusion
  { source: 17, target: 5, strength: 0.6, type: 'functional' }, // Luma ↔ Midjourney
  
  // NLP tools network
  { source: 3, target: 10, strength: 0.7, type: 'functional' }, // Claude ↔ Character.AI
  { source: 16, target: 10, strength: 0.8, type: 'complementary' }, // Poe ↔ Character.AI
  { source: 18, target: 19, strength: 0.9, type: 'competitive' }, // Jasper ↔ Copy.ai
  { source: 20, target: 1, strength: 0.7, type: 'functional' }, // Perplexity ↔ ChatGPT
  
  // Audio/Video connections
  { source: 13, target: 14, strength: 0.8, type: 'complementary' }, // ElevenLabs ↔ Suno
  { source: 15, target: 5, strength: 0.6, type: 'functional' }, // Runway ↔ Midjourney
  { source: 15, target: 17, strength: 0.7, type: 'functional' }, // Runway ↔ Luma
  
  // Cross-domain synergies
  { source: 2, target: 5, strength: 0.5, type: 'workflow' }, // Bolt ↔ Midjourney (web + images)
  { source: 1, target: 13, strength: 0.6, type: 'workflow' }, // ChatGPT ↔ ElevenLabs (text to voice)
  { source: 18, target: 5, strength: 0.7, type: 'workflow' }, // Jasper ↔ Midjourney (content + images)
  { source: 19, target: 7, strength: 0.6, type: 'workflow' }, // Copy.ai ↔ DALL-E
  { source: 9, target: 20, strength: 0.8, type: 'functional' }, // NotebookLM ↔ Perplexity (research)
];

// Função para gerar posições aleatórias para ferramentas adicionais
export const generateRandomPosition = (index, total) => {
  const radius = 50 + (index / total) * 100; // Aumenta o raio conforme o index
  const phi = Math.acos(-1 + (2 * index) / total); // Distribuição esférica
  const theta = Math.sqrt(total * Math.PI) * phi;
  
  return {
    x: radius * Math.cos(theta) * Math.sin(phi),
    y: radius * Math.sin(theta) * Math.sin(phi),
    z: radius * Math.cos(phi)
  };
};

// Função para calcular o tamanho do nó baseado na popularidade
export const calculateNodeSize = (popularity, connections) => {
  const baseSize = 1;
  const popularityFactor = (popularity / 100) * 3; // 0-3 baseado na popularidade
  const connectionsFactor = Math.log(connections + 1) * 0.5; // Fator logarítmico das conexões
  return baseSize + popularityFactor + connectionsFactor;
};

// Função para obter cor da categoria
export const getCategoryColor = (category) => {
  return CATEGORIES[category]?.color || '#6B7280';
};

// Export do dataset completo formatado para react-force-graph-3d
export const getGraphData = () => {
  const nodes = AI_TOOLS_MOCK.map(tool => ({
    id: tool.id,
    name: tool.name,
    description: tool.description,
    category: tool.category,
    popularity: tool.popularity,
    connections: tool.connections,
    monthly_users: tool.monthly_users,
    url: tool.url,
    rank: tool.rank,
    val: calculateNodeSize(tool.popularity, tool.connections), // Dynamic size based on popularity
    color: getCategoryColor(tool.category) // Dynamic color by category
    // Remove fixed positions to let force simulation work naturally
  }));

  const links = SYNERGIES_MOCK.map(synergy => ({
    source: synergy.source,
    target: synergy.target,
    strength: synergy.strength,
    type: synergy.type,
    color: getConnectionColor(synergy.type) // Dynamic color by connection type
  }));

  return { nodes, links };
};

// Função para obter cor das conexões baseada no tipo
export const getConnectionColor = (type) => {
  const colors = {
    'complementary': 'rgba(34, 197, 94, 0.6)', // Verde - ferramentas que se complementam
    'competitive': 'rgba(239, 68, 68, 0.6)', // Vermelho - ferramentas concorrentes
    'functional': 'rgba(59, 130, 246, 0.6)', // Azul - relação funcional
    'workflow': 'rgba(168, 85, 247, 0.6)' // Roxo - integração de workflow
  };
  return colors[type] || 'rgba(156, 163, 175, 0.4)';
};