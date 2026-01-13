import React from 'react';
import { Activity, MessageSquare, Users, TrendingUp, CheckCircle } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const stats = [
    {
      label: 'Mensagens Hoje',
      value: '1.2k',
      change: '+12%',
      icon: MessageSquare,
      color: '#3b82f6',
    },
    {
      label: 'Conversas Ativas',
      value: '47',
      change: '+5',
      icon: Users,
      color: '#22c55e',
    },
    {
      label: 'Taxa Resolução',
      value: '89%',
      change: '+3%',
      icon: CheckCircle,
      color: '#22c55e',
    },
    {
      label: 'Orçamentos',
      value: '23',
      change: 'hoje',
      icon: TrendingUp,
      color: '#f59e0b',
    },
  ];

  const agents = [
    {
      name: 'Bot de Vendas',
      status: 'online',
      messages: 234,
      resolution: 92,
      model: 'Gemini Flash',
    },
    {
      name: 'Bot de Suporte',
      status: 'online',
      messages: 156,
      resolution: 87,
      model: 'Gemini Pro',
    },
  ];

  return (
    <div className="flex-1 bg-[#0a0a0a] overflow-y-auto">
      <div className="p-6 space-y-6">
        <div>
          <h1 className="text-white text-2xl font-bold">Dashboard</h1>
          <p className="text-[#888888] text-sm mt-1">Visão geral do sistema SunOps</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <div
                key={stat.label}
                className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4 hover:border-[#3b82f6] transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-[#888888] text-xs">{stat.label}</p>
                    <p className="text-white text-2xl font-bold mt-2">{stat.value}</p>
                    <p className="text-[#22c55e] text-xs mt-1">{stat.change}</p>
                  </div>
                  <div
                    className="p-2 rounded"
                    style={{ backgroundColor: `${stat.color}20` }}
                  >
                    <Icon className="w-5 h-5" style={{ color: stat.color }} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-white font-semibold">Status do Sistema</h2>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-[#22c55e]" />
              <span className="text-[#22c55e] text-xs">Operacional</span>
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-[#666666] text-xs">API</p>
              <p className="text-white text-sm mt-1">Online</p>
            </div>
            <div>
              <p className="text-[#666666] text-xs">Database</p>
              <p className="text-[#22c55e] text-sm mt-1">Online</p>
            </div>
            <div>
              <p className="text-[#666666] text-xs">Redis</p>
              <p className="text-[#22c55e] text-sm mt-1">Online</p>
            </div>
            <div>
              <p className="text-[#666666] text-xs">RabbitMQ</p>
              <p className="text-[#22c55e] text-sm mt-1">Online</p>
            </div>
          </div>
        </div>

        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
          <h2 className="text-white font-semibold mb-4">Agentes IA</h2>
          <div className="space-y-3">
            {agents.map((agent) => (
              <div
                key={agent.name}
                className="bg-[#0a0a0a] border border-[#2a2a2a] rounded p-3 flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-[#22c55e]" />
                  <div>
                    <p className="text-white text-sm font-medium">{agent.name}</p>
                    <p className="text-[#666666] text-xs">{agent.model}</p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <p className="text-white text-sm">{agent.messages}</p>
                    <p className="text-[#666666] text-xs">msgs/dia</p>
                  </div>
                  <div className="text-right">
                    <p className="text-[#22c55e] text-sm">{agent.resolution}%</p>
                    <p className="text-[#666666] text-xs">resolução</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
          <h2 className="text-white font-semibold mb-4">Atividade Recente</h2>
          <div className="space-y-3">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="flex items-start gap-3 pb-3 border-b border-[#2a2a2a] last:border-0"
              >
                <Activity className="w-4 h-4 text-[#3b82f6] mt-0.5" />
                <div className="flex-1">
                  <p className="text-white text-sm">Novo orçamento gerado</p>
                  <p className="text-[#666666] text-xs mt-1">há 5 minutos</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
