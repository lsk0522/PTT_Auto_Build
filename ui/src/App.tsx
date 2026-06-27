import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open, save } from "@tauri-apps/plugin-dialog";
import "./App.css";

function App() {
  const [designPath, setDesignPath] = useState<string>("");
  const [inputPath, setInputPath] = useState<string>("");
  const [rawText, setRawText] = useState<string>("");
  const [isRaw, setIsRaw] = useState<boolean>(true);
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
      
      // If we are using raw text instead of file path, we would need to save it to a temp file first, 
      // or pass the text directly. For simplicity in MVP, we assume inputPath is used.
      
      await invoke("generate_ppt", {
        designPath: designPath,
        inputPath: inputPath,
        outPath: outPath,
        isRaw: isRaw
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

      <button onClick={handleGenerate} disabled={!designPath || !inputPath}>
        Generate PPTX
      </button>
      
      <p>{status}</p>
    </main>
  );
}

export default App;
