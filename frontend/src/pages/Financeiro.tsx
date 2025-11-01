import { useEffect, useState } from 'react';
import {
  DollarSign,
  TrendingUp,
  Settings,
  FileText,
  CheckCircle,
  Clock,
  Archive, // Novo ícone
  Calculator, // Novo ícone
  BarChart, // Novo ícone
  Loader2, // Novo ícone
  AlertTriangle, // Novo ícone
} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

// --- INTERFACES EXISTENTES (baseadas em financeiro/schema.py) ---

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

// --- NOVAS INTERFACES (baseadas em financeiro/schema.py) ---

type Tab = 'visao_geral' | 'premissas' | 'calculadora';

interface ShowPremissaFaixa {
  id: number;
  nome_faixa: string;
  potencia_min: number;
  potencia_max: number;
  preco_unitario: number; // Decimal vira number no TS
}

interface ShowPremissaPorRegiao {
  id: number;
  regiao: string;
  aliquota_imposto: number;
}

interface ShowPremissa {
  id: number;
  nome: string;
  descricao: string | null;
  data_vigencia_inicio: string; // date vira string
  data_vigencia_fim: string; // date vira string
  ativa: boolean;
  faixas: ShowPremissaFaixa[];
  regioes: ShowPremissaPorRegiao[];
}

interface CalculoPrecosRequest {
  potencia_kw: number;
  regiao: string;
  data: string; // YYYY-MM-DD
  premissa_id: number | null;
  custos_adicionais: number;
  margem_lucro_override: number | null;
  comissao_override: number | null;
  imposto_override: number | null;
}

interface CalculoPrecosResponse {
  potencia_solicitada_kw: number;
  regiao: string;
  data_calculo: string;
  premissa_usada_id: number;
  premissa_usada_nome: string;
  faixa_aplicada_nome: string;
  preco_unitario_wp: number;
  preco_base: number;
  custos_adicionais: number;
  subtotal_custos: number;
  margem_lucro_percentual: number;
  margem_lucro_valor: number;
  comissao_percentual: number;
  comissao_valor: number;
  subtotal_sem_imposto: number;
  imposto_percentual: number;
  imposto_valor: number;
  preco_final: number;
  detalhes: Record<string, any>;
}

// --- COMPONENTE ---

export default function Financeiro() {
  const [activeTab, setActiveTab] = useState<Tab>('visao_geral');

  // Estado da Visão Geral
  const [config, setConfig] = useState<ConfiguracaoFinanceira | null>(null);
  const [transacoes, setTransacoes] = useState<Transacao[]>([]);
  const [loadingVisaoGeral, setLoadingVisaoGeral] = useState(true);
  const [editConfig, setEditConfig] = useState<ConfiguracaoFinanceira | null>(null);
  
  // Estado das Premissas
  const [premissas, setPremissas] = useState<ShowPremissa[]>([]);
  const [loadingPremissas, setLoadingPremissas] = useState(false);

  // Estado da Calculadora
  const [calculoRequest, setCalculoRequest] = useState<CalculoPrecosRequest>({
    potencia_kw: 5.5,
    regiao: 'SP',
    data: new Date().toISOString().split('T')[0], // Hoje
    premissa_id: null,
    custos_adicionais: 0,
    margem_lucro_override: null,
    comissao_override: null,
    imposto_override: null,
  });
  const [calculoResponse, setCalculoResponse] = useState<CalculoPrecosResponse | null>(null);
  const [loadingCalculo, setLoadingCalculo] = useState(false);


  // --- CARREGAMENTO DE DADOS ---

  const fetchVisaoGeralData = async () => {
    setLoadingVisaoGeral(true);
    try {
      const [configResponse, transacoesResponse] = await Promise.all([
        api.get('/financeiro/configuracoes'),
        api.get('/financeiro/transacoes')
      ]);

      setConfig(configResponse.data);
      setEditConfig(configResponse.data);
      setTransacoes(transacoesResponse.data);

    } catch (error) {
      toast.error('Erro ao carregar dados financeiros');
    } finally {
      setLoadingVisaoGeral(false);
    }
  };
  
  const fetchPremissasData = async () => {
    // Evita recarregar se já tiver os dados
    if (premissas.length > 0) return; 

    setLoadingPremissas(true);
    try {
      const response = await api.get('/financeiro/premissas');
      setPremissas(response.data);
    } catch (error) {
      toast.error('Erro ao carregar premissas de preço');
    } finally {
      setLoadingPremissas(false);
    }
  };

  // Carrega Visão Geral no mount
  useEffect(() => {
    fetchVisaoGeralData();
  }, []);

  // Carrega dados das outras abas quando ativadas
  useEffect(() => {
    if (activeTab === 'premissas' || activeTab === 'calculadora') {
      fetchPremissasData();
    }
  }, [activeTab]);


  // --- HANDLERS (VISÃO GERAL) ---

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
  
  // --- HANDLERS (CALCULADORA) ---
  
  const handleCalculoRequestChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    // Converte valores para número ou nulo
    const formatValue = (val: string) => {
      if (val === '') return null;
      if (['potencia_kw', 'custos_adicionais', 'margem_lucro_override', 'comissao_override', 'imposto_override'].includes(name)) {
        return parseFloat(val);
      }
      if (name === 'premissa_id') {
        return val === "null" ? null : parseInt(val);
      }
      return val;
    };
    
    // Converte % para decimal em overrides
    let finalValue: any = formatValue(value);
    if (['margem_lucro_override', 'comissao_override', 'imposto_override'].includes(name) && finalValue) {
      finalValue = finalValue / 100;
    }

    setCalculoRequest(prev => ({
      ...prev,
      [name]: finalValue
    }));
  };
  
  const handleCalculoSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingCalculo(true);
    setCalculoResponse(null);
    
    try {
      const response = await api.post('/financeiro/calcular-preco', calculoRequest);
      setCalculoResponse(response.data);
      toast.success('Cálculo realizado com sucesso!');
    } catch (error: any) {
      const detail = error.response?.data?.detail || 'Erro ao calcular preço.';
      toast.error(detail);
      console.error(error);
    } finally {
      setLoadingCalculo(false);
    }
  };
  
  // Helper para formatar data (ex: 2024-10-31)
  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('pt-BR', {timeZone: 'UTC'});
    } catch (e) {
      return 'Data inválida';
    }
  };

  // Helper para formatar moeda
  const formatCurrency = (value: number) => {
    return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  };
  
  // --- RENDERIZAÇÃO ---

  const renderLoading = () => (
    <div className="flex items-center justify-center h-64">
      <Loader2 className="w-12 h-12 animate-spin text-orange-500" />
    </div>
  );

  const renderVisaoGeral = () => {
    if (loadingVisaoGeral) return renderLoading();
    if (!config || !editConfig) {
      return <div className="text-center text-gray-500">Erro ao carregar dados financeiros</div>;
    }

    const totalPendente = transacoes
      .filter(t => t.status === StatusTransacao.PENDENTE || t.status === StatusTransacao.ATRASADA)
      .reduce((acc, t) => acc + t.valor, 0);

    const totalPago = transacoes
      .filter(t => t.status === StatusTransacao.PAGA && (t.tipo === TipoTransacao.ENTRADA_PROJETO || t.tipo === TipoTransacao.OUTRA_RECEITA))
      .reduce((acc, t) => acc + t.valor, 0);

    return (
      <div className="space-y-6">
        {/* KPIs Simples */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <p className="text-sm text-gray-600">Total Recebido (Pago)</p>
            <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalPago)}</p>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <p className="text-sm text-gray-600">Total a Receber (Pendente)</p>
            <p className="text-2xl font-bold text-yellow-800">{formatCurrency(totalPendente)}</p>
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
                    value={(editConfig.margem_lucro_padrao * 100).toFixed(2)}
                    onChange={(e) => setEditConfig({...editConfig, margem_lucro_padrao: parseFloat(e.target.value) / 100})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Comissão Padrão Vendedor (%)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={(editConfig.percentual_comissao_padrao * 100).toFixed(2)}
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
                        {(t.tipo.includes('ENTRADA') || t.tipo.includes('RECEITA')) ? '+' : '-'} {formatCurrency(t.valor)}
                      </td>
                      <td className="py-3">
                        <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full capitalize ${getStatusColor(t.status)}`}>
                          {getStatusIcon(t.status)}
                          {t.status}
                        </span>
                      </td>
                      <td className="py-3 text-sm text-gray-600">
                        {t.data_vencimento ? formatDate(t.data_vencimento) : 'N/A'}
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
  };

  const renderPremissas = () => {
    if (loadingPremissas) return renderLoading();
    
    return (
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold mb-4">Premissas de Preço Cadastradas</h3>
        
        {premissas.length === 0 && (
          <div className="text-center py-12">
            <Archive className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">Nenhuma premissa de preço encontrada.</p>
            {/* Adicionar botão de "Criar Premissa" aqui quando o modal estiver pronto */}
          </div>
        )}
        
        <div className="space-y-4">
          {premissas.map(premissa => (
            <div key={premissa.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-semibold text-gray-900">{premissa.nome}</h4>
                  <p className="text-sm text-gray-600">
                    Vigência: {formatDate(premissa.data_vigencia_inicio)} a {formatDate(premissa.data_vigencia_fim)}
                  </p>
                </div>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${premissa.ativa ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                  {premissa.ativa ? 'Ativa' : 'Inativa'}
                </span>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div>
                  <h5 className="text-sm font-medium mb-2">Faixas de Preço (por kWp)</h5>
                  <ul className="space-y-1 text-sm">
                    {premissa.faixas.sort((a,b) => a.potencia_min - b.potencia_min).map(faixa => (
                      <li key={faixa.id} className="flex justify-between p-2 bg-gray-50 rounded">
                        <span>{faixa.nome_faixa} ({faixa.potencia_min}kW - {faixa.potencia_max}kW)</span>
                        <span className="font-medium">{formatCurrency(faixa.preco_unitario)} / Wp</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h5 className="text-sm font-medium mb-2">Impostos por Região</h5>
                   <ul className="space-y-1 text-sm">
                    {premissa.regioes.map(regiao => (
                      <li key={regiao.id} className="flex justify-between p-2 bg-gray-50 rounded">
                        <span>Região: {regiao.regiao.toUpperCase()}</span>
                        <span className="font-medium">{(regiao.aliquota_imposto * 100).toFixed(2)}%</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  const renderCalculadora = () => {
    return (
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Formulário da Calculadora */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-lg font-semibold mb-4">Simular Preço de Venda</h3>
          <form onSubmit={handleCalculoSubmit} className="space-y-4">
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Potência (kWp)</label>
                <input
                  type="number"
                  step="0.01"
                  name="potencia_kw"
                  value={calculoRequest.potencia_kw}
                  onChange={handleCalculoRequestChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Região (UF)</label>
                <input
                  type="text"
                  name="regiao"
                  value={calculoRequest.regiao}
                  onChange={handleCalculoRequestChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  placeholder="Ex: SP, MG, RJ"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Data do Cálculo</label>
                <input
                  type="date"
                  name="data"
                  value={calculoRequest.data}
                  onChange={handleCalculoRequestChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  required
                />
              </div>
            </div>
            
            <hr/>
            <h4 className="text-base font-medium">Parâmetros Opcionais</h4>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Usar Premissa Específica</label>
              <select
                name="premissa_id"
                value={calculoRequest.premissa_id || "null"}
                onChange={handleCalculoRequestChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                disabled={loadingPremissas}
              >
                <option value="null">Automático (ativa e vigente na data)</option>
                {premissas.map(p => (
                  <option key={p.id} value={p.id}>{p.nome}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Custos Adicionais (R$)</label>
              <input
                type="number"
                step="0.01"
                name="custos_adicionais"
                value={calculoRequest.custos_adicionais}
                onChange={handleCalculoRequestChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Margem Override (%)</label>
                <input
                  type="number"
                  step="0.01"
                  name="margem_lucro_override"
                  placeholder="Padrão"
                  onChange={handleCalculoRequestChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Comissão Override (%)</label>
                <input
                  type="number"
                  step="0.01"
                  name="comissao_override"
                  placeholder="Padrão"
                  onChange={handleCalculoRequestChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Imposto Override (%)</label>
                <input
                  type="number"
                  step="0.01"
                  name="imposto_override"
                  placeholder="Padrão"
                  onChange={handleCalculoRequestChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loadingCalculo}
              className="w-full px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors flex items-center justify-center gap-2"
            >
              {loadingCalculo ? <Loader2 className="w-5 h-5 animate-spin" /> : <Calculator className="w-5 h-5" />}
              Calcular Preço
            </button>
          </form>
        </div>
        
        {/* Resultado da Calculadora */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
           <h3 className="text-lg font-semibold mb-4">Resultado da Simulação</h3>
           {loadingCalculo && renderLoading()}
           
           {!loadingCalculo && !calculoResponse && (
             <div className="text-center py-12">
               <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
               <p className="text-gray-500">Preencha o formulário e clique em "Calcular Preço" para ver o resultado.</p>
             </div>
           )}
           
           {calculoResponse && (
             <div className="space-y-3">
               <div className="text-center p-4 bg-orange-50 border border-orange-200 rounded-lg">
                 <p className="text-sm text-orange-700">Preço Final de Venda</p>
                 <p className="text-3xl font-bold text-orange-600">{formatCurrency(calculoResponse.preco_final)}</p>
               </div>
               
               <div className="space-y-2 text-sm">
                 <h5 className="font-medium text-base mt-4 mb-2">Detalhes do Cálculo</h5>
                 <div className="flex justify-between"><span className="text-gray-600">Premissa usada:</span> <span className="font-medium">{calculoResponse.premissa_usada_nome} (ID: {calculoResponse.premissa_usada_id})</span></div>
                 <div className="flex justify-between"><span className="text-gray-600">Faixa aplicada:</span> <span className="font-medium">{calculoResponse.faixa_aplicada_nome}</span></div>
                 <div className="flex justify-between"><span className="text-gray-600">Preço Unitário (Wp):</span> <span className="font-medium">{formatCurrency(calculoResponse.preco_unitario_wp)}</span></div>
                 
                 <hr className="my-2"/>
                 
                 <div className="flex justify-between"><span className="text-gray-600">(+) Preço Base:</span> <span>{formatCurrency(calculoResponse.preco_base)}</span></div>
                 <div className="flex justify-between"><span className="text-gray-600">(+) Custos Adicionais:</span> <span>{formatCurrency(calculoResponse.custos_adicionais)}</span></div>
                 <div className="flex justify-between font-semibold"><span className="text-gray-800">(=) Subtotal de Custos:</span> <span>{formatCurrency(calculoResponse.subtotal_custos)}</span></div>
                 
                 <hr className="my-2"/>
                 
                 <div className="flex justify-between"><span className="text-gray-600">(+) Margem de Lucro ({(calculoResponse.margem_lucro_percentual * 100).toFixed(2)}%):</span> <span>{formatCurrency(calculoResponse.margem_lucro_valor)}</span></div>
                 <div className="flex justify-between"><span className="text-gray-600">(+) Comissão ({(calculoResponse.comissao_percentual * 100).toFixed(2)}%):</span> <span>{formatCurrency(calculoResponse.comissao_valor)}</span></div>
                 <div className="flex justify-between font-semibold"><span className="text-gray-800">(=) Subtotal s/ Imposto:</span> <span>{formatCurrency(calculoResponse.subtotal_sem_imposto)}</span></div>
                 
                 <hr className="my-2"/>
                 
                 <div className="flex justify-between"><span className="text-gray-600">(+) Imposto ({(calculoResponse.imposto_percentual * 100).toFixed(2)}%):</span> <span>{formatCurrency(calculoResponse.imposto_valor)}</span></div>
                 <div className="flex justify-between font-bold text-lg text-green-600"><span className="">(=) PREÇO FINAL:</span> <span>{formatCurrency(calculoResponse.preco_final)}</span></div>
               </div>
             </div>
           )}
        </div>
      </div>
    );
  };
  
  // --- RENDERIZAÇÃO PRINCIPAL (COM ABAS) ---

  const tabs = [
    { id: 'visao_geral', nome: 'Visão Geral', icon: BarChart },
    { id: 'premissas', nome: 'Premissas de Preço', icon: Archive },
    { id: 'calculadora', nome: 'Calculadora', icon: Calculator },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Financeiro</h1>
        <p className="text-gray-600">Gerencie as configurações, premissas e transações do sistema</p>
      </div>

      {/* Navegação em Abas */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-6" aria-label="Tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as Tab)}
              className={`flex items-center gap-2 whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-orange-500 text-orange-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <tab.icon className="w-5 h-5" />
              {tab.nome}
            </button>
          ))}
        </nav>
      </div>

      {/* Conteúdo da Aba Ativa */}
      <div>
        {activeTab === 'visao_geral' && renderVisaoGeral()}
        {activeTab === 'premissas' && renderPremissas()}
        {activeTab === 'calculadora' && renderCalculadora()}
      </div>
    </div>
  );
}