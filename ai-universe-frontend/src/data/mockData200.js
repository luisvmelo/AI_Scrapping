// Mock data para desenvolvimento do AI Universe - 200 AI Tools
// Simulando dados das ferramentas com estrutura otimizada para 3D

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

// 200 AI Tools - Comprehensive dataset
export const AI_TOOLS_MOCK = [
  // Top tier - Most famous (1-20)
  { id: 1, name: "ChatGPT", description: "OpenAI's conversational AI assistant", category: "NLP", popularity: 98.0, connections: 45, monthly_users: 200000000, url: "https://chat.openai.com", rank: 1 },
  { id: 2, name: "Bolt.new", description: "AI-powered full-stack web development platform", category: "CODING", popularity: 95.0, connections: 38, monthly_users: 2000000, url: "https://bolt.new", rank: 2 },
  { id: 3, name: "Claude", description: "Anthropic's AI assistant for conversations and text", category: "NLP", popularity: 92.0, connections: 42, monthly_users: 50000000, url: "https://claude.ai", rank: 3 },
  { id: 4, name: "Cursor", description: "AI-powered code editor", category: "CODING", popularity: 93.7, connections: 35, monthly_users: 3000000, url: "https://cursor.sh", rank: 4 },
  { id: 5, name: "Midjourney", description: "AI image generation platform", category: "COMPUTER_VISION", popularity: 90.0, connections: 40, monthly_users: 15000000, url: "https://midjourney.com", rank: 5 },
  { id: 6, name: "Lovable", description: "AI website builder that generates full applications", category: "CODING", popularity: 92.0, connections: 33, monthly_users: 1500000, url: "https://lovable.dev", rank: 6 },
  { id: 7, name: "DALL-E 2", description: "OpenAI's image generation model", category: "COMPUTER_VISION", popularity: 88.0, connections: 37, monthly_users: 8000000, url: "https://openai.com/dall-e-2", rank: 7 },
  { id: 8, name: "V0 by Vercel", description: "AI UI generator for React components", category: "CODING", popularity: 90.0, connections: 31, monthly_users: 1800000, url: "https://v0.dev", rank: 8 },
  { id: 9, name: "NotebookLM", description: "Google's AI research assistant for documents", category: "PRODUCTIVITY", popularity: 88.0, connections: 29, monthly_users: 3000000, url: "https://notebooklm.google.com", rank: 9 },
  { id: 10, name: "Character.AI", description: "AI chatbots with distinct personalities", category: "NLP", popularity: 87.0, connections: 36, monthly_users: 8000000, url: "https://character.ai", rank: 10 },
  { id: 11, name: "Stable Diffusion", description: "Open-source image generation model", category: "COMPUTER_VISION", popularity: 85.0, connections: 34, monthly_users: 5000000, url: "https://stability.ai", rank: 11 },
  { id: 12, name: "GitHub Copilot", description: "AI coding assistant", category: "CODING", popularity: 88.0, connections: 39, monthly_users: 10000000, url: "https://github.com/features/copilot", rank: 12 },
  { id: 13, name: "ElevenLabs", description: "AI voice synthesis", category: "AUDIO", popularity: 84.0, connections: 28, monthly_users: 2000000, url: "https://elevenlabs.io", rank: 13 },
  { id: 14, name: "Suno AI", description: "AI music generation from text prompts", category: "AUDIO", popularity: 84.0, connections: 26, monthly_users: 2500000, url: "https://suno.ai", rank: 14 },
  { id: 15, name: "Runway ML", description: "AI video and image editing", category: "VIDEO", popularity: 82.0, connections: 30, monthly_users: 1800000, url: "https://runwayml.com", rank: 15 },
  { id: 16, name: "Poe", description: "AI chatbot platform by Quora with multiple models", category: "NLP", popularity: 85.0, connections: 32, monthly_users: 5000000, url: "https://poe.com", rank: 16 },
  { id: 17, name: "Luma AI", description: "AI 3D scene generation and video creation", category: "COMPUTER_VISION", popularity: 83.0, connections: 25, monthly_users: 1000000, url: "https://lumalabs.ai", rank: 17 },
  { id: 18, name: "Jasper", description: "AI content writing platform", category: "BUSINESS", popularity: 81.0, connections: 27, monthly_users: 1500000, url: "https://jasper.ai", rank: 18 },
  { id: 19, name: "Copy.ai", description: "AI copywriting tool", category: "BUSINESS", popularity: 79.0, connections: 24, monthly_users: 1200000, url: "https://copy.ai", rank: 19 },
  { id: 20, name: "Perplexity", description: "AI-powered search engine", category: "NLP", popularity: 86.0, connections: 33, monthly_users: 4000000, url: "https://perplexity.ai", rank: 20 },

  // Second tier - Popular tools (21-50)
  { id: 21, name: "Gemini", description: "Google's advanced AI model", category: "NLP", popularity: 85.0, connections: 35, monthly_users: 25000000, url: "https://gemini.google.com", rank: 21 },
  { id: 22, name: "Replicate", description: "Run open-source machine learning models", category: "OTHER", popularity: 78.0, connections: 22, monthly_users: 800000, url: "https://replicate.com", rank: 22 },
  { id: 23, name: "Hugging Face", description: "Open-source ML platform and model hub", category: "OTHER", popularity: 82.0, connections: 40, monthly_users: 2000000, url: "https://huggingface.co", rank: 23 },
  { id: 24, name: "Anthropic Claude API", description: "API access to Claude models", category: "NLP", popularity: 80.0, connections: 25, monthly_users: 1000000, url: "https://console.anthropic.com", rank: 24 },
  { id: 25, name: "OpenAI API", description: "API access to GPT models", category: "NLP", popularity: 83.0, connections: 30, monthly_users: 5000000, url: "https://platform.openai.com", rank: 25 },
  { id: 26, name: "Cohere", description: "Enterprise AI platform for language models", category: "NLP", popularity: 76.0, connections: 20, monthly_users: 500000, url: "https://cohere.ai", rank: 26 },
  { id: 27, name: "Writesonic", description: "AI writing assistant for content creation", category: "BUSINESS", popularity: 77.0, connections: 18, monthly_users: 900000, url: "https://writesonic.com", rank: 27 },
  { id: 28, name: "Grammarly", description: "AI-powered writing assistant", category: "PRODUCTIVITY", popularity: 84.0, connections: 25, monthly_users: 30000000, url: "https://grammarly.com", rank: 28 },
  { id: 29, name: "Notion AI", description: "AI-powered workspace and note-taking", category: "PRODUCTIVITY", popularity: 82.0, connections: 28, monthly_users: 20000000, url: "https://notion.so", rank: 29 },
  { id: 30, name: "Canva AI", description: "AI design tools within Canva platform", category: "COMPUTER_VISION", popularity: 81.0, connections: 26, monthly_users: 15000000, url: "https://canva.com", rank: 30 },
  { id: 31, name: "Adobe Firefly", description: "Adobe's AI creative suite", category: "COMPUTER_VISION", popularity: 80.0, connections: 24, monthly_users: 8000000, url: "https://firefly.adobe.com", rank: 31 },
  { id: 32, name: "Leonardo AI", description: "AI art generation platform", category: "COMPUTER_VISION", popularity: 79.0, connections: 23, monthly_users: 1200000, url: "https://leonardo.ai", rank: 32 },
  { id: 33, name: "Synthesia", description: "AI video generation with synthetic actors", category: "VIDEO", popularity: 78.0, connections: 21, monthly_users: 800000, url: "https://synthesia.io", rank: 33 },
  { id: 34, name: "Descript", description: "AI-powered audio and video editing", category: "AUDIO", popularity: 77.0, connections: 20, monthly_users: 600000, url: "https://descript.com", rank: 34 },
  { id: 35, name: "Murf", description: "AI voice generator for voiceovers", category: "AUDIO", popularity: 76.0, connections: 19, monthly_users: 500000, url: "https://murf.ai", rank: 35 },
  { id: 36, name: "Otter.ai", description: "AI meeting transcription and notes", category: "PRODUCTIVITY", popularity: 80.0, connections: 22, monthly_users: 2000000, url: "https://otter.ai", rank: 36 },
  { id: 37, name: "Tome", description: "AI presentation and storytelling tool", category: "PRODUCTIVITY", popularity: 75.0, connections: 18, monthly_users: 400000, url: "https://tome.app", rank: 37 },
  { id: 38, name: "Gamma", description: "AI presentation maker", category: "PRODUCTIVITY", popularity: 74.0, connections: 17, monthly_users: 350000, url: "https://gamma.app", rank: 38 },
  { id: 39, name: "Beautiful.AI", description: "AI-powered presentation design", category: "PRODUCTIVITY", popularity: 73.0, connections: 16, monthly_users: 300000, url: "https://beautiful.ai", rank: 39 },
  { id: 40, name: "Loom AI", description: "AI features in video messaging", category: "VIDEO", popularity: 76.0, connections: 20, monthly_users: 14000000, url: "https://loom.com", rank: 40 },
  { id: 41, name: "Figma AI", description: "AI design assistance in Figma", category: "COMPUTER_VISION", popularity: 78.0, connections: 25, monthly_users: 4000000, url: "https://figma.com", rank: 41 },
  { id: 42, name: "Framer AI", description: "AI website building in Framer", category: "CODING", popularity: 75.0, connections: 22, monthly_users: 1000000, url: "https://framer.com", rank: 42 },
  { id: 43, name: "Webflow AI", description: "AI features in Webflow website builder", category: "CODING", popularity: 74.0, connections: 21, monthly_users: 3500000, url: "https://webflow.com", rank: 43 },
  { id: 44, name: "Replit AI", description: "AI coding assistant in online IDE", category: "CODING", popularity: 77.0, connections: 24, monthly_users: 2000000, url: "https://replit.com", rank: 44 },
  { id: 45, name: "CodeT5", description: "Code generation and understanding AI", category: "CODING", popularity: 72.0, connections: 18, monthly_users: 250000, url: "https://github.com/salesforce/CodeT5", rank: 45 },
  { id: 46, name: "Tabnine", description: "AI code completion tool", category: "CODING", popularity: 76.0, connections: 23, monthly_users: 1000000, url: "https://tabnine.com", rank: 46 },
  { id: 47, name: "Codeium", description: "Free AI code acceleration toolkit", category: "CODING", popularity: 75.0, connections: 22, monthly_users: 500000, url: "https://codeium.com", rank: 47 },
  { id: 48, name: "Amazon CodeWhisperer", description: "AWS AI coding companion", category: "CODING", popularity: 73.0, connections: 20, monthly_users: 800000, url: "https://aws.amazon.com/codewhisperer", rank: 48 },
  { id: 49, name: "Sourcegraph Cody", description: "AI coding assistant for large codebases", category: "CODING", popularity: 71.0, connections: 19, monthly_users: 300000, url: "https://sourcegraph.com/cody", rank: 49 },
  { id: 50, name: "DeepL", description: "AI-powered translation service", category: "NLP", popularity: 82.0, connections: 26, monthly_users: 25000000, url: "https://deepl.com", rank: 50 },

  // Third tier - Specialized tools (51-100)
  { id: 51, name: "Krisp", description: "AI noise cancellation for calls", category: "AUDIO", popularity: 70.0, connections: 15, monthly_users: 2000000, url: "https://krisp.ai", rank: 51 },
  { id: 52, name: "Remove.bg", description: "AI background removal tool", category: "COMPUTER_VISION", popularity: 75.0, connections: 18, monthly_users: 5000000, url: "https://remove.bg", rank: 52 },
  { id: 53, name: "Upscale.media", description: "AI image upscaling service", category: "COMPUTER_VISION", popularity: 70.0, connections: 16, monthly_users: 800000, url: "https://upscale.media", rank: 53 },
  { id: 54, name: "Topaz Labs", description: "AI photo and video enhancement", category: "COMPUTER_VISION", popularity: 72.0, connections: 17, monthly_users: 600000, url: "https://topazlabs.com", rank: 54 },
  { id: 55, name: "Luminar AI", description: "AI photo editing software", category: "COMPUTER_VISION", popularity: 71.0, connections: 16, monthly_users: 1000000, url: "https://skylum.com/luminar-ai", rank: 55 },
  { id: 56, name: "Face Swap by Reface", description: "AI face swapping app", category: "COMPUTER_VISION", popularity: 68.0, connections: 14, monthly_users: 10000000, url: "https://reface.ai", rank: 56 },
  { id: 57, name: "FaceApp", description: "AI photo editing with filters", category: "COMPUTER_VISION", popularity: 69.0, connections: 15, monthly_users: 15000000, url: "https://faceapp.com", rank: 57 },
  { id: 58, name: "Prisma", description: "AI art filter application", category: "COMPUTER_VISION", popularity: 67.0, connections: 13, monthly_users: 8000000, url: "https://prisma-ai.com", rank: 58 },
  { id: 59, name: "RunwayML Gen-2", description: "Text-to-video generation", category: "VIDEO", popularity: 74.0, connections: 20, monthly_users: 500000, url: "https://runwayml.com/gen-2", rank: 59 },
  { id: 60, name: "Pika Labs", description: "AI video generation platform", category: "VIDEO", popularity: 72.0, connections: 18, monthly_users: 300000, url: "https://pika.art", rank: 60 },
  { id: 61, name: "Steve AI", description: "AI video creation platform", category: "VIDEO", popularity: 68.0, connections: 15, monthly_users: 200000, url: "https://steve.ai", rank: 61 },
  { id: 62, name: "Pictory", description: "AI video creation from text", category: "VIDEO", popularity: 69.0, connections: 16, monthly_users: 250000, url: "https://pictory.ai", rank: 62 },
  { id: 63, name: "Invideo AI", description: "AI-powered video editor", category: "VIDEO", popularity: 70.0, connections: 17, monthly_users: 1000000, url: "https://invideo.io", rank: 63 },
  { id: 64, name: "Fliki", description: "Text to video with AI voices", category: "VIDEO", popularity: 68.0, connections: 15, monthly_users: 180000, url: "https://fliki.ai", rank: 64 },
  { id: 65, name: "Speechify", description: "AI text-to-speech reader", category: "AUDIO", popularity: 75.0, connections: 19, monthly_users: 20000000, url: "https://speechify.com", rank: 65 },
  { id: 66, name: "Voice.ai", description: "Real-time AI voice changer", category: "AUDIO", popularity: 67.0, connections: 14, monthly_users: 1500000, url: "https://voice.ai", rank: 66 },
  { id: 67, name: "Resemble AI", description: "AI voice cloning platform", category: "AUDIO", popularity: 69.0, connections: 16, monthly_users: 100000, url: "https://resembleai.com", rank: 67 },
  { id: 68, name: "Podcastle", description: "AI podcast creation platform", category: "AUDIO", popularity: 66.0, connections: 13, monthly_users: 150000, url: "https://podcastle.ai", rank: 68 },
  { id: 69, name: "Soundraw", description: "AI music composition tool", category: "AUDIO", popularity: 68.0, connections: 15, monthly_users: 200000, url: "https://soundraw.io", rank: 69 },
  { id: 70, name: "Amper Music", description: "AI music creation platform", category: "AUDIO", popularity: 65.0, connections: 12, monthly_users: 80000, url: "https://ampermusic.com", rank: 70 },
  { id: 71, name: "AIVA", description: "AI music composition assistant", category: "AUDIO", popularity: 67.0, connections: 14, monthly_users: 100000, url: "https://aiva.ai", rank: 71 },
  { id: 72, name: "Boomy", description: "AI music generation platform", category: "AUDIO", popularity: 66.0, connections: 13, monthly_users: 500000, url: "https://boomy.com", rank: 72 },
  { id: 73, name: "Endel", description: "AI adaptive music for focus", category: "AUDIO", popularity: 64.0, connections: 11, monthly_users: 2000000, url: "https://endel.io", rank: 73 },
  { id: 74, name: "Brain.fm", description: "AI music for cognitive enhancement", category: "AUDIO", popularity: 63.0, connections: 10, monthly_users: 800000, url: "https://brain.fm", rank: 74 },
  { id: 75, name: "Rytr", description: "AI writing assistant for content", category: "BUSINESS", popularity: 72.0, connections: 18, monthly_users: 7000000, url: "https://rytr.me", rank: 75 },
  { id: 76, name: "Wordtune", description: "AI writing companion and rewriter", category: "BUSINESS", popularity: 73.0, connections: 19, monthly_users: 1000000, url: "https://wordtune.com", rank: 76 },
  { id: 77, name: "Quillbot", description: "AI paraphrasing and grammar checker", category: "BUSINESS", popularity: 74.0, connections: 20, monthly_users: 50000000, url: "https://quillbot.com", rank: 77 },
  { id: 78, name: "Surfer SEO", description: "AI content optimization for SEO", category: "BUSINESS", popularity: 71.0, connections: 17, monthly_users: 500000, url: "https://surferseo.com", rank: 78 },
  { id: 79, name: "MarketMuse", description: "AI content planning and optimization", category: "BUSINESS", popularity: 68.0, connections: 15, monthly_users: 50000, url: "https://marketmuse.com", rank: 79 },
  { id: 80, name: "Frase", description: "AI content optimization tool", category: "BUSINESS", popularity: 69.0, connections: 16, monthly_users: 100000, url: "https://frase.io", rank: 80 },
  { id: 81, name: "ContentKing", description: "AI SEO monitoring platform", category: "BUSINESS", popularity: 66.0, connections: 13, monthly_users: 30000, url: "https://contentkingapp.com", rank: 81 },
  { id: 82, name: "Clearscope", description: "AI content optimization for search", category: "BUSINESS", popularity: 67.0, connections: 14, monthly_users: 25000, url: "https://clearscope.io", rank: 82 },
  { id: 83, name: "Anyword", description: "AI copywriting optimization", category: "BUSINESS", popularity: 68.0, connections: 15, monthly_users: 200000, url: "https://anyword.com", rank: 83 },
  { id: 84, name: "Persado", description: "AI-powered marketing language", category: "BUSINESS", popularity: 65.0, connections: 12, monthly_users: 10000, url: "https://persado.com", rank: 84 },
  { id: 85, name: "Phrasee", description: "AI email marketing copy", category: "BUSINESS", popularity: 64.0, connections: 11, monthly_users: 5000, url: "https://phrasee.co", rank: 85 },
  { id: 86, name: "Smartly.io", description: "AI social media advertising", category: "BUSINESS", popularity: 70.0, connections: 17, monthly_users: 800000, url: "https://smartly.io", rank: 86 },
  { id: 87, name: "Albert AI", description: "AI digital marketing platform", category: "BUSINESS", popularity: 66.0, connections: 13, monthly_users: 50000, url: "https://albert.ai", rank: 87 },
  { id: 88, name: "Seventh Sense", description: "AI email delivery optimization", category: "BUSINESS", popularity: 63.0, connections: 10, monthly_users: 20000, url: "https://seventhsense.com", rank: 88 },
  { id: 89, name: "Mailchimp AI", description: "AI features in email marketing", category: "BUSINESS", popularity: 75.0, connections: 21, monthly_users: 12000000, url: "https://mailchimp.com", rank: 89 },
  { id: 90, name: "HubSpot AI", description: "AI tools in HubSpot CRM", category: "BUSINESS", popularity: 76.0, connections: 22, monthly_users: 5000000, url: "https://hubspot.com", rank: 90 },
  { id: 91, name: "Salesforce Einstein", description: "AI integrated into Salesforce", category: "BUSINESS", popularity: 78.0, connections: 25, monthly_users: 150000, url: "https://salesforce.com/products/einstein", rank: 91 },
  { id: 92, name: "Zendesk AI", description: "AI customer service tools", category: "BUSINESS", popularity: 74.0, connections: 20, monthly_users: 100000, url: "https://zendesk.com", rank: 92 },
  { id: 93, name: "Intercom AI", description: "AI customer messaging platform", category: "BUSINESS", popularity: 73.0, connections: 19, monthly_users: 25000, url: "https://intercom.com", rank: 93 },
  { id: 94, name: "Drift AI", description: "AI conversational marketing", category: "BUSINESS", popularity: 71.0, connections: 17, monthly_users: 5000, url: "https://drift.com", rank: 94 },
  { id: 95, name: "Ada", description: "AI chatbot platform", category: "BUSINESS", popularity: 69.0, connections: 15, monthly_users: 1000, url: "https://ada.cx", rank: 95 },
  { id: 96, name: "LivePerson", description: "AI conversational cloud", category: "BUSINESS", popularity: 68.0, connections: 14, monthly_users: 18000, url: "https://liveperson.com", rank: 96 },
  { id: 97, name: "MonkeyLearn", description: "AI text analysis platform", category: "NLP", popularity: 66.0, connections: 13, monthly_users: 50000, url: "https://monkeylearn.com", rank: 97 },
  { id: 98, name: "Lexalytics", description: "AI text analytics engine", category: "NLP", popularity: 64.0, connections: 11, monthly_users: 10000, url: "https://lexalytics.com", rank: 98 },
  { id: 99, name: "Aylien", description: "AI text analysis API", category: "NLP", popularity: 63.0, connections: 10, monthly_users: 5000, url: "https://aylien.com", rank: 99 },
  { id: 100, name: "MeaningCloud", description: "AI text analytics service", category: "NLP", popularity: 62.0, connections: 9, monthly_users: 15000, url: "https://meaningcloud.com", rank: 100 },

  // Fourth tier - Emerging/Specialized (101-200)
  { id: 101, name: "Weights & Biases", description: "AI experiment tracking platform", category: "OTHER", popularity: 70.0, connections: 16, monthly_users: 200000, url: "https://wandb.ai", rank: 101 },
  { id: 102, name: "Neptune.ai", description: "ML experiment management", category: "OTHER", popularity: 65.0, connections: 12, monthly_users: 50000, url: "https://neptune.ai", rank: 102 },
  { id: 103, name: "MLflow", description: "Open source ML lifecycle management", category: "OTHER", popularity: 68.0, connections: 15, monthly_users: 100000, url: "https://mlflow.org", rank: 103 },
  { id: 104, name: "Comet ML", description: "ML experiment tracking", category: "OTHER", popularity: 64.0, connections: 11, monthly_users: 30000, url: "https://comet.ml", rank: 104 },
  { id: 105, name: "TensorBoard", description: "TensorFlow visualization toolkit", category: "OTHER", popularity: 72.0, connections: 18, monthly_users: 500000, url: "https://tensorflow.org/tensorboard", rank: 105 },
  { id: 106, name: "Paperspace", description: "Cloud ML development platform", category: "OTHER", popularity: 66.0, connections: 13, monthly_users: 100000, url: "https://paperspace.com", rank: 106 },
  { id: 107, name: "FloydHub", description: "Cloud platform for deep learning", category: "OTHER", popularity: 60.0, connections: 8, monthly_users: 5000, url: "https://floydhub.com", rank: 107 },
  { id: 108, name: "Google Colab", description: "Free cloud-based Jupyter notebooks", category: "OTHER", popularity: 85.0, connections: 30, monthly_users: 10000000, url: "https://colab.research.google.com", rank: 108 },
  { id: 109, name: "Kaggle", description: "Data science competition platform", category: "OTHER", popularity: 80.0, connections: 25, monthly_users: 5000000, url: "https://kaggle.com", rank: 109 },
  { id: 110, name: "DataRobot", description: "Automated machine learning platform", category: "OTHER", popularity: 72.0, connections: 18, monthly_users: 50000, url: "https://datarobot.com", rank: 110 },
  { id: 111, name: "H2O.ai", description: "Open source machine learning platform", category: "OTHER", popularity: 70.0, connections: 16, monthly_users: 100000, url: "https://h2o.ai", rank: 111 },
  { id: 112, name: "AutoML", description: "Automated machine learning by Google", category: "OTHER", popularity: 68.0, connections: 15, monthly_users: 20000, url: "https://cloud.google.com/automl", rank: 112 },
  { id: 113, name: "Azure ML", description: "Microsoft Azure machine learning", category: "OTHER", popularity: 74.0, connections: 20, monthly_users: 100000, url: "https://azure.microsoft.com/en-us/services/machine-learning", rank: 113 },
  { id: 114, name: "AWS SageMaker", description: "Amazon's ML platform", category: "OTHER", popularity: 76.0, connections: 22, monthly_users: 150000, url: "https://aws.amazon.com/sagemaker", rank: 114 },
  { id: 115, name: "IBM Watson", description: "IBM's AI platform", category: "OTHER", popularity: 71.0, connections: 17, monthly_users: 80000, url: "https://ibm.com/watson", rank: 115 },
  { id: 116, name: "Vertex AI", description: "Google Cloud ML platform", category: "OTHER", popularity: 69.0, connections: 15, monthly_users: 50000, url: "https://cloud.google.com/vertex-ai", rank: 116 },
  { id: 117, name: "Algorithmia", description: "Algorithm marketplace and hosting", category: "OTHER", popularity: 62.0, connections: 9, monthly_users: 10000, url: "https://algorithmia.com", rank: 117 },
  { id: 118, name: "Spell", description: "Deep learning infrastructure", category: "OTHER", popularity: 58.0, connections: 6, monthly_users: 2000, url: "https://spell.ml", rank: 118 },
  { id: 119, name: "Determined AI", description: "Deep learning training platform", category: "OTHER", popularity: 61.0, connections: 8, monthly_users: 5000, url: "https://determined.ai", rank: 119 },
  { id: 120, name: "Domino Data Lab", description: "Data science platform", category: "OTHER", popularity: 65.0, connections: 12, monthly_users: 15000, url: "https://dominodatalab.com", rank: 120 },
  { id: 121, name: "Dataiku", description: "Data science platform", category: "OTHER", popularity: 67.0, connections: 14, monthly_users: 25000, url: "https://dataiku.com", rank: 121 },
  { id: 122, name: "Palantir", description: "Big data analytics platform", category: "OTHER", popularity: 70.0, connections: 16, monthly_users: 10000, url: "https://palantir.com", rank: 122 },
  { id: 123, name: "Tableau AI", description: "AI features in data visualization", category: "PRODUCTIVITY", popularity: 73.0, connections: 19, monthly_users: 1000000, url: "https://tableau.com", rank: 123 },
  { id: 124, name: "Power BI AI", description: "Microsoft's AI-powered BI tool", category: "PRODUCTIVITY", popularity: 74.0, connections: 20, monthly_users: 5000000, url: "https://powerbi.microsoft.com", rank: 124 },
  { id: 125, name: "Qlik Sense AI", description: "AI-powered analytics platform", category: "PRODUCTIVITY", popularity: 68.0, connections: 15, monthly_users: 500000, url: "https://qlik.com", rank: 125 },
  { id: 126, name: "Looker AI", description: "Google's AI business intelligence", category: "PRODUCTIVITY", popularity: 66.0, connections: 13, monthly_users: 100000, url: "https://looker.com", rank: 126 },
  { id: 127, name: "Sisense AI", description: "AI-driven analytics platform", category: "PRODUCTIVITY", popularity: 64.0, connections: 11, monthly_users: 50000, url: "https://sisense.com", rank: 127 },
  { id: 128, name: "Domo AI", description: "Cloud business intelligence with AI", category: "PRODUCTIVITY", popularity: 65.0, connections: 12, monthly_users: 25000, url: "https://domo.com", rank: 128 },
  { id: 129, name: "ThoughtSpot", description: "Search-driven analytics platform", category: "PRODUCTIVITY", popularity: 67.0, connections: 14, monthly_users: 30000, url: "https://thoughtspot.com", rank: 129 },
  { id: 130, name: "Alteryx AI", description: "AI-powered data analytics", category: "PRODUCTIVITY", popularity: 69.0, connections: 16, monthly_users: 100000, url: "https://alteryx.com", rank: 130 },
  { id: 131, name: "Knime", description: "Open source data analytics platform", category: "PRODUCTIVITY", popularity: 66.0, connections: 13, monthly_users: 200000, url: "https://knime.com", rank: 131 },
  { id: 132, name: "RapidMiner", description: "Data science platform", category: "PRODUCTIVITY", popularity: 64.0, connections: 11, monthly_users: 50000, url: "https://rapidminer.com", rank: 132 },
  { id: 133, name: "Orange", description: "Open source machine learning toolkit", category: "PRODUCTIVITY", popularity: 62.0, connections: 9, monthly_users: 100000, url: "https://orangedatamining.com", rank: 133 },
  { id: 134, name: "Weka", description: "Machine learning workbench", category: "PRODUCTIVITY", popularity: 60.0, connections: 8, monthly_users: 50000, url: "https://waikato.github.io/weka-wiki", rank: 134 },
  { id: 135, name: "R Studio AI", description: "AI features in R development", category: "PRODUCTIVITY", popularity: 70.0, connections: 17, monthly_users: 2000000, url: "https://rstudio.com", rank: 135 },
  { id: 136, name: "Jupyter AI", description: "AI extensions for Jupyter", category: "PRODUCTIVITY", popularity: 71.0, connections: 18, monthly_users: 8000000, url: "https://jupyter.org", rank: 136 },
  { id: 137, name: "Observable AI", description: "AI-powered data visualization", category: "PRODUCTIVITY", popularity: 63.0, connections: 10, monthly_users: 100000, url: "https://observablehq.com", rank: 137 },
  { id: 138, name: "Streamlit", description: "AI app development framework", category: "CODING", popularity: 72.0, connections: 19, monthly_users: 1000000, url: "https://streamlit.io", rank: 138 },
  { id: 139, name: "Gradio", description: "ML model interface builder", category: "CODING", popularity: 68.0, connections: 15, monthly_users: 200000, url: "https://gradio.app", rank: 139 },
  { id: 140, name: "FastAPI", description: "High-performance API framework", category: "CODING", popularity: 75.0, connections: 22, monthly_users: 5000000, url: "https://fastapi.tiangolo.com", rank: 140 },
  { id: 141, name: "Flask-AI", description: "AI extensions for Flask", category: "CODING", popularity: 65.0, connections: 12, monthly_users: 1000000, url: "https://flask.palletsprojects.com", rank: 141 },
  { id: 142, name: "Django AI", description: "AI tools for Django framework", category: "CODING", popularity: 67.0, connections: 14, monthly_users: 2000000, url: "https://djangoproject.com", rank: 142 },
  { id: 143, name: "TensorFlow.js", description: "Machine learning for JavaScript", category: "CODING", popularity: 73.0, connections: 20, monthly_users: 1000000, url: "https://tensorflow.org/js", rank: 143 },
  { id: 144, name: "PyTorch Lightning", description: "High-level PyTorch framework", category: "CODING", popularity: 71.0, connections: 18, monthly_users: 500000, url: "https://pytorchlightning.ai", rank: 144 },
  { id: 145, name: "Keras", description: "High-level neural networks API", category: "CODING", popularity: 78.0, connections: 25, monthly_users: 2000000, url: "https://keras.io", rank: 145 },
  { id: 146, name: "Scikit-learn", description: "Machine learning library for Python", category: "CODING", popularity: 82.0, connections: 30, monthly_users: 5000000, url: "https://scikit-learn.org", rank: 146 },
  { id: 147, name: "XGBoost", description: "Gradient boosting framework", category: "CODING", popularity: 75.0, connections: 22, monthly_users: 1000000, url: "https://xgboost.readthedocs.io", rank: 147 },
  { id: 148, name: "LightGBM", description: "Gradient boosting framework", category: "CODING", popularity: 72.0, connections: 19, monthly_users: 500000, url: "https://lightgbm.readthedocs.io", rank: 148 },
  { id: 149, name: "CatBoost", description: "Gradient boosting library", category: "CODING", popularity: 68.0, connections: 15, monthly_users: 200000, url: "https://catboost.ai", rank: 149 },
  { id: 150, name: "Prophet", description: "Time series forecasting tool", category: "CODING", popularity: 66.0, connections: 13, monthly_users: 300000, url: "https://facebook.github.io/prophet", rank: 150 },
  { id: 151, name: "Detectron2", description: "Object detection platform", category: "COMPUTER_VISION", popularity: 70.0, connections: 17, monthly_users: 100000, url: "https://detectron2.readthedocs.io", rank: 151 },
  { id: 152, name: "YOLO", description: "Real-time object detection", category: "COMPUTER_VISION", popularity: 74.0, connections: 21, monthly_users: 500000, url: "https://pjreddie.com/darknet/yolo", rank: 152 },
  { id: 153, name: "OpenCV", description: "Computer vision library", category: "COMPUTER_VISION", popularity: 80.0, connections: 28, monthly_users: 2000000, url: "https://opencv.org", rank: 153 },
  { id: 154, name: "MediaPipe", description: "ML solutions for live perception", category: "COMPUTER_VISION", popularity: 72.0, connections: 19, monthly_users: 300000, url: "https://mediapipe.dev", rank: 154 },
  { id: 155, name: "DeepFace", description: "Face recognition framework", category: "COMPUTER_VISION", popularity: 68.0, connections: 15, monthly_users: 200000, url: "https://github.com/serengil/deepface", rank: 155 },
  { id: 156, name: "FaceNet", description: "Face recognition system", category: "COMPUTER_VISION", popularity: 66.0, connections: 13, monthly_users: 100000, url: "https://github.com/davidsandberg/facenet", rank: 156 },
  { id: 157, name: "InsightFace", description: "Face analysis toolkit", category: "COMPUTER_VISION", popularity: 64.0, connections: 11, monthly_users: 50000, url: "https://insightface.ai", rank: 157 },
  { id: 158, name: "Dlib", description: "Machine learning toolkit", category: "COMPUTER_VISION", popularity: 70.0, connections: 17, monthly_users: 500000, url: "http://dlib.net", rank: 158 },
  { id: 159, name: "ImageAI", description: "Computer vision made easy", category: "COMPUTER_VISION", popularity: 66.0, connections: 13, monthly_users: 100000, url: "https://imageai.org", rank: 159 },
  { id: 160, name: "PaddlePaddle", description: "Deep learning platform", category: "CODING", popularity: 65.0, connections: 12, monthly_users: 200000, url: "https://paddlepaddle.org", rank: 160 },
  { id: 161, name: "MXNet", description: "Flexible deep learning framework", category: "CODING", popularity: 62.0, connections: 9, monthly_users: 50000, url: "https://mxnet.apache.org", rank: 161 },
  { id: 162, name: "Caffe", description: "Deep learning framework", category: "CODING", popularity: 60.0, connections: 8, monthly_users: 30000, url: "http://caffe.berkeleyvision.org", rank: 162 },
  { id: 163, name: "Theano", description: "Mathematical expressions compiler", category: "CODING", popularity: 58.0, connections: 6, monthly_users: 20000, url: "http://deeplearning.net/software/theano", rank: 163 },
  { id: 164, name: "CNTK", description: "Microsoft Cognitive Toolkit", category: "CODING", popularity: 56.0, connections: 5, monthly_users: 10000, url: "https://docs.microsoft.com/en-us/cognitive-toolkit", rank: 164 },
  { id: 165, name: "Chainer", description: "Flexible deep learning framework", category: "CODING", popularity: 54.0, connections: 4, monthly_users: 5000, url: "https://chainer.org", rank: 165 },
  { id: 166, name: "DyNet", description: "Dynamic neural network toolkit", category: "CODING", popularity: 52.0, connections: 3, monthly_users: 2000, url: "https://dynet.readthedocs.io", rank: 166 },
  { id: 167, name: "JAX", description: "NumPy-compatible ML research", category: "CODING", popularity: 69.0, connections: 16, monthly_users: 200000, url: "https://jax.readthedocs.io", rank: 167 },
  { id: 168, name: "Flax", description: "Neural network library for JAX", category: "CODING", popularity: 64.0, connections: 11, monthly_users: 50000, url: "https://flax.readthedocs.io", rank: 168 },
  { id: 169, name: "Haiku", description: "Neural network library for JAX", category: "CODING", popularity: 62.0, connections: 9, monthly_users: 30000, url: "https://dm-haiku.readthedocs.io", rank: 169 },
  { id: 170, name: "Optax", description: "Gradient processing library", category: "CODING", popularity: 60.0, connections: 8, monthly_users: 20000, url: "https://optax.readthedocs.io", rank: 170 },
  { id: 171, name: "Whisper", description: "OpenAI's speech recognition", category: "AUDIO", popularity: 78.0, connections: 25, monthly_users: 1000000, url: "https://openai.com/research/whisper", rank: 171 },
  { id: 172, name: "Wav2Vec", description: "Facebook's speech representation", category: "AUDIO", popularity: 70.0, connections: 17, monthly_users: 100000, url: "https://ai.facebook.com/blog/wav2vec-20", rank: 172 },
  { id: 173, name: "DeepSpeech", description: "Mozilla's speech recognition", category: "AUDIO", popularity: 68.0, connections: 15, monthly_users: 50000, url: "https://deepspeech.readthedocs.io", rank: 173 },
  { id: 174, name: "Kaldi", description: "Speech recognition toolkit", category: "AUDIO", popularity: 66.0, connections: 13, monthly_users: 30000, url: "https://kaldi-asr.org", rank: 174 },
  { id: 175, name: "ESPnet", description: "End-to-end speech processing", category: "AUDIO", popularity: 64.0, connections: 11, monthly_users: 20000, url: "https://espnet.github.io/espnet", rank: 175 },
  { id: 176, name: "SpeechBrain", description: "Speech processing toolkit", category: "AUDIO", popularity: 62.0, connections: 9, monthly_users: 15000, url: "https://speechbrain.github.io", rank: 176 },
  { id: 177, name: "Fairseq", description: "Sequence modeling toolkit", category: "NLP", popularity: 70.0, connections: 17, monthly_users: 200000, url: "https://fairseq.readthedocs.io", rank: 177 },
  { id: 178, name: "Transformers", description: "State-of-the-art NLP library", category: "NLP", popularity: 85.0, connections: 35, monthly_users: 5000000, url: "https://huggingface.co/transformers", rank: 178 },
  { id: 179, name: "spaCy", description: "Industrial-strength NLP", category: "NLP", popularity: 80.0, connections: 28, monthly_users: 2000000, url: "https://spacy.io", rank: 179 },
  { id: 180, name: "NLTK", description: "Natural language toolkit", category: "NLP", popularity: 78.0, connections: 26, monthly_users: 3000000, url: "https://nltk.org", rank: 180 },
  { id: 181, name: "Gensim", description: "Topic modeling and similarity", category: "NLP", popularity: 72.0, connections: 19, monthly_users: 500000, url: "https://radimrehurek.com/gensim", rank: 181 },
  { id: 182, name: "AllenNLP", description: "NLP research library", category: "NLP", popularity: 68.0, connections: 15, monthly_users: 100000, url: "https://allennlp.org", rank: 182 },
  { id: 183, name: "Flair", description: "NLP framework", category: "NLP", popularity: 66.0, connections: 13, monthly_users: 200000, url: "https://flairnlp.github.io", rank: 183 },
  { id: 184, name: "TextBlob", description: "Simple text processing", category: "NLP", popularity: 70.0, connections: 17, monthly_users: 1000000, url: "https://textblob.readthedocs.io", rank: 184 },
  { id: 185, name: "StanfordNLP", description: "Stanford NLP toolkit", category: "NLP", popularity: 74.0, connections: 21, monthly_users: 300000, url: "https://stanfordnlp.github.io/stanza", rank: 185 },
  { id: 186, name: "CoreNLP", description: "Stanford's NLP toolkit", category: "NLP", popularity: 72.0, connections: 19, monthly_users: 200000, url: "https://stanfordnlp.github.io/CoreNLP", rank: 186 },
  { id: 187, name: "OpenNMT", description: "Neural machine translation", category: "NLP", popularity: 66.0, connections: 13, monthly_users: 50000, url: "https://opennmt.net", rank: 187 },
  { id: 188, name: "MarianMT", description: "Neural machine translation", category: "NLP", popularity: 64.0, connections: 11, monthly_users: 30000, url: "https://marian-nmt.github.io", rank: 188 },
  { id: 189, name: "Moses", description: "Statistical machine translation", category: "NLP", popularity: 60.0, connections: 8, monthly_users: 10000, url: "http://statmt.org/moses", rank: 189 },
  { id: 190, name: "FastText", description: "Efficient text classification", category: "NLP", popularity: 74.0, connections: 21, monthly_users: 1000000, url: "https://fasttext.cc", rank: 190 },
  { id: 191, name: "Word2Vec", description: "Word embeddings toolkit", category: "NLP", popularity: 76.0, connections: 23, monthly_users: 2000000, url: "https://code.google.com/archive/p/word2vec", rank: 191 },
  { id: 192, name: "GloVe", description: "Global vectors for word representation", category: "NLP", popularity: 72.0, connections: 19, monthly_users: 500000, url: "https://nlp.stanford.edu/projects/glove", rank: 192 },
  { id: 193, name: "BERT", description: "Bidirectional transformer", category: "NLP", popularity: 82.0, connections: 30, monthly_users: 3000000, url: "https://github.com/google-research/bert", rank: 193 },
  { id: 194, name: "RoBERTa", description: "Robustly optimized BERT", category: "NLP", popularity: 78.0, connections: 26, monthly_users: 1000000, url: "https://github.com/pytorch/fairseq/tree/master/examples/roberta", rank: 194 },
  { id: 195, name: "GPT-2", description: "Generative pre-trained transformer", category: "NLP", popularity: 80.0, connections: 28, monthly_users: 2000000, url: "https://openai.com/research/better-language-models", rank: 195 },
  { id: 196, name: "T5", description: "Text-to-text transfer transformer", category: "NLP", popularity: 76.0, connections: 24, monthly_users: 500000, url: "https://github.com/google-research/text-to-text-transfer-transformer", rank: 196 },
  { id: 197, name: "ELECTRA", description: "Efficiently learning encoder", category: "NLP", popularity: 72.0, connections: 20, monthly_users: 200000, url: "https://github.com/google-research/electra", rank: 197 },
  { id: 198, name: "DeBERTa", description: "Decoding-enhanced BERT", category: "NLP", popularity: 70.0, connections: 18, monthly_users: 100000, url: "https://github.com/microsoft/DeBERTa", rank: 198 },
  { id: 199, name: "ALBERT", description: "A lite BERT", category: "NLP", popularity: 68.0, connections: 16, monthly_users: 150000, url: "https://github.com/google-research/albert", rank: 199 },
  { id: 200, name: "DistilBERT", description: "Distilled version of BERT", category: "NLP", popularity: 74.0, connections: 22, monthly_users: 800000, url: "https://github.com/huggingface/transformers/tree/master/examples/distillation", rank: 200 }
];

// Generate synergy connections for 200 nodes
export const SYNERGIES_MOCK = [
  // Top tier connections (1-20)
  { source: 1, target: 3, strength: 0.9, type: 'complementary', description: 'Both leading conversational AI assistants with different strengths' },
  { source: 1, target: 21, strength: 0.85, type: 'competitive', description: 'Competing conversational AI platforms from OpenAI and Google' },
  { source: 2, target: 4, strength: 0.8, type: 'complementary', description: 'Full-stack development platform pairs well with AI-powered code editor' },
  { source: 2, target: 6, strength: 0.9, type: 'competitive', description: 'Both are AI website builders competing in the same space' },
  { source: 2, target: 8, strength: 0.85, type: 'functional', description: 'Bolt.new for full apps, V0 for React components - workflow integration' },
  { source: 4, target: 12, strength: 0.9, type: 'complementary', description: 'Cursor editor works excellently with GitHub Copilot suggestions' },
  { source: 5, target: 7, strength: 0.9, type: 'competitive', description: 'Leading image generation platforms with different approaches' },
  { source: 5, target: 11, strength: 0.85, type: 'competitive', description: 'Midjourney vs Stable Diffusion - commercial vs open source' },
  { source: 7, target: 11, strength: 0.8, type: 'competitive', description: 'DALL-E vs Stable Diffusion in AI image generation' },
  { source: 8, target: 12, strength: 0.7, type: 'functional', description: 'V0 components can be enhanced with Copilot suggestions' },
  { source: 6, target: 8, strength: 0.8, type: 'competitive', description: 'Lovable vs V0 - both generate web components' },
  { source: 13, target: 14, strength: 0.8, type: 'complementary', description: 'Voice synthesis pairs well with AI music generation' },
  { source: 1, target: 13, strength: 0.6, type: 'workflow', description: 'ChatGPT text can be converted to speech with ElevenLabs' },
  { source: 18, target: 19, strength: 0.9, type: 'competitive', description: 'Both AI copywriting platforms targeting similar markets' },
  { source: 1, target: 9, strength: 0.8, type: 'functional', description: 'ChatGPT and NotebookLM both excel at research assistance' },
  { source: 3, target: 10, strength: 0.7, type: 'functional', description: 'Claude and Character.AI both focus on conversational AI' },
  { source: 16, target: 10, strength: 0.8, type: 'complementary', description: 'Poe platform includes Character.AI-style bots' },
  { source: 20, target: 1, strength: 0.7, type: 'functional', description: 'Perplexity search complements ChatGPT conversations' },
  { source: 15, target: 5, strength: 0.6, type: 'functional', description: 'Runway video editing enhanced with Midjourney images' },
  { source: 17, target: 5, strength: 0.6, type: 'functional', description: 'Luma 3D generation works with Midjourney for textures' },

  // Second tier connections (21-50)
  { source: 25, target: 1, strength: 0.95, type: 'complementary', description: 'OpenAI API provides programmatic access to ChatGPT capabilities' },
  { source: 24, target: 3, strength: 0.95, type: 'complementary', description: 'Claude API enables integration of Claude in applications' },
  { source: 23, target: 178, strength: 0.9, type: 'complementary', description: 'Hugging Face hosts and distributes Transformers library' },
  { source: 28, target: 29, strength: 0.7, type: 'functional', description: 'Grammarly and Notion AI both enhance writing workflows' },
  { source: 30, target: 31, strength: 0.8, type: 'competitive', description: 'Canva AI vs Adobe Firefly in AI-powered design tools' },
  { source: 32, target: 5, strength: 0.85, type: 'competitive', description: 'Leonardo AI competes with Midjourney in AI art generation' },
  { source: 33, target: 15, strength: 0.8, type: 'competitive', description: 'Synthesia vs Runway in AI video generation space' },
  { source: 34, target: 13, strength: 0.7, type: 'functional', description: 'Descript audio editing enhanced with ElevenLabs voices' },
  { source: 35, target: 13, strength: 0.85, type: 'competitive', description: 'Murf vs ElevenLabs in AI voice generation market' },
  { source: 36, target: 9, strength: 0.7, type: 'functional', description: 'Otter.ai and NotebookLM both process meeting content' },
  { source: 42, target: 43, strength: 0.8, type: 'competitive', description: 'Framer AI vs Webflow AI in AI website building' },
  { source: 44, target: 12, strength: 0.8, type: 'competitive', description: 'Replit AI vs GitHub Copilot in cloud-based AI coding' },
  { source: 46, target: 47, strength: 0.85, type: 'competitive', description: 'Tabnine vs Codeium in AI code completion' },
  { source: 48, target: 12, strength: 0.7, type: 'competitive', description: 'AWS CodeWhisperer vs GitHub Copilot in enterprise' },
  { source: 49, target: 12, strength: 0.6, type: 'competitive', description: 'Sourcegraph Cody vs GitHub Copilot for large codebases' },
  { source: 50, target: 1, strength: 0.6, type: 'functional', description: 'DeepL translation enhances ChatGPT multilingual capabilities' },

  // Framework and library connections (140-200)
  { source: 145, target: 146, strength: 0.9, type: 'complementary', description: 'Keras high-level API often used with scikit-learn for complete ML pipelines' },
  { source: 178, target: 179, strength: 0.8, type: 'complementary', description: 'Transformers library integrates well with spaCy for NLP pipelines' },
  { source: 178, target: 180, strength: 0.7, type: 'functional', description: 'Transformers can be combined with NLTK for text preprocessing' },
  { source: 193, target: 178, strength: 0.95, type: 'complementary', description: 'BERT is available through Transformers library' },
  { source: 194, target: 178, strength: 0.9, type: 'complementary', description: 'RoBERTa model accessible via Transformers' },
  { source: 195, target: 178, strength: 0.9, type: 'complementary', description: 'GPT-2 implementation available in Transformers' },
  { source: 171, target: 172, strength: 0.8, type: 'competitive', description: 'Whisper vs Wav2Vec in speech recognition approaches' },
  { source: 171, target: 173, strength: 0.75, type: 'competitive', description: 'Whisper vs DeepSpeech in open-source speech recognition' },
  { source: 152, target: 151, strength: 0.8, type: 'competitive', description: 'YOLO vs Detectron2 in object detection frameworks' },
  { source: 153, target: 154, strength: 0.8, type: 'complementary', description: 'OpenCV often used with MediaPipe for computer vision' },

  // Cloud platform connections
  { source: 108, target: 109, strength: 0.8, type: 'complementary', description: 'Google Colab frequently used for Kaggle competitions' },
  { source: 114, target: 113, strength: 0.8, type: 'competitive', description: 'AWS SageMaker vs Azure ML in cloud ML platforms' },
  { source: 116, target: 114, strength: 0.7, type: 'competitive', description: 'Google Vertex AI vs AWS SageMaker' },
  { source: 115, target: 114, strength: 0.6, type: 'competitive', description: 'IBM Watson vs AWS SageMaker in enterprise AI' },

  // Business intelligence connections
  { source: 123, target: 124, strength: 0.85, type: 'competitive', description: 'Tableau vs Power BI in AI-powered data visualization' },
  { source: 125, target: 123, strength: 0.7, type: 'competitive', description: 'Qlik Sense vs Tableau in analytics platforms' },
  { source: 126, target: 124, strength: 0.6, type: 'competitive', description: 'Looker vs Power BI in business intelligence' },

  // Development framework connections
  { source: 138, target: 139, strength: 0.8, type: 'complementary', description: 'Streamlit and Gradio both create ML app interfaces' },
  { source: 140, target: 141, strength: 0.7, type: 'competitive', description: 'FastAPI vs Flask in Python web frameworks' },
  { source: 142, target: 141, strength: 0.6, type: 'competitive', description: 'Django vs Flask in web development' },
  { source: 143, target: 145, strength: 0.8, type: 'complementary', description: 'TensorFlow.js brings Keras models to browsers' },
  { source: 144, target: 145, strength: 0.7, type: 'functional', description: 'PyTorch Lightning simplifies PyTorch training loops' },

  // Gradient boosting family
  { source: 147, target: 148, strength: 0.9, type: 'competitive', description: 'XGBoost vs LightGBM in gradient boosting performance' },
  { source: 149, target: 147, strength: 0.8, type: 'competitive', description: 'CatBoost vs XGBoost in handling categorical features' },
  { source: 148, target: 149, strength: 0.8, type: 'competitive', description: 'LightGBM vs CatBoost in speed and accuracy' },

  // Cross-domain workflow connections
  { source: 2, target: 31, strength: 0.5, type: 'workflow', description: 'Bolt.new development enhanced with Adobe Firefly assets' },
  { source: 18, target: 30, strength: 0.7, type: 'workflow', description: 'Jasper content creation paired with Canva AI design' },
  { source: 19, target: 32, strength: 0.6, type: 'workflow', description: 'Copy.ai text with Leonardo AI generated images' },
  { source: 1, target: 35, strength: 0.6, type: 'workflow', description: 'ChatGPT scripts converted to voice with Murf' },
  { source: 9, target: 37, strength: 0.7, type: 'workflow', description: 'NotebookLM research presented using Tome' },
  { source: 20, target: 38, strength: 0.6, type: 'workflow', description: 'Perplexity research findings presented in Gamma' },

  // Additional synergies for comprehensive coverage
  { source: 75, target: 76, strength: 0.8, type: 'competitive', description: 'Rytr vs Wordtune in AI writing assistance' },
  { source: 77, target: 75, strength: 0.7, type: 'competitive', description: 'Quillbot vs Rytr in content rewriting' },
  { source: 89, target: 90, strength: 0.7, type: 'competitive', description: 'Mailchimp AI vs HubSpot AI in marketing automation' },
  { source: 91, target: 90, strength: 0.8, type: 'competitive', description: 'Salesforce Einstein vs HubSpot AI in CRM' },
  { source: 92, target: 93, strength: 0.8, type: 'competitive', description: 'Zendesk AI vs Intercom AI in customer service' },
  { source: 94, target: 95, strength: 0.7, type: 'competitive', description: 'Drift AI vs Ada in conversational marketing' },

  // Research and development connections
  { source: 101, target: 102, strength: 0.8, type: 'competitive', description: 'Weights & Biases vs Neptune.ai in experiment tracking' },
  { source: 103, target: 101, strength: 0.7, type: 'competitive', description: 'MLflow vs Weights & Biases in ML lifecycle' },
  { source: 104, target: 102, strength: 0.7, type: 'competitive', description: 'Comet ML vs Neptune.ai in experiment management' },

  // Audio processing family
  { source: 69, target: 70, strength: 0.8, type: 'competitive', description: 'Soundraw vs Amper Music in AI composition' },
  { source: 71, target: 72, strength: 0.7, type: 'competitive', description: 'AIVA vs Boomy in AI music generation' },
  { source: 73, target: 74, strength: 0.6, type: 'functional', description: 'Endel and Brain.fm both create focus-enhancing audio' },

  // Computer vision specialized tools
  { source: 52, target: 53, strength: 0.7, type: 'functional', description: 'Remove.bg followed by Upscale.media for image processing' },
  { source: 54, target: 55, strength: 0.8, type: 'competitive', description: 'Topaz Labs vs Luminar AI in photo enhancement' },
  { source: 56, target: 57, strength: 0.9, type: 'competitive', description: 'Reface vs FaceApp in mobile AI photo editing' },

  // Video generation and editing
  { source: 59, target: 60, strength: 0.9, type: 'competitive', description: 'RunwayML Gen-2 vs Pika Labs in text-to-video' },
  { source: 61, target: 62, strength: 0.8, type: 'competitive', description: 'Steve AI vs Pictory in AI video creation' },
  { source: 63, target: 64, strength: 0.7, type: 'competitive', description: 'Invideo AI vs Fliki in video generation' },

  // Speech processing connections
  { source: 174, target: 175, strength: 0.7, type: 'competitive', description: 'Kaldi vs ESPnet in speech recognition research' },
  { source: 176, target: 175, strength: 0.8, type: 'competitive', description: 'SpeechBrain vs ESPnet in speech processing' },

  // Language model connections
  { source: 177, target: 178, strength: 0.8, type: 'complementary', description: 'Fairseq models often distributed via Transformers' },
  { source: 181, target: 180, strength: 0.7, type: 'complementary', description: 'Gensim topic modeling complements NLTK preprocessing' },
  { source: 184, target: 180, strength: 0.8, type: 'functional', description: 'TextBlob built on top of NLTK for simplified usage' },

  // Additional cross-category connections
  { source: 136, target: 135, strength: 0.8, type: 'complementary', description: 'Jupyter AI features enhance R Studio workflows' },
  { source: 137, target: 136, strength: 0.7, type: 'competitive', description: 'Observable vs Jupyter in data visualization notebooks' },

  // Machine learning ops connections
  { source: 110, target: 111, strength: 0.8, type: 'competitive', description: 'DataRobot vs H2O.ai in automated machine learning' },
  { source: 112, target: 110, strength: 0.7, type: 'competitive', description: 'Google AutoML vs DataRobot in enterprise AutoML' },

  // Data science platform connections
  { source: 121, target: 120, strength: 0.8, type: 'competitive', description: 'Dataiku vs Domino Data Lab in data science platforms' },
  { source: 122, target: 121, strength: 0.6, type: 'competitive', description: 'Palantir vs Dataiku in data analytics platforms' },

  // Analytics platform connections
  { source: 130, target: 131, strength: 0.7, type: 'competitive', description: 'Alteryx vs Knime in data analytics workflows' },
  { source: 132, target: 133, strength: 0.8, type: 'competitive', description: 'RapidMiner vs Orange in visual ML tools' },
  { source: 134, target: 133, strength: 0.7, type: 'competitive', description: 'Weka vs Orange in academic ML tools' }
];

// Helper functions
export const calculateNodeSize = (popularity, connections) => {
  const baseSize = 1;
  const popularityFactor = (popularity / 100) * 3;
  const connectionsFactor = Math.log(connections + 1) * 0.5;
  return baseSize + popularityFactor + connectionsFactor;
};

export const getCategoryColor = (category) => {
  return CATEGORIES[category]?.color || '#6B7280';
};

export const getConnectionColor = (type) => {
  const colors = {
    'complementary': 'rgba(34, 197, 94, 0.6)', // Green - tools that complement each other
    'competitive': 'rgba(239, 68, 68, 0.6)', // Red - competing tools
    'functional': 'rgba(59, 130, 246, 0.6)', // Blue - functional relationship
    'workflow': 'rgba(168, 85, 247, 0.6)' // Purple - workflow integration
  };
  return colors[type] || 'rgba(156, 163, 175, 0.4)';
};

// Main data export function
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
    val: calculateNodeSize(tool.popularity, tool.connections),
    color: getCategoryColor(tool.category),
    // Get possible connections for this node
    possibleConnections: SYNERGIES_MOCK
      .filter(link => link.source === tool.id || link.target === tool.id)
      .map(link => {
        const connectedId = link.source === tool.id ? link.target : link.source;
        const connectedTool = AI_TOOLS_MOCK.find(t => t.id === connectedId);
        return {
          id: connectedId,
          name: connectedTool?.name || 'Unknown',
          type: link.type,
          description: link.description
        };
      })
  }));

  const links = SYNERGIES_MOCK.map(synergy => ({
    source: synergy.source,
    target: synergy.target,
    strength: synergy.strength,
    type: synergy.type,
    description: synergy.description,
    color: getConnectionColor(synergy.type)
  }));

  return { nodes, links };
};