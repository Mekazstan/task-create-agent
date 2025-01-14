import { useState } from 'react';
import axios from 'axios';
import { FiSend } from 'react-icons/fi';
import { clsx } from 'clsx';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        messages: [...messages, userMessage]
      });

      const aiMessage = { role: 'assistant', content: response.data.message };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      // Create a serializable error message
      const errorMessage = {
        role: 'error',
        content: error.response?.data?.detail || 'Sorry, there was an error processing your request.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Manage your Tasks with Tickle🤖</h1>
      </div>
      
      <div className="messages-container">
        {messages.map((message, index) => (
          <div
            key={index}
            className={clsx('message', {
              'user-message': message.role === 'user',
              'ai-message': message.role === 'assistant',
              'error-message': message.role === 'error'
            })}
          >
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message ai-message">
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button 
          type="submit" 
          disabled={isLoading || !input.trim()}
          className={clsx({ 'loading': isLoading })}
        >
          <FiSend />
        </button>
      </form>
    </div>
  );
}

export default App;