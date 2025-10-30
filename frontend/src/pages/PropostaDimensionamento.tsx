import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import toast from 'react-hot-toast';
import { ArrowLeft, Save, Loader2 } from 'lucide-react';

// Você precisará definir as interfaces baseadas nos seus schemas
// (Ex: de app/core/sales/propostas/schema.py)

interface ShowProposta {
  id: number;
  nome: string | null;
  potencia_kwp: number | null;
  valor_total: number;
  premissas: Record<string, any> | null;
  cliente: {
    nome_razao_social: string;
  };
  itens: PropostaItem[];
}

interface PropostaItem {
  id: number;
  categoria: string;
  descricao: string;
  quantidade: number;
  custo_unitario: number;
  valor_venda: number;
}

// Interface para o formulário da Etapa 1
interface DimensionamentoData {
  premissas: Record<string, any>;
  potencia_kwp: number;
  kit_id: number | null;
}

export default function PropostaDimensionamento() {
  const { propostaId } = useParams();
  const navigate = useNavigate();

  const [proposta, setProposta] = useState<ShowProposta | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // Estados para os formulários
  // (Você deve preenchê-los com os dados da 'proposta' quando ela carregar)
  const [formData, setFormData] = useState<DimensionamentoData>({
    premissas: { sistema: 'On grid', topologia: 'Tradicional' },
    potencia_kwp: 0,
    kit_id: null,
  });

  useEffect(() => {
    const fetchProposta = async () => {
      if (!propostaId) return;
      try {
        const response = await api.get(`/propostas/${propostaId}`);
        setProposta(response.data);
        
        // Preenche o formulário com dados existentes
        setFormData({
          premissas: response.data.premissas || { sistema: 'On grid', topologia: 'Tradicional' },
          potencia_kwp: response.data.potencia_kwp || 0,
          kit_id: null, // Você precisará de lógica para extrair o kit_id dos itens
        });
        
      } catch (error) {
        toast.error('Erro ao carregar proposta.');
        navigate('/app/propostas');
      } finally {
        setLoading(false);
      }
    };
    fetchProposta();
  }, [propostaId, navigate]);

  const handleSaveDimensionamento = async () => {
    setSaving(true);
    try {
      // Endpoint da Etapa 1 (PUT /propostas/{id}/dimensionamento)
      const response = await api.put(
        `/propostas/${propostaId}/dimensionamento`,
        formData
      );
      setProposta(response.data); // Atualiza a proposta com os itens de custo gerados
      toast.success('Etapa 1 salva! Custos gerados.');
    } catch (error) {
      toast.error('Erro ao salvar dimensionamento.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-12 h-12 animate-spin text-orange-500" />
      </div>
    );
  }

  if (!proposta) {
    return <div>Proposta não encontrada.</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate('/app/propostas')}
          className="p-2 rounded-md text-gray-500 hover:bg-gray-100"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {proposta.nome || `Dimensionamento - ${proposta.cliente.nome_razao_social}`}
          </h1>
          <p className="text-gray-600">Proposta ID: {proposta.id}</p>
        </div>
      </div>

      {/* Conteúdo da Página (baseado na sua UI) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Etapa 1: Dimensionamento */}
        <div className="lg:col-span-1 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-lg font-semibold mb-4">Etapa 1: Kit e Premissas</h2>
          {/* Adicione os campos do formulário (Kit, Potência, Premissas) aqui */}
          <div className="space-y-4">
             <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Potência (kWp)</label>
                <input
                  type="number"
                  value={formData.potencia_kwp}
                  onChange={(e) => setFormData({...formData, potencia_kwp: parseFloat(e.target.value) || 0})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            {/* ... outros campos ... */}
            <button
              onClick={handleSaveDimensionamento}
              disabled={saving}
              className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 disabled:opacity-50"
            >
              {saving ? <Loader2 className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
              Salvar Etapa 1 e Gerar Custos
            </button>
          </div>
        </div>

        {/* Etapa 2: Custos */}
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-lg font-semibold mb-4">Etapa 2: Custos e Preço de Venda</h2>
          {/* Tabela de custos (proposta.itens) aparecerá aqui */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2 text-sm font-medium text-gray-600">Descrição</th>
                  <th className="text-left py-2 text-sm font-medium text-gray-600">Valor (Venda)</th>
                </tr>
              </thead>
              <tbody>
                {proposta.itens.length === 0 ? (
                  <tr>
                    <td colSpan={2} className="text-center py-4 text-gray-500">
                      Salve a Etapa 1 para gerar os custos.
                    </td>
                  </tr>
                ) : (
                  proposta.itens.map((item) => (
                    <tr key={item.id} className="border-b border-gray-100">
                      <td className="py-2 text-sm text-gray-900">{item.descricao}</td>
                      <td className="py-2 text-sm text-gray-900">
                        {/* Adicione um <input> aqui para tornar editável */}
                        R$ {item.valor_venda.toLocaleString('pt-BR')}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  );
}