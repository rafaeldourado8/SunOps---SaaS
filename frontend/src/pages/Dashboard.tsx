import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import api from '../services/api';
import {TrendingUp, Users, FileText, DollarSign, Target, AlertTriangle, Clock, Briefcase, BarChart3, PieChart} from 'lucide-react';
import toast from 'react-hot-toast';

// --- INTERFACES CORRIGIDAS ---

// Objeto aninhado para Cliente (baseado no schema.py)
interface ShowCliente {
  id: number;
  nome_razao_social: string;
  // Outros campos de cliente se necessário
}

// Objeto aninhado para Usuário (baseado no schema.py)
interface ShowUser {
  id: number;
  name: string;
  email: string;
  role: 'gestor' | 'vendedor' | 'suporte';
}

// Interface para um único KPI (baseado no schema.py)
interface KPI {
  titulo: string;
  valor: string; // O backend envia como string formatada
  percentual_crescimento: number | null;
}

// Interface para um Projeto (baseado no projetos/schema.py)
interface ShowProjeto {
  id: number;
  nome: string;
  status: string;
  valor_total: number;
  cliente: ShowCliente;
  gestor_responsavel: ShowUser;
}

// Interface para o Funil (baseado no dashboards/schema.py)
interface FunilEtapa {
  status: string;
  contagem: number;
  valor_total: number;
}

// Interface para Alertas (baseado no dashboards/schema.py)
interface Alerta {
  tipo: string;
  titulo: string;
  descricao: string;
  link_id: number;
}

// Interface para Pendências (baseado no dashboards/schema.py)
interface Pendencia {
  tipo: string;
  titulo: string;
  descricao: string;
  link_id: number;
}

// Interface principal do Gestor (Corrigida)
interface DashboardGestor {
  kpis: KPI[]; // É uma lista de KPIs
  funil_propostas: FunilEtapa[];
  alertas: Alerta[];
  projetos_recentes: ShowProjeto[];
}

// Interface principal do Vendedor (Corrigida)
interface DashboardVendedor {
  saudacao: string;
  kpis: KPI[]; // É uma lista de KPIs
  meta_percentual: number;
  ranking: number;
  pendencias: Pendencia[];
  meus_projetos: ShowProjeto[];
}

// --- ÍCONES HELPER (Opcional, para deixar bonito) ---
const getKpiIcon = (titulo: string) => {
  if (titulo.toLowerCase().includes('negociação')) return <TrendingUp className="w-8 h-8 text-green-500" />;
  if (titulo.toLowerCase().includes('clientes')) return <Users className="w-8 h-8 text-blue-500" />;
  if (titulo.toLowerCase().includes('projetos')) return <Briefcase className="w-8 h-8 text-purple-500" />;
  if (titulo.toLowerCase().includes('receita') || titulo.toLowerCase().includes('ganhas')) return <DollarSign className="w-8 h-8 text-green-500" />;
  if (titulo.toLowerCase().includes('vendas')) return <FileText className="w-8 h-8 text-blue-500" />;
  if (titulo.toLowerCase().includes('comissão')) return <PieChart className="w-8 h-8 text-purple-500" />;
  return <BarChart3 className="w-8 h-8 text-gray-500" />;
}

// --- COMPONENTE ---

export default function Dashboard() {
  const { user } = useAuthStore();
  const [dashboardData, setDashboardData] = useState<DashboardGestor | DashboardVendedor | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await api.get('/dashboard/');
        setDashboardData(response.data);
      } catch (error) {
        toast.error('Erro ao carregar dados do dashboard');
        console.error('Dashboard error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="text-center text-gray-500">
        Erro ao carregar dados do dashboard
      </div>
    );
  }

  // Renderização para Gestor
  if (user?.role === 'gestor') {
    const data = dashboardData as DashboardGestor;

    return (
      <div className="space-y-6">
        {/* Saudação */}
        <div className="bg-gradient-to-r from-orange-500 to-yellow-500 rounded-2xl p-6 text-white">
          <h1 className="text-2xl font-bold mb-2">Bom dia, {user.name}!</h1>
          <p className="text-orange-100">Aqui está o resumo do seu negócio hoje</p>
        </div>

        {/* KPIs (Renderização dinâmica) */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {data.kpis.map((kpi) => (
            <div key={kpi.titulo} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{kpi.titulo}</p>
                  <p className="text-2xl font-bold text-gray-900">{kpi.valor}</p>
                  {kpi.percentual_crescimento != null && (
                    <p className={`text-xs font-medium ${kpi.percentual_crescimento >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {kpi.percentual_crescimento >= 0 ? '▲' : '▼'} {kpi.percentual_crescimento.toFixed(1)}%
                    </p>
                  )}
                </div>
                {getKpiIcon(kpi.titulo)}
              </div>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Funil de Propostas */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold mb-4">Funil de Propostas</h3>
            <div className="space-y-3">
              {data.funil_propostas.map((item) => (
                <div key={item.status} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900 capitalize">{item.status}</p>
                    <p className="text-sm text-gray-600">{item.contagem} propostas</p>
                  </div>
                  <p className="font-semibold text-gray-900">
                    R$ {item.valor_total.toLocaleString('pt-BR')}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Alertas */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold mb-4">Alertas</h3>
            <div className="space-y-3">
              {data.alertas.length === 0 ? (
                <p className="text-sm text-gray-500">Nenhum alerta no momento.</p>
              ) : (
                data.alertas.map((alerta, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                    <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
                    <div>
                      <p className="font-medium text-gray-900">{alerta.titulo}</p>
                      <p className="text-sm text-gray-600">{alerta.descricao}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Projetos Recentes */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-lg font-semibold mb-4">Projetos Recentes</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 text-sm font-medium text-gray-600">Projeto</th>
                  <th className="text-left py-3 text-sm font-medium text-gray-600">Cliente</th>
                  <th className="text-left py-3 text-sm font-medium text-gray-600">Responsável</th>
                  <th className="text-left py-3 text-sm font-medium text-gray-600">Status</th>
                  <th className="text-left py-3 text-sm font-medium text-gray-600">Valor</th>
                </tr>
              </thead>
              <tbody>
                {data.projetos_recentes.map((projeto) => (
                  <tr key={projeto.id} className="border-b border-gray-100">
                    <td className="py-3 text-sm text-gray-900">{projeto.nome}</td>
                    <td className="py-3 text-sm text-gray-600">{projeto.cliente.nome_razao_social}</td>
                    <td className="py-3 text-sm text-gray-600">{projeto.gestor_responsavel.name}</td>
                    <td className="py-3">
                      <span className="inline-flex px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full capitalize">
                        {projeto.status}
                      </span>
                    </td>
                    <td className="py-3 text-sm text-gray-900">
                      R$ {projeto.valor_total.toLocaleString('pt-BR')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }

  // Renderização para Vendedor
  const data = dashboardData as DashboardVendedor;

  return (
    <div className="space-y-6">
      {/* Saudação */}
      <div className="bg-gradient-to-r from-orange-500 to-yellow-500 rounded-2xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">{data.saudacao}</h1>
        <p className="text-orange-100">Vamos alcançar suas metas hoje!</p>
      </div>

      {/* KPIs Pessoais (Renderização dinâmica) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {data.kpis.map((kpi) => (
          <div key={kpi.titulo} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{kpi.titulo}</p>
                <p className="text-2xl font-bold text-gray-900">{kpi.valor}</p>
              </div>
              {getKpiIcon(kpi.titulo)}
            </div>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Meta e Ranking */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-lg font-semibold mb-4">Minha Performance</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg">
              <div>
                <p className="text-sm text-gray-600">Meta do Mês</p>
                <p className="text-2xl font-bold text-gray-900">{data.meta_percentual}%</p>
              </div>
              <Target className="w-8 h-8 text-green-500" />
            </div>

            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
              <div>
                <p className="text-sm text-gray-600">Ranking</p>
                <p className="text-2xl font-bold text-gray-900">#{data.ranking}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-purple-500" />
            </div>
          </div>
        </div>

        {/* Pendências */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 className="text-lg font-semibold mb-4">Minhas Pendências</h3>
          <div className="space-y-3">
            {data.pendencias.length === 0 ? (
              <p className="text-sm text-gray-500">Nenhuma pendência no momento.</p>
            ) : (
              data.pendencias.map((pendencia, index) => (
                <div key={index} className="flex items-start gap-3 p-3 bg-orange-50 rounded-lg border border-orange-200">
                  <Clock className="w-5 h-5 text-orange-600 mt-0.5" />
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{pendencia.titulo}</p>
                    <p className="text-sm text-gray-600">{pendencia.descricao}</p>
                    {/* <p className="text-xs text-orange-600 mt-1">Prazo: {pendencia.prazo}</p> */}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Meus Projetos */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold mb-4">Meus Projetos</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 text-sm font-medium text-gray-600">Projeto</th>
                <th className="text-left py-3 text-sm font-medium text-gray-600">Cliente</th>
                <th className="text-left py-3 text-sm font-medium text-gray-600">Status</th>
                <th className="text-left py-3 text-sm font-medium text-gray-600">Valor</th>
              </tr>
            </thead>
            <tbody>
              {data.meus_projetos.map((projeto) => (
                <tr key={projeto.id} className="border-b border-gray-100">
                  <td className="py-3 text-sm text-gray-900">{projeto.nome}</td>
                  <td className="py-3 text-sm text-gray-600">{projeto.cliente.nome_razao_social}</td>
                  <td className="py-3">
                    <span className="inline-flex px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full capitalize">
                      {projeto.status}
                    </span>
                  </td>
                  <td className="py-3 text-sm text-gray-900">
                    R$ {projeto.valor_total.toLocaleString('pt-BR')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}