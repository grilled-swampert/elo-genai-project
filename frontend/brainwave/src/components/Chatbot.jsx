import React, { useState, useEffect } from "react";
import axios from "axios";
import chatbotIcon from "../assets/chatbot.webp"; // Import custom chatbot icon

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const financeKeywords = [
    "stocks",
    "bonds",
    "mutual funds",
    "investment",
    "banking",
    "portfolio",
    "finance",
    "hedge funds",
    "market trends",
    "interest rates",
    "financial",
    "capital",
    "loans",
    "credit",
    "insurance",
    "bank",
  ];

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async () => {
    if (userMessage.trim() === "") return;

    const newMessages = [...messages, { sender: "user", text: userMessage }];
    setMessages(newMessages);
    setUserMessage("");

    // Normalize user input for keyword matching
    const normalizedMessage = userMessage.toLowerCase();

    // Check if the query is related to finance topics
    const isFinanceRelated = financeKeywords.some((keyword) =>
      normalizedMessage.includes(keyword)
    );

    if (!isFinanceRelated) {
      setMessages([
        ...newMessages,
        {
          sender: "bot",
          text: "❌ Invalid query: Please ask questions related to finance, banking, or investments.",
        },
      ]);
      return;
    }

    setIsTyping(true);

    try {
      const response = await axios.post(
        "https://api.openai.com/v1/chat/completions",
        {
          model: "gpt-3.5-turbo",
          messages: [{ role: "user", content: userMessage }],
          max_tokens: 150,
          temperature: 0.7,
        },
        {
          headers: {
            Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
            "Content-Type": "application/json",
          },
        }
      );

      const botMessage = response.data.choices[0].message.content.trim();
      setMessages([...newMessages, { sender: "bot", text: botMessage }]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages([
        ...newMessages,
        { sender: "bot", text: "⚠️ Sorry, I couldn't fetch the answer. Please try again." },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  useEffect(() => {
    const chatbox = document.querySelector(".chatbox-messages");
    if (chatbox) chatbox.scrollTop = chatbox.scrollHeight;
  }, [messages]);

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Chatbot Icon */}
      <div
        className="p-4 rounded-full shadow-xl cursor-pointer hover:scale-110 transition-transform"
        onClick={handleToggle}
      >
        <img
          src={chatbotIcon}
          alt="Chatbot Icon"
          className="w-16 h-16 rounded-full object-cover border-4 border-purple-500 shadow-lg"
        />
      </div>

      {/* Chatbox Window */}
      {isOpen && (
        <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg h-[32rem] border border-gray-200 flex flex-col transition-all transform">
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-lg font-semibold py-3 px-4 rounded-t-xl flex justify-between items-center">
            <span>Elo AI Chat</span>
            <button
              className="text-white text-xl font-bold cursor-pointer"
              onClick={handleToggle}
            >
              ×
            </button>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3 bg-gray-50 chatbox-messages">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`px-4 py-2 rounded-lg max-w-xs text-sm ${
                    msg.sender === "user"
                      ? "bg-purple-500 text-white shadow-md"
                      : "bg-gray-200 text-gray-800 shadow-sm"
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex justify-start">
                <div className="px-4 py-2 rounded-lg max-w-xs text-sm bg-gray-200 text-gray-800 shadow-sm">
                  🔄 Elo AI is typing...
                </div>
              </div>
            )}
          </div>

          {/* Input Section */}
          <div className="bg-white border-t border-gray-200 px-4 py-3 flex items-center space-x-3">
            <input
              type="text"
              className="flex-1 border border-gray-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-purple-500 outline-none"
              placeholder="Ask your query..."
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              onKeyDown={handleKeyDown} // Listen for Enter key
            />
            <button
              className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-lg text-sm hover:scale-105 transition-transform"
              onClick={handleSendMessage}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
