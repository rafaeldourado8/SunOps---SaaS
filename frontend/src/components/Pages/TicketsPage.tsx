import React, { useState, useEffect } from 'react';
import { Ticket, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import { api } from '../../lib/api';
import { PageHeader } from '../Common/PageHeader';

export const TicketsPage: React.FC = () => {
  const [tickets, setTickets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      const response = await api.get('/agents/tickets');
      setTickets(response.tickets || []);
    } catch (error) {
      console.error('Error loading tickets:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'text-[#ef4444]';
      case 'resolved': return 'text-[#22c55e]';
      case 'in_progress': return 'text-[#f59e0b]';
      default: return 'text-[#888888]';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open': return <AlertCircle className="w-4 h-4" />;
      case 'resolved': return <CheckCircle className="w-4 h-4" />;
      case 'in_progress': return <Clock className="w-4 h-4" />;
      default: return <Ticket className="w-4 h-4" />;
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'open': return 'Aberto';
      case 'resolved': return 'Resolvido';
      case 'in_progress': return 'Em Andamento';
      default: return status;
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-6">
      <PageHeader
        title="🎫 Tickets de Suporte"
        subtitle="Gerencie todos os tickets de suporte técnico"
      />

      <div className="mt-6">
        {loading ? (
          <div className="text-center text-[#666666] py-12">
            Carregando tickets...
          </div>
        ) : tickets.length === 0 ? (
          <div className="text-center text-[#666666] py-12">
            <Ticket className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>Nenhum ticket encontrado</p>
          </div>
        ) : (
          <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg overflow-hidden">
            <table className="w-full">
              <thead className="bg-[#0a0a0a] border-b border-[#2a2a2a]">
                <tr>
                  <th className="text-left text-xs font-medium text-[#888888] uppercase px-6 py-3">
                    Ticket
                  </th>
                  <th className="text-left text-xs font-medium text-[#888888] uppercase px-6 py-3">
                    Status
                  </th>
                  <th className="text-left text-xs font-medium text-[#888888] uppercase px-6 py-3">
                    Prioridade
                  </th>
                  <th className="text-left text-xs font-medium text-[#888888] uppercase px-6 py-3">
                    Assunto
                  </th>
                  <th className="text-left text-xs font-medium text-[#888888] uppercase px-6 py-3">
                    Telefone
                  </th>
                  <th className="text-left text-xs font-medium text-[#888888] uppercase px-6 py-3">
                    Criado em
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2a2a2a]">
                {tickets.map((ticket) => (
                  <tr key={ticket.id} className="hover:bg-[#0a0a0a] transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <Ticket className="w-4 h-4 text-[#3b82f6]" />
                        <span className="text-sm font-mono">{ticket.ticket_number}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className={`flex items-center gap-2 ${getStatusColor(ticket.status)}`}>
                        {getStatusIcon(ticket.status)}
                        <span className="text-sm">{getStatusLabel(ticket.status)}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-[#888888]">{ticket.priority || 'Normal'}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm">{ticket.subject || '-'}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-[#888888]">{ticket.phone}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-[#888888]">
                        {new Date(ticket.created_at).toLocaleDateString('pt-BR')}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
