import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
npm install @supabase/supabase-js


const API_URL = 'https://your-actual-render-url.onrender.com';

interface Bot {
  id: string;
  bot_name: string;
  status: string;
  created_at: string;
}

function App() {
  const [bots, setBots] = useState<Bot[]>([]);
  const [botName, setBotName] = useState('');
  const [botToken, setBotToken] = useState('');

  useEffect(() => {
    fetchBots();
  }, []);

  const fetchBots = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/bots`);
      setBots(response.data);
    } catch (error) {
      console.error('Error fetching bots:', error);
    }
  };

  const createBot = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/bots`, {
        bot_name: botName,
        bot_token: botToken
      });
      setBotName('');
      setBotToken('');
      fetchBots();
    } catch (error) {
      console.error('Error creating bot:', error);
    }
  };

  const startBot = async (botId: string) => {
    try {
      await axios.post(`${API_URL}/api/bots/${botId}/start`);
      alert('Bot started!');
    } catch (error) {
      console.error('Error starting bot:', error);
    }
  };

  return (
    <div className="App">
      <h1>Creator Dashboard</h1>
      
      <div>
        <h2>Add New Bot</h2>
        <form onSubmit={createBot}>
          <input
            type="text"
            placeholder="Bot Name"
            value={botName}
            onChange={(e) => setBotName(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Bot Token"
            value={botToken}
            onChange={(e) => setBotToken(e.target.value)}
            required
          />
          <button type="submit">Add Bot</button>
        </form>
      </div>

      <div>
        <h2>Your Bots</h2>
        {bots.map((bot) => (
          <div key={bot.id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px' }}>
            <h3>{bot.bot_name}</h3>
            <p>Status: {bot.status}</p>
            <button onClick={() => startBot(bot.id)}>Start Bot</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;