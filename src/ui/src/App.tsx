import { useState, useRef, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open, save } from "@tauri-apps/plugin-dialog";
import "./App.css";

interface ChatMessage {
  id: string;
  role: 'user' | 'ai';
  text: string;
}

function App() {
  const [designPath, setDesignPath] = useState<string>("");
  const [aiProvider, setAiProvider] = useState<string>("gemini");
  const [apiKey, setApiKey] = useState<string>("");
  const [status, setStatus] = useState<string>("Ready to create amazing presentations ✨");
  
  // Chat State
  const [messages, setMessages] = useState<ChatMessage[]>([{
    id: 'intro',
    role: 'ai',
    text: "Hello! I'm your Presentation AI. Tell me what kind of PPT you want to create!"
  }]);
  const [chatInput, setChatInput] = useState<string>("");
  const [isChatting, setIsChatting] = useState<boolean>(false);
  const chatHistoryRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSelectDesign = async () => {
    const selected = await open({
      multiple: false,
      filters: [{ name: "Markdown", extensions: ["md"] }],
    });
    if (selected && !Array.isArray(selected)) {
      setDesignPath(selected);
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim()) return;
    if (!apiKey) {
      setStatus("⚠️ Please enter your API Key first.");
      return;
    }

    const userMessage: ChatMessage = { id: Date.now().toString(), role: 'user', text: chatInput };
    setMessages(prev => [...prev, userMessage]);
    setChatInput("");
    setIsChatting(true);
    setStatus("AI is thinking...");

    try {
      const responseText: string = await invoke("chat_with_ai", {
        message: userMessage.text,
        provider: aiProvider,
        apiKey: apiKey
      });

      const aiMessage: ChatMessage = { id: (Date.now() + 1).toString(), role: 'ai', text: responseText };
      setMessages(prev => [...prev, aiMessage]);
      setStatus("Ready.");
    } catch (error) {
      console.error(error);
      const errorMessage: ChatMessage = { id: (Date.now() + 1).toString(), role: 'ai', text: `Error: ${error}` };
      setMessages(prev => [...prev, errorMessage]);
      setStatus("Error communicating with AI.");
    } finally {
      setIsChatting(false);
    }
  };

  const handleGenerateFromChat = async () => {
    if (messages.length <= 1) {
      setStatus("⚠️ Chat with the AI first to generate content!");
      return;
    }
    
    // Get the latest AI response to use as input text
    const aiResponses = messages.filter(m => m.role === 'ai' && m.id !== 'intro');
    if (aiResponses.length === 0) return;
    const latestAiContent = aiResponses[aiResponses.length - 1].text;

    try {
      const outPath = await save({
        filters: [{ name: "PowerPoint", extensions: ["pptx"] }],
        defaultPath: "presentation.pptx"
      });
      
      if (!outPath) return;

      setStatus("✨ Generating your PowerPoint...");
      
      await invoke("generate_ppt", {
        designPath: designPath,
        inputPath: "", // Not using a file
        inputText: latestAiContent, // Passing the chat output directly!
        outPath: outPath,
        isRaw: true, // It needs to be parsed by the LLM in the engine into DSL if it isn't already DSL
        aiProvider: aiProvider,
        apiKey: apiKey
      });
      
      setStatus(`✅ Success! Presentation saved to ${outPath}`);
    } catch (error) {
      console.error(error);
      setStatus(`❌ Generation Failed: ${error}`);
    }
  };

  return (
    <div className="app-container">
      
      {/* Left Panel: Chat Interface */}
      <div className="panel chat-panel">
        <div className="chat-header">🤖 Presentation Assistant</div>
        
        <div className="chat-history" ref={chatHistoryRef}>
          {messages.map(msg => (
            <div key={msg.id} className={`chat-bubble ${msg.role}`}>
              {msg.text}
            </div>
          ))}
          {isChatting && (
            <div className="chat-bubble ai">Typing...</div>
          )}
        </div>

        <div className="chat-input-area">
          <input 
            type="text" 
            className="chat-input"
            placeholder="E.g. 'Make a 5-slide presentation about Space Exploration...'" 
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            disabled={isChatting}
          />
          <button className="btn btn-primary" onClick={handleSendMessage} disabled={isChatting}>
            Send
          </button>
        </div>
      </div>

      {/* Right Panel: Settings & Generation */}
      <div className="panel settings-panel">
        <div className="settings-header">PPT Generator</div>

        <div className="setting-group">
          <label>1. Select AI Provider</label>
          <select value={aiProvider} onChange={(e) => setAiProvider(e.target.value)}>
            <option value="gemini">Google Gemini (Flash)</option>
            <option value="perplexity">Perplexity (Sonar)</option>
            <option value="openai">OpenAI (GPT-4o)</option>
          </select>
        </div>

        <div className="setting-group">
          <label>2. API Key Authentication</label>
          <input 
            type="password" 
            placeholder={`Enter your ${aiProvider.toUpperCase()} API Key`}
            value={apiKey} 
            onChange={(e) => setApiKey(e.target.value)} 
          />
        </div>

        <div className="setting-group">
          <label>3. Design Theme (Optional)</label>
          <button className="btn" onClick={handleSelectDesign}>
            {designPath ? 'Change Theme File' : 'Select DESIGN.md'}
          </button>
          <span style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.2rem' }}>
            {designPath || "No design selected. Default theme will be used."}
          </span>
        </div>

        <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <button 
            className="btn btn-primary" 
            style={{ padding: '1.2rem', fontSize: '1.1rem' }}
            onClick={handleGenerateFromChat} 
            disabled={!designPath || !apiKey || messages.length <= 1}
          >
            Export to PPTX
          </button>

          <div className="status-bar">
            {status}
          </div>
        </div>
      </div>

    </div>
  );
}

export default App;
