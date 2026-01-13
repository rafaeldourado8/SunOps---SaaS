import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';
import { PageHeader } from '../components/Common/PageHeader';

export const VendasAgentTestPage: React.FC = () => {
  const [phone, setPhone] = useState('+5511999999999');
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      const data = await api.get('/agents/vendas/metrics');
      setMetrics(data);
    } catch (error) {
      console.error('Error loading metrics:', error);
    }
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    try {
      const response = await api.post('/agents/vendas/message', {
        phone,
        message,
      });

      setConversation([
        ...conversation,
        { role: 'user', content: message },
        { role: 'assistant', content: response.text },
      ]);
      setMessage('');
      loadMetrics();
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Erro ao enviar mensagem');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-6">
      <PageHeader
        title="🤖 Teste - Agente de Vendas"
        subtitle="Teste o agente de vendas em tempo real"
      />

      <div className="grid grid-cols-3 gap-6 mt-6">
        {/* Chat */}
        <div className="col-span-2 bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Conversa</h2>

          <div className="space-y-4 mb-4 h-96 overflow-y-auto">
            {conversation.map((msg, index) => (
              <div
                key={index}
                className={`p-3 rounded ${
                  msg.role === 'user'
                    ? 'bg-[#3b82f6] ml-12'
                    : 'bg-[#2a2a2a] mr-12'
                }`}
              >
                <div className="text-xs text-[#888888] mb-1">
                  {msg.role === 'user' ? 'Você' : 'Bot'}
                </div>
                <div className="text-sm">{msg.content}</div>
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Digite sua mensagem..."
              className="flex-1 bg-[#0a0a0a] border border-[#2a2a2a] rounded px-4 py-2 text-white focus:outline-none focus:border-[#3b82f6]"
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              className="bg-[#3b82f6] hover:bg-[#2563eb] px-6 py-2 rounded font-medium disabled:opacity-50"
            >
              {loading ? 'Enviando...' : 'Enviar'}
            </button>
          </div>
        </div>

        {/* Métricas */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">Métricas</h2>

          {metrics ? (
            <div className="space-y-4">
              <div className="bg-[#0a0a0a] border border-[#2a2a2a] rounded p-4">
                <div className="text-2xl font-bold">{metrics.total_conversations}</div>
                <div className="text-xs text-[#888888] mt-1">Total Conversas</div>
              </div>

              <div className="bg-[#0a0a0a] border border-[#2a2a2a] rounded p-4">
                <div className="text-2xl font-bold text-[#22c55e]">
                  {metrics.active_conversations}
                </div>
                <div className="text-xs text-[#888888] mt-1">Conversas Ativas</div>
              </div>

              <div className="bg-[#0a0a0a] border border-[#2a2a2a] rounded p-4">
                <div className="text-2xl font-bold text-[#3b82f6]">
                  {metrics.orcamentos_gerados}
                </div>
                <div className="text-xs text-[#888888] mt-1">Orçamentos Gerados</div>
              </div>

              <div className="bg-[#0a0a0a] border border-[#2a2a2a] rounded p-4">
                <div className="text-2xl font-bold text-[#f59e0b]">
                  {(metrics.taxa_conversao * 100).toFixed(1)}%
                </div>
                <div className="text-xs text-[#888888] mt-1">Taxa Conversão</div>
              </div>
            </div>
          ) : (
            <div className="text-[#666666] text-sm">Carregando métricas...</div>
          )}
        </div>
      </div>
    </div>
  );
};
