import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open, save } from "@tauri-apps/plugin-dialog";
import "./App.css";

function App() {
  const [designPath, setDesignPath] = useState<string>("");
  const [inputPath, setInputPath] = useState<string>("");
  const [isRaw, setIsRaw] = useState<boolean>(true);
  const [aiProvider, setAiProvider] = useState<string>("gemini");
  const [apiKey, setApiKey] = useState<string>("");
  const [status, setStatus] = useState<string>("");

  const handleSelectDesign = async () => {
    const selected = await open({
      multiple: false,
      filters: [{ name: "Markdown", extensions: ["md"] }],
    });
    if (selected && !Array.isArray(selected)) {
      setDesignPath(selected);
    }
  };

  const handleSelectInput = async () => {
    const selected = await open({
      multiple: false,
      filters: [{ name: "Text", extensions: ["txt", "md"] }],
    });
    if (selected && !Array.isArray(selected)) {
      setInputPath(selected);
    }
  };

  const handleGenerate = async () => {
    try {
      const outPath = await save({
        filters: [{ name: "PowerPoint", extensions: ["pptx"] }],
        defaultPath: "presentation.pptx"
      });
      
      if (!outPath) return;

      setStatus("Generating PPTX...");
      
      await invoke("generate_ppt", {
        designPath: designPath,
        inputPath: inputPath,
        outPath: outPath,
        isRaw: isRaw,
        aiProvider: aiProvider,
        apiKey: apiKey
      });
      
      setStatus(`Success! Saved to ${outPath}`);
    } catch (error) {
      console.error(error);
      setStatus(`Error: ${error}`);
    }
  };

  return (
    <main className="container">
      <h1>PPT Generator</h1>
      
      <div className="row">
        <button onClick={handleSelectDesign}>Select DESIGN.md</button>
        <span>{designPath || "No file selected"}</span>
      </div>

      <div className="row">
        <button onClick={handleSelectInput}>Select Input Data (TXT/MD)</button>
        <span>{inputPath || "No file selected"}</span>
      </div>
      
      <div className="row">
        <label>
          <input 
            type="checkbox" 
            checked={isRaw} 
            onChange={(e) => setIsRaw(e.target.checked)} 
          />
          Use LLM to structure content (Raw Data Mode)
        </label>
      </div>

      {isRaw && (
        <>
          <div className="row">
            <label>AI Provider: </label>
            <select value={aiProvider} onChange={(e) => setAiProvider(e.target.value)}>
              <option value="gemini">Gemini</option>
              <option value="perplexity">Perplexity</option>
              <option value="openai">OpenAI</option>
            </select>
          </div>
          <div className="row">
            <label>API Key: </label>
            <input 
              type="password" 
              placeholder="Enter your API Key" 
              value={apiKey} 
              onChange={(e) => setApiKey(e.target.value)} 
            />
          </div>
        </>
      )}

      <button onClick={handleGenerate} disabled={!designPath || !inputPath || (isRaw && !apiKey)}>
        Generate PPTX
      </button>
      
      <p>{status}</p>
    </main>
  );
}

export default App;
