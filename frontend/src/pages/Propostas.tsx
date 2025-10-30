// Em: frontend/src/pages/Propostas.tsx

import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import {Plus, FileText, DollarSign, User, X, Loader2} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

// --- INTERFACES CORRIGIDAS (baseadas no backend) ---
interface ShowCliente {
  id: number;
  nome_razao_social: string;
}

interface ShowUser {
  id: number;
  name: string;
}

enum PropostaStatus {
  NOVA = "nova",
  ENVIADA = "enviada",
  EM_NEGOCIACAO = "em_negociacao",
  GANHA = "ganha",
  PERDIDA = "perdida",
}

interface Proposta {
  id: number;
  nome: string | null;
  descricao: string | null;
  potencia_kwp: number | null;
  valor_total: number; // CORRIGIDO (era 'valor')
  status: PropostaStatus;
  cliente: ShowCliente; // CORRIGIDO (era 'cliente_nome')
  vendedor_responsavel: ShowUser; // CORRIGIDO (era 'vendedor_nome')
  // 'created_at' removido pois não existe no schema ShowProposta
}

// Interface para a lista de clientes no modal
interface Cliente {
  id: number;
  nome_razao_social: string;
  email: string | null;
  telefone: string | null;
}

// --- COMPONENTE ---
export default function Propostas() {
  const [propostas, setPropostas] = useState<Proposta[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const navigate = useNavigate();

  const fetchPropostas = async () => {
    try {
      const response = await api.get('/propostas/');
      setPropostas(response.data);
    } catch (error) {
      toast.error('Erro ao carregar propostas');
    } finally {
      setLoading(false);
    }
  };

  const fetchClientes = async () => {
    try {
      const response = await api.get('/clientes/');
      setClientes(response.data);
    } catch (error) {
      toast.error('Erro ao carregar clientes');
    }
  };

  useEffect(() => {
    fetchPropostas();
    fetchClientes();
  }, []);

  // --- FUNÇÃO DE CRIAÇÃO ATUALIZADA ---
  const handleSelectCliente = async (cliente: Cliente) => {
    setIsCreating(true);
    try {
      // 1. Criar a proposta 'em branco'
      // O backend (PropostaCreate) espera: cliente_id
      // valor_total, nome, etc. são opcionais.
      const payload = {
        cliente_id: cliente.id,
        nome: `Proposta para ${cliente.nome_razao_social}`,
        // Outros campos (valor_total, etc.) usarão o default do backend
      };

      const response = await api.post('/propostas/', payload);
      const novaProposta: Proposta = response.data;

      toast.success('Proposta criada! Redirecionando...');
      
      // 2. Redirecionar para a página de dimensionamento
      navigate(`/app/propostas/${novaProposta.id}/dimensionamento`);

    } catch (error) {
      toast.error('Erro ao criar proposta');
    } finally {
      setIsCreating(false);
      setShowModal(false);
    }
  };
  
  const getStatusColor = (status: string) => {
    const colors = {
      'nova': 'bg-gray-100 text-gray-800',
      'enviada': 'bg-blue-100 text-blue-800',
      'em_negociacao': 'bg-yellow-100 text-yellow-800',
      'ganha': 'bg-green-100 text-green-800',
      'perdida': 'bg-red-100 text-red-800',
    };
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-12 h-12 animate-spin text-orange-500" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Propostas</h1>
          <p className="text-gray-600">Gerencie suas propostas comerciais</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          disabled={isCreating}
          className="inline-flex items-center justify-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors disabled:opacity-50"
        >
          {isCreating ? <Loader2 className="w-5 h-5 animate-spin" /> : <Plus className="w-5 h-5" />}
          Nova Proposta
        </button>
      </div>

      {/* Propostas Grid - CAMPOS CORRIGIDOS */}
      <div className="grid gap-6 lg:grid-cols-2 xl:grid-cols-3">
        {propostas.map((proposta) => (
          <div 
            key={proposta.id} 
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => navigate(`/app/propostas/${proposta.id}/dimensionamento`)} // Adiciona link
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-orange-500 rounded-full flex items-center justify-center">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <div>
                  {/* USA O NOME DO CLIENTE DO OBJETO ANINHADO */}
                  <h3 className="font-semibold text-gray-900">{proposta.cliente.nome_razao_social}</h3>
                  <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full capitalize ${getStatusColor(proposta.status)}`}>
                    {proposta.status.replace('_', ' ')}
                  </span>
                </div>
              </div>
              {/* created_at removido, pois não vem da API */}
            </div>

            <div className="space-y-3">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <DollarSign className="w-4 h-4" />
                <span className="font-semibold text-gray-900">
                  {/* USA valor_total - A CORREÇÃO DO CRASH */}
                  R$ {proposta.valor_total.toLocaleString('pt-BR')}
                </span>
              </div>

              <div className="flex items-center gap-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                {/* USA O NOME DO VENDEDOR DO OBJETO ANINHADO */}
                <span>Vendedor: {proposta.vendedor_responsavel.name}</span>
              </div>

              <div className="text-sm text-gray-600">
                {/* USA O 'nome' da proposta ou 'descricao' */}
                <p className="line-clamp-3">{proposta.nome || proposta.descricao || 'Proposta sem descrição'}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {propostas.length === 0 && !loading && (
        <div className="text-center py-12">
          <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">Nenhuma proposta encontrada</p>
        </div>
      )}

      {/* Modal Seleção de Cliente (SIMPLIFICADO) */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Selecionar Cliente</h2>
              <button
                onClick={() => setShowModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="space-y-4">
              <p className="text-gray-600">Selecione um cliente para iniciar a proposta:</p>
              
              <div className="max-h-64 overflow-y-auto space-y-2">
                {clientes.map((cliente) => (
                  <div
                    key={cliente.id}
                    onClick={() => handleSelectCliente(cliente)}
                    className="p-3 border border-gray-200 rounded-lg hover:border-orange-500 cursor-pointer transition-colors"
                  >
                    {/* USA nome_razao_social */}
                    <div className="font-semibold text-gray-900">{cliente.nome_razao_social}</div>
                    <div className="text-sm text-gray-600">{cliente.email}</div>
                    <div className="text-sm text-gray-600">{cliente.telefone}</div>
                  </div>
                ))}
              </div>
              
              {clientes.length === 0 && (
                <p className="text-center text-gray-500 py-4">Nenhum cliente encontrado</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* O MODAL DE DIMENSIONAMENTO FOI REMOVIDO DAQUI */}
    </div>
  );
}