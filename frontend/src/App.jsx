import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL = "http://localhost:8000";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi, I am your RAG assistant. Upload a document and ask me anything from it.",
    },
  ]);

  const [question, setQuestion] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);

      const response = await axios.post(`${API_BASE_URL}/api/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: response.data.message,
        },
      ]);

      setFile(null);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Upload failed. Please check backend/Qdrant/Ollama.",
        },
      ]);
    } finally {
      setUploading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        question: userQuestion,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: response.data.answer,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Something went wrong. Please check the backend terminal.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleAsk();
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        <h1>Production RAG Chatbot</h1>
        <p className="subtitle">React + FastAPI + Qdrant + Redis + Ollama</p>

        <div className="upload-box">
          <input
            type="file"
            accept=".txt"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button onClick={handleUpload} disabled={uploading}>
            {uploading ? "Uploading..." : "Upload Document"}
          </button>
        </div>

        <div className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              {message.text}
            </div>
          ))}

          {loading && <div className="message bot">Thinking...</div>}
        </div>

        <div className="input-box">
          <input
            type="text"
            placeholder="Ask a question from your document..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button onClick={handleAsk} disabled={loading}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;