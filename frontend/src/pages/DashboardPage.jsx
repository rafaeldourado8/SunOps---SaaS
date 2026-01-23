// src/pages/DashboardPage.jsx
import { useState, useEffect } from 'react';
import { 
  FiUsers, 
  FiFileText, 
  FiCheckCircle, 
  FiDollarSign 
} from 'react-icons/fi';
import { clientesApi, propostasApi } from '../services/api';
import toast from 'react-hot-toast';

const DashboardPage = () => {
  const [stats, setStats] = useState({
    totalClientes: 0,
    propostasAtivas: 0,
    contratosFechados: 0,
    receitaTotal: 0,
  });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [clientesRes, propostasRes] = await Promise.all([
        clientesApi.getAll(),
        propostasApi.getAll(),
      ]);

      const clientes = clientesRes.data;
      const propostas = propostasRes.data;

      const propostasAtivas = propostas.filter(p => 
        p.status === 'ENVIADA' || p.status === 'APROVADA'
      ).length;

      const contratosFechados = propostas.filter(p => 
        p.status === 'APROVADA'
      ).length;

      const receitaTotal = propostas
        .filter(p => p.status === 'APROVADA')
        .reduce((sum, p) => sum + (p.valor_total || 0), 0);

      setStats({
        totalClientes: clientes.length,
        propostasAtivas,
        contratosFechados,
        receitaTotal,
      });
    } catch (error) {
      toast.error('Erro ao carregar estatísticas');
    }
  };

  const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-400 mb-1">{label}</p>
          <p className={`text-2xl font-bold ${color}`}>
            {typeof value === 'number' && value.toLocaleString('pt-BR', {
              style: 'currency',
              currency: 'BRL',
            })}
            {typeof value !== 'number' && value}
          </p>
        </div>
        <div className={`p-3 rounded-lg ${color.replace('text', 'bg').replace('-600', '-500/20')}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">Visão geral do sistema SunOPS</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          icon={FiUsers}
          label="Total de Clientes"
          value={stats.totalClientes}
          color="text-blue-400"
        />
        <StatCard
          icon={FiFileText}
          label="Propostas Ativas"
          value={stats.propostasAtivas}
          color="text-solar-400"
        />
        <StatCard
          icon={FiCheckCircle}
          label="Contratos Fechados"
          value={stats.contratosFechados}
          color="text-green-400"
        />
        <StatCard
          icon={FiDollarSign}
          label="Receita Total"
          value={stats.receitaTotal}
          color="text-emerald-400"
        />
      </div>

      {/* Gráficos Placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Propostas por Status
          </h3>
          <div className="h-64 flex items-center justify-center text-gray-500">
            <p>Gráfico de pizza aqui</p>
          </div>
        </div>
        
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Receita Mensal
          </h3>
          <div className="h-64 flex items-center justify-center text-gray-500">
            <p>Gráfico de linha aqui</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;