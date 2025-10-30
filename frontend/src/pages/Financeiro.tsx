import { useEffect, useState } from 'react';
import {DollarSign, TrendingUp, Settings, FileText, CheckCircle, Clock} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

// --- INTERFACES CORRIGIDAS (baseadas em financeiro/schema.py) ---

interface ConfiguracaoFinanceira {
  id: number;
  margem_lucro_padrao: number;
  percentual_comissao_padrao: number;
}

enum TipoTransacao {
  ENTRADA_PROJETO = "entrada_projeto",
  CUSTO_EQUIPAMENTO = "custo_equipamento",
  COMISSAO_A_PAGAR = "comissao_a_pagar",
  OUTRA_RECEITA = "outra_receita",
  OUTRA_DESPESA = "outra_despesa",
}

enum StatusTransacao {
  PENDENTE = "pendente",
  PAGA = "paga",
  ATRASADA = "atrasada",
  CANCELADA = "cancelada",
}

interface Transacao {
  id: number;
  descricao: string;
  valor: number;
  tipo: TipoTransacao;
  status: StatusTransacao;
  data_criacao: string; // Vem como string ISO
  data_vencimento: string | null; // Vem como string ISO
  projeto_id: number | null;
  vendedor_id: number | null;
}

export default function Financeiro() {
  const [config, setConfig] = useState<ConfiguracaoFinanceira | null>(null);
  const [transacoes, setTransacoes] = useState<Transacao[]>([]);
  const [loading, setLoading] = useState(true);

  // Estado para o formulário de atualização
  const [editConfig, setEditConfig] = useState<ConfiguracaoFinanceira | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Carrega as duas fontes de dados
      const [configResponse, transacoesResponse] = await Promise.all([
        api.get('/financeiro/configuracoes'),
        api.get('/financeiro/transacoes')
      ]);

      setConfig(configResponse.data);
      setEditConfig(configResponse.data); // Preenche o formulário de edição
      setTransacoes(transacoesResponse.data);

    } catch (error) {
      toast.error('Erro ao carregar dados financeiros');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleConfigUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editConfig) return;

    const payload = {
      margem_lucro_padrao: parseFloat(String(editConfig.margem_lucro_padrao)),
      percentual_comissao_padrao: parseFloat(String(editConfig.percentual_comissao_padrao)),
    };

    try {
      const response = await api.put('/financeiro/configuracoes', payload);
      setConfig(response.data);
      setEditConfig(response.data);
      toast.success('Configurações salvas com sucesso!');
    } catch (error) {
      toast.error('Erro ao salvar configurações');
    }
  };

  const getStatusColor = (status: StatusTransacao) => {
    const colors = {
      'paga': 'bg-green-100 text-green-800',
      'pendente': 'bg-yellow-100 text-yellow-800',
      'atrasada': 'bg-red-100 text-red-800',
      'cancelada': 'bg-gray-100 text-gray-800',
    };
    return colors[status] || colors.cancelada;
  };

  const getStatusIcon = (status: StatusTransacao) => {
    const icons = {
      'paga': <CheckCircle className="w-4 h-4" />,
      'pendente': <Clock className="w-4 h-4" />,
      'atrasada': <Clock className="w-4 h-4" />,
      'cancelada': <FileText className="w-4 h-4" />,
    };
    return icons[status] || icons.cancelada;
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
      </div>
    );
  }

  if (!config || !editConfig) {
    return (
      <div className="text-center text-gray-500">
        Erro ao carregar dados financeiros
      </div>
    );
  }

  const totalPendente = transacoes
    .filter(t => t.status === StatusTransacao.PENDENTE || t.status === StatusTransacao.ATRASADA)
    .reduce((acc, t) => acc + t.valor, 0);

  const totalPago = transacoes
    .filter(t => t.status === StatusTransacao.PAGA && (t.tipo === TipoTransacao.ENTRADA_PROJETO || t.tipo === TipoTransacao.OUTRA_RECEITA))
    .reduce((acc, t) => acc + t.valor, 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Financeiro</h1>
        <p className="text-gray-600">Gerencie as configurações e transações do sistema</p>
      </div>

      {/* KPIs Simples */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <p className="text-sm text-gray-600">Total Recebido (Pago)</p>
          <p className="text-2xl font-bold text-gray-900">
            R$ {totalPago.toLocaleString('pt-BR')}
          </p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <p className="text-sm text-gray-600">Total a Receber (Pendente)</p>
          <p className="text-2xl font-bold text-yellow-800">
            R$ {totalPendente.toLocaleString('pt-BR')}
          </p>
        </div>
      </div>

      {/* Grid de Config e Transações */}
      <div className="grid lg:grid-cols-3 gap-6">

        {/* Coluna de Configurações */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Settings className="w-5 h-5" />
              Configurações Globais
            </h3>
            <form onSubmit={handleConfigUpdate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Margem de Lucro Padrão (%)</label>
                <input
                  type="number"
                  step="0.01"
                  value={(editConfig.margem_lucro_padrao * 100).toFixed(2)} // Exibe como porcentagem
                  onChange={(e) => setEditConfig({...editConfig, margem_lucro_padrao: parseFloat(e.target.value) / 100})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Comissão Padrão Vendedor (%)</label>
                <input
                  type="number"
                  step="0.01"
                  value={(editConfig.percentual_comissao_padrao * 100).toFixed(2)} // Exibe como porcentagem
                  onChange={(e) => setEditConfig({...editConfig, percentual_comissao_padrao: parseFloat(e.target.value) / 100})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>
              <button
                type="submit"
                className="w-full px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
              >
                Salvar Configurações
              </button>
            </form>
          </div>
        </div>

        {/* Coluna de Transações */}
        <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-lg font-semibold mb-4">Últimas Transações</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 text-sm font-medium text-gray-600">Descrição</th>
                  <th className="text-left py-3 text-sm font-medium text-gray-600">Valor</th>
                  <th className="text-left py-3 text-sm font-medium text-gray-600">Status</th>
                  <th className="text-left py-3 text-sm font-medium text-gray-600">Vencimento</th>
                </tr>
              </thead>
              <tbody>
                {transacoes.map((t) => (
                  <tr key={t.id} className="border-b border-gray-100">
                    <td className="py-3 text-sm text-gray-900">
                      <p className="font-medium">{t.descricao}</p>
                      <p className="text-xs text-gray-500 capitalize">{t.tipo.replace('_', ' ')}</p>
                    </td>
                    <td className={`py-3 text-sm font-semibold ${(t.tipo.includes('ENTRADA') || t.tipo.includes('RECEITA')) ? 'text-green-600' : 'text-red-600'}`}>
                      {(t.tipo.includes('ENTRADA') || t.tipo.includes('RECEITA')) ? '+' : '-'} R$ {t.valor.toLocaleString('pt-BR')}
                    </td>
                    <td className="py-3">
                      <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full capitalize ${getStatusColor(t.status)}`}>
                        {getStatusIcon(t.status)}
                        {t.status}
                      </span>
                    </td>
                    <td className="py-3 text-sm text-gray-600">
                      {t.data_vencimento ? new Date(t.data_vencimento).toLocaleDateString('pt-BR', {timeZone: 'UTC'}) : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  );
}