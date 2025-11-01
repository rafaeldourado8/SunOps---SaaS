import React from 'react';
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '@/services/api';
import toast from 'react-hot-toast';
import { ArrowLeft, Save, Loader2, Zap, LayoutGrid, Calendar } from 'lucide-react';
import axios from 'axios'; // <--- 1. IMPORTAR AXIOS

// --- Interfaces ---
interface ShowCliente {
  id: number;
  nome_razao_social: string;
}

interface PropostaItem {
  id: number;
  categoria: string;
  descricao: string;
  quantidade: number;
  custo_unitario: number;
  valor_venda: number;
  impostos: number;
  margem: number;
}

interface ShowProposta {
  id: number;
  nome: string | null;
  potencia_kwp: number | null;
  valor_total: number;
  premissas: Record<string, any> | null;
  cliente: ShowCliente;
  itens: PropostaItem[];
}

interface CatalogoItem {
  id: number;
  equipamento: {
    id: number;
    nome_modelo: string;
    potencia_w: number | null;
    categoria: {
      id: number;
      nome: string;
    };
  };
}

// 2. Interfaces para os dados da sua API Flask
interface CatalogoApiResponse {
  fabricante: string;
  nome_modelo: string;
  potencia_w: number | null;
}

interface DimensionamentoData {
  premissas: Record<string, any>;
  potencia_kwp: number;
  nome_kit: string;
  nome_distribuidor: string;
  custo_kit: number;
  sistema: string;
  topologia: string;
  modulo_id: number | null;
  modulo_potencia: number;
  modulo_qtd: number;
  inversor_id: number | null;
  inversor_qtd: number;
}

export default function PropostaDimensionamento() {
  const { propostaId } = useParams();
  const navigate = useNavigate();

  const [proposta, setProposta] = useState<ShowProposta | null>(null);
  const [loading, setLoading] = useState(true);
  const [savingEtapa1, setSavingEtapa1] = useState(false);
  const [savingEtapa2, setSavingEtapa2] = useState(false);

  // Estados para dropdowns
  const [modulos, setModulos] = useState<CatalogoItem[]>([]);
  const [inversores, setInversores] = useState<CatalogoItem[]>([]);
  const [loadingCatalogo, setLoadingCatalogo] = useState(false);

  const [formData, setFormData] = useState<DimensionamentoData>({
    premissas: { sistema: 'On grid', topologia: 'Tradicional' },
    potencia_kwp: 0,
    nome_kit: '',
    nome_distribuidor: '',
    custo_kit: 0,
    sistema: 'On grid',
    topologia: 'Tradicional',
    modulo_id: null,
    modulo_potencia: 0,
    modulo_qtd: 1,
    inversor_id: null,
    inversor_qtd: 1,
  });

  const [itensEditaveis, setItensEditaveis] = useState<PropostaItem[]>([]);

  // Carrega catálogo do backend
  useEffect(() => {
    // 3. FUNÇÃO MODIFICADA PARA BUSCAR DA API FLASK
    const fetchCatalogo = async () => {
      setLoadingCatalogo(true);
      // Sua API Flask roda na porta 5001
      const catalogoApiUrl = 'http://localhost:5001';

      try {
        // Busca os endpoints /modulos e /inversores da sua API
        const [modulosResponse, inversoresResponse] = await Promise.all([
          axios.get<{ total: number, data: CatalogoApiResponse[] }>(`${catalogoApiUrl}/modulos`),
          axios.get<{ total: number, data: CatalogoApiResponse[] }>(`${catalogoApiUrl}/inversores`)
        ]);

        // 4. Transforma os dados dos MÓDULOS para o formato CatalogoItem
        // Os dados da API são: { fabricante, nome_modelo, potencia_w }
        // O componente React espera: { id, equipamento: { id, nome_modelo, potencia_w, ... } }
        const modulosList: CatalogoItem[] = modulosResponse.data.data.map((item, index) => ({
          id: index + 1, // Usa o índice como ID único
          equipamento: {
            id: index + 1,
            nome_modelo: `${item.fabricante} ${item.nome_modelo}`, // Combina fabricante e modelo
            potencia_w: item.potencia_w,
            categoria: {
              id: 1,
              nome: 'Módulos'
            }
          }
        }));
        
        // 5. Transforma os dados dos INVERSORES para o formato CatalogoItem
        const inversoresList: CatalogoItem[] = inversoresResponse.data.data.map((item, index) => ({
          id: index + 10000, // Usa um índice alto para evitar colisão de ID com módulos
          equipamento: {
            id: index + 10000,
            nome_modelo: `${item.fabricante} ${item.nome_modelo}`,
            potencia_w: item.potencia_w,
            categoria: {
              id: 2,
              nome: 'Inversores'
            }
          }
        }));

        setModulos(modulosList);
        setInversores(inversoresList);
        
      } catch (error) {
        toast.error("Erro ao carregar catálogo da API Python.");
        console.error('Erro:', error);
      } finally {
        setLoadingCatalogo(false);
      }
    };

    fetchCatalogo();
  }, []); // Dependência vazia, roda 1x

  // Carrega proposta
  useEffect(() => {
    const fetchProposta = async () => {
      if (!propostaId) return;
      try {
        const response = await api.get(`/propostas/${propostaId}`);
        setProposta(response.data);
        
        const premissas = response.data.premissas || {};
        
        setFormData((prevFormData) => ({
          ...prevFormData,
          premissas: premissas,
          potencia_kwp: response.data.potencia_kwp || 0,
          sistema: premissas.sistema || 'On grid',
          topologia: premissas.topologia || 'Tradicional',
          nome_kit: premissas.nome_kit || '',
          nome_distribuidor: premissas.nome_distribuidor || '',
        }));
        
        setItensEditaveis(response.data.itens || []);
        
      } catch (error) {
        console.error('Erro ao carregar proposta:', error);
        toast.error('Erro ao carregar proposta.');
        navigate('/app/propostas');
      } finally {
        setLoading(false);
      }
    };

    fetchProposta();
  }, [propostaId, navigate]);

  // Calcula Potência
  useEffect(() => {
    const potenciaW = formData.modulo_potencia * formData.modulo_qtd;
    setFormData(f => ({ ...f, potencia_kwp: potenciaW / 1000 }));
  }, [formData.modulo_potencia, formData.modulo_qtd]);
  
  // Handlers
  const handleModuloChange = (itemId: string) => {
    const id = parseInt(itemId);
    // 6. A lógica de seleção agora funciona, pois os dados estão no formato correto
    const item = modulos.find(m => m.id === id); 
    if (item) {
      setFormData({
        ...formData,
        modulo_id: id,
        modulo_potencia: item.equipamento.potencia_w || 0,
      });
    }
  };

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSaveDimensionamento = async () => {
    setSavingEtapa1(true);
    try {
      const response = await api.put(
        `/propostas/${propostaId}/dimensionamento`,
        formData
      );
      setProposta(response.data); 
      setItensEditaveis(response.data.itens || []);
      toast.success('Etapa 1 salva! Custos gerados.');
    } catch (error: any) {
      console.error('Erro ao salvar dimensionamento:', error);
      toast.error(error.response?.data?.detail || 'Erro ao salvar dimensionamento.');
    } finally {
      setSavingEtapa1(false);
    }
  };

  const handleItemChange = (index: number, campo: keyof PropostaItem, valor: string | number) => {
    const novosItens = [...itensEditaveis];
    novosItens[index] = {
      ...novosItens[index],
      [campo]: typeof valor === 'string' ? parseFloat(valor) || 0 : valor,
    };
    setItensEditaveis(novosItens);
  };
  
  const valorTotalCalculado = itensEditaveis.reduce((acc, item) => 
    acc + (Number(item.valor_venda) * Number(item.quantidade)), 0
  );
  
  const handleSaveCustosEProsseguir = async () => {
    setSavingEtapa2(true);
    try {
      const payload = {
        itens: itensEditaveis.map(item => ({
          categoria: item.categoria,
          descricao: item.descricao,
          quantidade: Number(item.quantidade),
          custo_unitario: Number(item.custo_unitario),
          valor_venda: Number(item.valor_venda),
          impostos: Number(item.impostos) || 0,
          margem: Number(item.margem) || 0,
        })),
        valor_total: valorTotalCalculado,
      };

      await api.put(`/propostas/${propostaId}/custos`, payload);
      toast.success('Custos salvos! Prosseguindo...');
      navigate(`/app/propostas/${propostaId}/preview`);

    } catch (error: any) {
      console.error('Erro ao salvar custos:', error);
      toast.error(error.response?.data?.detail || 'Erro ao salvar custos.');
    } finally {
      setSavingEtapa2(false);
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
    return <div className="p-8 text-center">Proposta não encontrada.</div>;
  }
  
  const areaUtil = (formData.modulo_qtd * 2.5).toFixed(1);
  const geracaoMensal = (formData.potencia_kwp * 130).toFixed(0);

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
            {proposta.nome || `Proposta - ${proposta.cliente.nome_razao_social}`}
          </h1>
          <p className="text-gray-600">Cliente: {proposta.cliente.nome_razao_social}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        
        {/* Etapa 1 */}
        <div className="lg:col-span-1 bg-white p-6 rounded-xl shadow-sm border border-gray-100 space-y-4 sticky top-6">
          <h2 className="text-lg font-semibold">Etapa 1: Kit e Premissas</h2>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nome do Kit (Opcional)</label>
            <input
              type="text"
              name="nome_kit"
              value={formData.nome_kit}
              onChange={handleFormChange}
              placeholder="Ex: KIT SOLAR 2.80KWP"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nome do distribuidor</label>
            <input
              type="text"
              name="nome_distribuidor"
              value={formData.nome_distribuidor}
              onChange={handleFormChange}
              placeholder="Nome do distribuidor..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Custo do Kit (R$)</label>
            <input
              type="number"
              name="custo_kit"
              value={formData.custo_kit}
              onChange={(e) => setFormData({...formData, custo_kit: parseFloat(e.target.value) || 0})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          
          {/* Módulo */}
          <div className="flex items-end gap-2">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">Módulo</label>
              <select
                value={formData.modulo_id || ''}
                onChange={(e) => handleModuloChange(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                disabled={loadingCatalogo}
              >
                <option value="">
                  {loadingCatalogo ? 'Carregando...' : 'Selecione o módulo'}
                </option>
                {/* 7. O Dropdown agora é populado com os dados da API Flask */}
                {modulos.map(m => (
                  <option key={m.id} value={m.id}>
                    {m.equipamento.nome_modelo} - {m.equipamento.potencia_w}W
                  </option>
                ))}
              </select>
            </div>
            <div className="w-20">
              <label className="block text-sm font-medium text-gray-700 mb-1">Qtd</label>
              <input
                type="number"
                value={formData.modulo_qtd}
                onChange={(e) => setFormData({...formData, modulo_qtd: parseInt(e.target.value) || 1})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                min="1"
              />
            </div>
          </div>
          
          {/* Inversor */}
          <div className="flex items-end gap-2">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">Inversor</label>
              <select
                value={formData.inversor_id || ''}
                onChange={(e) => setFormData({...formData, inversor_id: parseInt(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                disabled={loadingCatalogo}
              >
                <option value="">
                  {loadingCatalogo ? 'Carregando...' : 'Selecione o inversor'}
                </option>
                {/* 7. O Dropdown agora é populado com os dados da API Flask */}
                {inversores.map(i => (
                  <option key={i.id} value={i.id}>
                    {i.equipamento.nome_modelo} - {((i.equipamento.potencia_w || 0)/1000).toFixed(1)}kW
                  </option>
                ))}
              </select>
            </div>
            <div className="w-20">
              <label className="block text-sm font-medium text-gray-700 mb-1">Qtd</label>
              <input
                type="number"
                value={formData.inversor_qtd}
                onChange={(e) => setFormData({...formData, inversor_qtd: parseInt(e.target.value) || 1})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                min="1"
              />
            </div>
          </div>

          <div className="bg-orange-50 p-3 rounded-lg text-center">
            <span className="text-sm text-gray-600">Potência Total</span>
            <p className="text-xl font-bold text-orange-600">{formData.potencia_kwp.toFixed(2)} kWp</p>
          </div>

          <button
            onClick={handleSaveDimensionamento}
            disabled={savingEtapa1}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 disabled:opacity-50"
          >
            {savingEtapa1 ? <Loader2 className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
            {itensEditaveis.length > 0 ? 'Recalcular Custos' : 'Gerar Custos'}
          </button>
        </div>

        {/* Etapa 2 */}
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-4">
             <h2 className="text-lg font-semibold">Etapa 2: Custos e Preço de Venda</h2>
             <div className="flex flex-wrap gap-4 text-sm">
                <div className="flex items-center gap-1 text-gray-600">
                  <Zap className="w-4 h-4 text-orange-500" />
                  Potência: <span className="font-semibold text-gray-900">{formData.potencia_kwp.toFixed(2)} kWp</span>
                </div>
                <div className="flex items-center gap-1 text-gray-600">
                  <LayoutGrid className="w-4 h-4 text-orange-500" />
                  Área útil: <span className="font-semibold text-gray-900">{areaUtil} m²</span>
                </div>
                 <div className="flex items-center gap-1 text-gray-600">
                  <Calendar className="w-4 h-4 text-orange-500" />
                  Geração: <span className="font-semibold text-gray-900">{geracaoMensal} kWh/mês</span>
                </div>
             </div>
          </div>
          
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg mb-4">
            <span className="font-semibold text-gray-900">Preço de Venda</span>
            <span className="text-xl font-bold text-gray-900">
              R$ {valorTotalCalculado.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2 px-2 text-sm font-medium text-gray-600">Categoria</th>
                  <th className="text-left py-2 px-2 text-sm font-medium text-gray-600">Item</th>
                  <th className="text-left py-2 px-2 text-sm font-medium text-gray-600 w-20">Qtd</th>
                  <th className="text-left py-2 px-2 text-sm font-medium text-gray-600 w-32">Valores (R$)</th>
                </tr>
              </thead>
              <tbody>
                {itensEditaveis.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="text-center py-8 text-gray-500">
                      Salve a Etapa 1 para gerar os custos.
                    </td>
                  </tr>
                ) : (
                  itensEditaveis.map((item, index) => (
                    <tr key={item.id || index} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-1 px-2 text-sm">{item.categoria}</td>
                      <td className="py-1 px-2 text-sm">{item.descricao}</td>
                      <td className="py-1 px-2">
                        <input
                          type="number"
                          value={item.quantidade}
                          onChange={(e) => handleItemChange(index, 'quantidade', e.target.value)}
                          className="w-full px-2 py-1 border border-gray-200 rounded-md"
                        />
                      </td>
                      <td className="py-1 px-2">
                         <input
                          type="number"
                          step="0.01"
                          value={item.valor_venda}
                          onChange={(e) => handleItemChange(index, 'valor_venda', e.target.value)}
                          className="w-full px-2 py-1 border border-gray-200 rounded-md"
                        />
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          
          {itensEditaveis.length > 0 && (
            <div className="mt-6 flex justify-end">
              <button
                onClick={handleSaveCustosEProsseguir}
                disabled={savingEtapa2}
                className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
              >
                {savingEtapa2 ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Salvar e Prosseguir'}
              </button>
            </div>
          )}
          
        </div>
      </div>
    </div>
  );
}