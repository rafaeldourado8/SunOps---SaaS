import React, { useState, useEffect } from 'react';
import { Smartphone, QrCode, CheckCircle, XCircle, Loader } from 'lucide-react';
import { PageHeader } from '../Common/PageHeader';

export function WhatsAppPage() {
  const [status, setStatus] = useState<'disconnected' | 'connecting' | 'connected'>('disconnected');
  const [qrCode, setQrCode] = useState<string>('');
  const [metrics, setMetrics] = useState({ messages: 0, conversations: 0 });
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    connectWebSocket();
    return () => ws?.close();
  }, []);

  const connectWebSocket = () => {
    const websocket = new WebSocket('ws://localhost:3001');
    
    websocket.onopen = () => {
      console.log('WebSocket conectado');
    };
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'qr') {
        setQrCode(data.qr);
        setStatus('connecting');
      } else if (data.type === 'ready') {
        setStatus('connected');
        setQrCode('');
      } else if (data.type === 'disconnected') {
        setStatus('disconnected');
        setQrCode('');
      }
    };
    
    websocket.onerror = () => {
      setStatus('disconnected');
    };
    
    setWs(websocket);
  };

  const handleConnect = () => {
    setStatus('connecting');
    connectWebSocket();
  };

  const handleDisconnect = () => {
    ws?.close();
    setStatus('disconnected');
    setQrCode('');
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-6">
      <PageHeader
        title="📱 WhatsApp"
        subtitle="Configure e gerencie a integração com WhatsApp"
      />

      <div className="grid grid-cols-3 gap-6 mt-6">
        {/* Status e Conexão */}
        <div className="col-span-2 bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold">Status da Conexão</h2>
            <div className="flex items-center gap-2">
              {status === 'connected' && (
                <>
                  <CheckCircle className="w-5 h-5 text-[#22c55e]" />
                  <span className="text-[#22c55e] text-sm">Conectado</span>
                </>
              )}
              {status === 'connecting' && (
                <>
                  <Loader className="w-5 h-5 text-[#f59e0b] animate-spin" />
                  <span className="text-[#f59e0b] text-sm">Conectando...</span>
                </>
              )}
              {status === 'disconnected' && (
                <>
                  <XCircle className="w-5 h-5 text-[#ef4444]" />
                  <span className="text-[#ef4444] text-sm">Desconectado</span>
                </>
              )}
            </div>
          </div>

          {/* QR Code */}
          {status === 'connecting' && qrCode && (
            <div className="flex flex-col items-center justify-center py-8">
              <QrCode className="w-12 h-12 text-[#3b82f6] mb-4" />
              <h3 className="text-lg font-semibold mb-2">Escaneie o QR Code</h3>
              <p className="text-[#888888] text-sm mb-6 text-center">
                Abra o WhatsApp no seu celular e escaneie o código abaixo
              </p>
              <div className="bg-white p-4 rounded-lg">
                <img src={qrCode} alt="QR Code" className="w-64 h-64" />
              </div>
            </div>
          )}

          {/* Conectado */}
          {status === 'connected' && (
            <div className="flex flex-col items-center justify-center py-12">
              <Smartphone className="w-16 h-16 text-[#22c55e] mb-4" />
              <h3 className="text-lg font-semibold mb-2">WhatsApp Conectado!</h3>
              <p className="text-[#888888] text-sm text-center">
                Seu WhatsApp está conectado e pronto para receber mensagens
              </p>
            </div>
          )}

          {/* Desconectado */}
          {status === 'disconnected' && (
            <div className="flex flex-col items-center justify-center py-12">
              <Smartphone className="w-16 h-16 text-[#666666] mb-4" />
              <h3 className="text-lg font-semibold mb-2">WhatsApp Desconectado</h3>
              <p className="text-[#888888] text-sm text-center mb-6">
                Clique no botão abaixo para conectar seu WhatsApp
              </p>
            </div>
          )}

          {/* Botões */}
          <div className="flex gap-3 mt-6">
            {status === 'disconnected' && (
              <button
                onClick={handleConnect}
                className="flex-1 bg-[#22c55e] hover:bg-[#16a34a] text-white px-6 py-3 rounded font-medium transition-colors"
              >
                Conectar WhatsApp
              </button>
            )}
            {status === 'connected' && (
              <button
                onClick={handleDisconnect}
                className="flex-1 bg-[#ef4444] hover:bg-[#dc2626] text-white px-6 py-3 rounded font-medium transition-colors"
              >
                Desconectar WhatsApp
              </button>
            )}
          </div>
        </div>

        {/* Métricas */}
        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-6">Métricas</h2>
          
          <div className="space-y-4">
            <div className="bg-[#0a0a0a] border border-[#2a2a2a] rounded p-4">
              <div className="text-2xl font-bold text-[#3b82f6]">{metrics.messages}</div>
              <div className="text-xs text-[#888888] mt-1">Mensagens Hoje</div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#2a2a2a] rounded p-4">
              <div className="text-2xl font-bold text-[#22c55e]">{metrics.conversations}</div>
              <div className="text-xs text-[#888888] mt-1">Conversas Ativas</div>
            </div>

            <div className="bg-[#0a0a0a] border border-[#2a2a2a] rounded p-4">
              <div className="text-2xl font-bold text-[#f59e0b]">
                {status === 'connected' ? '100%' : '0%'}
              </div>
              <div className="text-xs text-[#888888] mt-1">Disponibilidade</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
