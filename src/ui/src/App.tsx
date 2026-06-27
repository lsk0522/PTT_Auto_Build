import { useState, useRef, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open, save } from "@tauri-apps/plugin-dialog";
import "./App.css";

interface ChatMessage {
  id: string;
  role: 'user' | 'ai';
  text: string;
}

const translations: Record<string, any> = {
  Korean: {
    title: "🤖 발표자료 생성 도우미",
    intro: "안녕하세요! 발표자료 생성 AI입니다. 어떤 PPT를 만들고 싶으신지 말씀해 주세요!",
    placeholder: "예: '우주 탐사 역사에 대한 5장짜리 슬라이드 만들어줘...'",
    send: "전송",
    settingsTitle: "PPT 생성기 설정",
    langLabel: "1. 출력 언어 설정",
    providerLabel: "2. AI 모델 선택",
    apiKeyLabel: "3. API 키 인증",
    apiKeyPlaceholder: "API 키를 입력하세요",
    themeLabel: "4. 디자인 테마 (선택)",
    themeChange: "테마 파일 변경",
    themeSelect: "DESIGN.md 선택",
    themeNone: "지정된 디자인 없음. 기본 테마가 사용됩니다.",
    exportBtn: "PPTX 파일로 내보내기",
    typing: "입력 중...",
    statusReady: "멋진 발표자료를 만들 준비가 되었습니다 ✨",
    statusThinking: "AI가 생각하는 중...",
    statusGenerating: "✨ 파워포인트 파일을 생성하는 중...",
    statusSuccess: "✅ 성공! 발표자료가 저장되었습니다: ",
    statusError: "❌ 실패: "
  },
  English: {
    title: "🤖 Presentation Assistant",
    intro: "Hello! I'm your Presentation AI. Tell me what kind of PPT you want to create!",
    placeholder: "E.g. 'Make a 5-slide presentation about Space Exploration...'",
    send: "Send",
    settingsTitle: "PPT Generator",
    langLabel: "1. Output Language",
    providerLabel: "2. Select AI Provider",
    apiKeyLabel: "3. API Key Authentication",
    apiKeyPlaceholder: "Enter your API Key",
    themeLabel: "4. Design Theme (Optional)",
    themeChange: "Change Theme File",
    themeSelect: "Select DESIGN.md",
    themeNone: "No design selected. Default theme will be used.",
    exportBtn: "Export to PPTX",
    typing: "Typing...",
    statusReady: "Ready to create amazing presentations ✨",
    statusThinking: "AI is thinking...",
    statusGenerating: "✨ Generating your PowerPoint...",
    statusSuccess: "✅ Success! Presentation saved to: ",
    statusError: "❌ Generation Failed: "
  },
  Japanese: {
    title: "🤖 プレゼンテーション アシスタント",
    intro: "こんにちは！プレゼン作成AIです。どのようなPPTを作りたいか教えてください！",
    placeholder: "例：'宇宙探査の歴史に関する5枚のスライドを作って...'",
    send: "送信",
    settingsTitle: "PPT ジェネレーター",
    langLabel: "1. 出力言語",
    providerLabel: "2. AIプロバイダーの選択",
    apiKeyLabel: "3. APIキー認証",
    apiKeyPlaceholder: "APIキーを入力してください",
    themeLabel: "4. デザインテーマ（オプション）",
    themeChange: "テーマファイルの変更",
    themeSelect: "DESIGN.mdを選択",
    themeNone: "デザインが選択されていません。デフォルトテーマが使用されます。",
    exportBtn: "PPTXでエクスポート",
    typing: "入力中...",
    statusReady: "素晴らしいプレゼンテーションを作成する準備ができました ✨",
    statusThinking: "AIが考えています...",
    statusGenerating: "✨ パワーポイントを作成しています...",
    statusSuccess: "✅ 成功！プレゼンテーションが保存されました: ",
    statusError: "❌ エクスポート失敗: "
  },
  Chinese: {
    title: "🤖 演示文稿助手",
    intro: "你好！我是你的演示文稿 AI 助手。告诉我你想创建什么样的 PPT！",
    placeholder: "例如：'制作一个关于太空探索历史的5页幻灯片...'",
    send: "发送",
    settingsTitle: "PPT 生成器",
    langLabel: "1. 输出语言",
    providerLabel: "2. 选择 AI 提供商",
    apiKeyLabel: "3. API 密钥认证",
    apiKeyPlaceholder: "请输入您的 API 密钥",
    themeLabel: "4. 设计主题（可选）",
    themeChange: "更改主题文件",
    themeSelect: "选择 DESIGN.md",
    themeNone: "未选择设计。将使用默认主题。",
    exportBtn: "导出为 PPTX",
    typing: "正在输入...",
    statusReady: "准备好创建精彩的演示文稿了 ✨",
    statusThinking: "AI 正在思考...",
    statusGenerating: "✨ 正在生成您的幻灯片...",
    statusSuccess: "✅ 成功！演示文稿已保存至: ",
    statusError: "❌ 导出失败: "
  }
};

function App() {
  const [designPath, setDesignPath] = useState<string>("");
  const [aiProvider, setAiProvider] = useState<string>("gemini");
  const [apiKey, setApiKey] = useState<string>("AIzaSyBx...");
  const [language, setLanguage] = useState<string>("Korean");
  const [status, setStatus] = useState<string>("Ready to create amazing presentations ✨");
  
  const t = translations[language] || translations["Korean"];

  // Chat State
  const [messages, setMessages] = useState<ChatMessage[]>([{
    id: 'intro',
    role: 'ai',
    text: t.intro
  }]);
  const [chatInput, setChatInput] = useState<string>("");
  const [isChatting, setIsChatting] = useState<boolean>(false);
  const chatHistoryRef = useRef<HTMLDivElement>(null);

  // Update intro message when language changes
  useEffect(() => {
    setMessages(prev => prev.map(m => m.id === 'intro' ? { ...m, text: t.intro } : m));
    setStatus(t.statusReady);
  }, [language]);

  // Auto-scroll chat
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSelectDesign = async () => {
    try {
      const selected = await open({
        multiple: false,
        filters: [{ name: "Markdown", extensions: ["md"] }],
      });
      if (selected && !Array.isArray(selected)) {
        setDesignPath(selected);
      }
    } catch (err) {
      console.error(err);
      setStatus(`${t.statusError} ${err}`);
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
    setStatus(t.statusThinking);

    try {
      const responseText: string = await invoke("chat_with_ai", {
        message: userMessage.text,
        provider: aiProvider,
        apiKey: apiKey,
        language: language
      });

      const aiMessage: ChatMessage = { id: (Date.now() + 1).toString(), role: 'ai', text: responseText };
      setMessages(prev => [...prev, aiMessage]);
      setStatus(t.statusReady);
    } catch (error) {
      console.error(error);
      const errorMessage: ChatMessage = { id: (Date.now() + 1).toString(), role: 'ai', text: `Error: ${error}` };
      setMessages(prev => [...prev, errorMessage]);
      setStatus(t.statusError + error);
    } finally {
      setIsChatting(false);
    }
  };

  const handleGenerateFromChat = async () => {
    if (messages.length <= 1) {
      setStatus("⚠️ Chat with the AI first to generate content!");
      return;
    }
    
    const aiResponses = messages.filter(m => m.role === 'ai' && m.id !== 'intro');
    if (aiResponses.length === 0) return;
    const latestAiContent = aiResponses[aiResponses.length - 1].text;

    try {
      const outPath = await save({
        filters: [{ name: "PowerPoint", extensions: ["pptx"] }],
        defaultPath: "presentation.pptx"
      });
      
      if (!outPath) return;

      setStatus(t.statusGenerating);
      
      await invoke("generate_ppt", {
        designPath: designPath,
        inputPath: "", 
        inputText: latestAiContent, 
        outPath: outPath,
        isRaw: true, 
        aiProvider: aiProvider,
        apiKey: apiKey,
        language: language
      });
      
      setStatus(`${t.statusSuccess} ${outPath}`);
    } catch (error) {
      console.error(error);
      setStatus(`${t.statusError} ${error}`);
    }
  };

  return (
    <div className="app-container">
      
      {/* Left Panel: Chat Interface */}
      <div className="panel chat-panel">
        <div className="chat-header">{t.title}</div>
        
        <div className="chat-history" ref={chatHistoryRef}>
          {messages.map(msg => (
            <div key={msg.id} className={`chat-bubble ${msg.role}`}>
              {msg.text}
            </div>
          ))}
          {isChatting && (
            <div className="chat-bubble ai">{t.typing}</div>
          )}
        </div>

        <div className="chat-input-area">
          <input 
            type="text" 
            className="chat-input"
            placeholder={t.placeholder} 
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            disabled={isChatting}
          />
          <button className="btn btn-primary" onClick={handleSendMessage} disabled={isChatting}>
            {t.send}
          </button>
        </div>
      </div>

      {/* Right Panel: Settings & Generation */}
      <div className="panel settings-panel">
        <div className="settings-header">{t.settingsTitle}</div>

        <div className="setting-group">
          <label>{t.langLabel}</label>
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="Korean">Korean (한국어)</option>
            <option value="English">English (영어)</option>
            <option value="Japanese">Japanese (日本語)</option>
            <option value="Chinese">Chinese (中文)</option>
          </select>
        </div>

        <div className="setting-group">
          <label>{t.providerLabel}</label>
          <select value={aiProvider} onChange={(e) => setAiProvider(e.target.value)}>
            <option value="gemini">Google Gemini (Flash)</option>
            <option value="perplexity">Perplexity (Sonar)</option>
            <option value="openai">OpenAI (GPT-4o)</option>
          </select>
        </div>

        <div className="setting-group">
          <label>{t.apiKeyLabel}</label>
          <input 
            type="password" 
            placeholder={t.apiKeyPlaceholder}
            value={apiKey} 
            onChange={(e) => setApiKey(e.target.value)} 
          />
        </div>

        <div className="setting-group">
          <label>{t.themeLabel}</label>
          <button className="btn" onClick={handleSelectDesign}>
            {designPath ? t.themeChange : t.themeSelect}
          </button>
          <span style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.2rem' }}>
            {designPath || t.themeNone}
          </span>
        </div>

        <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <button 
            className="btn btn-primary" 
            style={{ padding: '1.2rem', fontSize: '1.1rem' }}
            onClick={handleGenerateFromChat} 
            disabled={!designPath || !apiKey || messages.length <= 1}
          >
            {t.exportBtn}
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
