import { useEffect, useState } from 'react';
import {Plus, Briefcase, DollarSign, Calendar, User, MapPin, Zap} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/authStore';

// --- INTERFACES CORRIGIDAS (baseadas em projetos/schema.py) ---

interface ShowCliente {
  id: number;
  nome_razao_social: string;
}

interface ShowUser {
  id: number;
  name: string;
  role: string;
}

// Interface corrigida para ShowProjeto
interface Projeto {
  id: number;
  nome: string;
  cliente: ShowCliente; // Objeto aninhado
  valor_total: number;
  potencia_kwp: number | null;
  status: string;
  endereco_instalacao: string; // Este campo não está no schema ShowProjeto, mas está no seu frontend.
  descricao: string; // Este campo não está no schema ShowProjeto.
  gestor_responsavel: ShowUser; // Objeto aninhado
  // O campo 'created_at' não existe no seu backend (model/schema.py)
}

// Interface para um Usuário (para o select do modal)
interface Usuario {
  id: number;
  name: string;
  role: 'gestor' | 'vendedor' | 'suporte';
}

// Interface para um Cliente (para o select do modal)
interface Cliente {
  id: number;
  nome_razao_social: string;
  // Adicione outros campos se necessário para o select
}


export default function Projetos() {
  const [projetos, setProjetos] = useState<Projeto[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const { user } = useAuthStore();

  // Estado do novo projeto corrigido (baseado em projetos/schema.py -> ProjetoCreate)
  const [newProjeto, setNewProjeto] = useState({
    nome: '',
    cliente_id: '',
    valor_total: '', // Corrigido de 'valor'
    potencia_kwp: '',
    descricao: '', // Este campo não existe no schema 'ProjetoCreate'
    endereco_instalacao: '', // Este campo não existe no schema 'ProjetoCreate'
    responsavel_id: '' // Corrigido de 'vendedor_id'
  });

  const fetchProjetos = async () => {
    try {
      const response = await api.get('/projetos/');
      setProjetos(response.data);
    } catch (error) {
      toast.error('Erro ao carregar projetos');
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

  const fetchUsuarios = async () => {
    if (user?.role === 'gestor') {
      try {
        const response = await api.get('/users/');
        setUsuarios(response.data);
      } catch (error) {
        toast.error('Erro ao carregar usuários');
      }
    }
  };

  useEffect(() => {
    fetchProjetos();
    fetchClientes();
    fetchUsuarios();
  }, [user?.role]);

  const handleCreateProjeto = async (e: React.FormEvent) => {
    e.preventDefault();

    // Payload corrigido para corresponder ao schema ProjetoCreate
    const payload = {
      nome: newProjeto.nome,
      cliente_id: parseInt(newProjeto.cliente_id),
      valor_total: parseFloat(newProjeto.valor_total),
      potencia_kwp: newProjeto.potencia_kwp ? parseFloat(newProjeto.potencia_kwp) : null,
      responsavel_id: parseInt(newProjeto.responsavel_id),
      // Os campos 'descricao' e 'endereco_instalacao' não estão no schema 'ProjetoCreate'
      // Se você os quer, precisa adicionar no backend
    };

    try {
      await api.post('/projetos/', payload);
      toast.success('Projeto criado com sucesso!');
      setShowModal(false);
      setNewProjeto({ // Resetar o estado
        nome: '',
        cliente_id: '',
        valor_total: '',
        potencia_kwp: '',
        descricao: '',
        endereco_instalacao: '',
        responsavel_id: ''
      });
      fetchProjetos();
    } catch (error) {
      toast.error('Erro ao criar projeto');
    }
  };

  const getStatusColor = (status: string) => {
    const colors = {
      'Em Negociação': 'bg-yellow-100 text-yellow-800',
      'Aprovado': 'bg-blue-100 text-blue-800',
      'Em Análise': 'bg-indigo-100 text-indigo-800',
      'Instalado': 'bg-green-100 text-green-800',
      'Cancelado': 'bg-red-100 text-red-800',
    };
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Projetos</h1>
          <p className="text-gray-600">Acompanhe seus projetos solares</p>
        </div>
        {user?.role === 'gestor' && (
          <button
            onClick={() => setShowModal(true)}
            className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Novo Projeto
          </button>
        )}
      </div>

      {/* Projetos Grid (Campos corrigidos) */}
      <div className="grid gap-6 lg:grid-cols-2">
        {projetos.map((projeto) => (
          <div key={projeto.id} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center">
                  <Briefcase className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{projeto.nome}</h3>
                  <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full capitalize ${getStatusColor(projeto.status)}`}>
                    {projeto.status}
                  </span>
                </div>
              </div>
              {/* created_at removido pois não existe no backend */}
            </div>

            <div className="space-y-3">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>Cliente: <span className="font-medium">{projeto.cliente.nome_razao_social}</span></span>
              </div>

              <div className="flex items-center gap-2 text-sm text-gray-600">
                <DollarSign className="w-4 h-4" />
                <span className="font-semibold text-gray-900">
                  R$ {projeto.valor_total.toLocaleString('pt-BR')}
                </span>
              </div>

              {projeto.potencia_kwp && (
                 <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Zap className="w-4 h-4" />
                  <span>Potência: {projeto.potencia_kwp} kWp</span>
                </div>
              )}

              <div className="flex items-center gap-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>Responsável: {projeto.gestor_responsavel.name}</span>
              </div>

              {/* Os campos 'endereco_instalacao' e 'descricao' não estão no seu schema ShowProjeto.
                Se você quiser exibi-los, precisa adicioná-los no backend.
                Removi as linhas que quebravam o código.
              */}
              {/*
              <div className="flex items-start gap-2 text-sm text-gray-600">
                <MapPin className="w-4 h-4 mt-0.5" />
                <span className="line-clamp-2">{projeto.endereco_instalacao}</span>
              </div>

              <div className="text-sm text-gray-600">
                <p className="line-clamp-3">{projeto.descricao}</p>
              </div>
              */}
            </div>
          </div>
        ))}
      </div>

      {projetos.length === 0 && (
        <div className="text-center py-12">
          <Briefcase className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">Nenhum projeto encontrado</p>
        </div>
      )}

      {/* Modal Novo Projeto (Campos corrigidos) */}
      {showModal && user?.role === 'gestor' && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-lg w-full p-6 max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-semibold mb-4">Novo Projeto</h2>
            <form onSubmit={handleCreateProjeto} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nome do Projeto</label>
                <input
                  type="text"
                  value={newProjeto.nome}
                  onChange={(e) => setNewProjeto({...newProjeto, nome: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Cliente</label>
                <select
                  value={newProjeto.cliente_id}
                  onChange={(e) => setNewProjeto({...newProjeto, cliente_id: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                >
                  <option value="">Selecione um cliente</option>
                  {clientes.map((cliente) => (
                    <option key={cliente.id} value={cliente.id}>
                      {cliente.nome_razao_social}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Responsável</label>
                <select
                  value={newProjeto.responsavel_id}
                  onChange={(e) => setNewProjeto({...newProjeto, responsavel_id: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                >
                  <option value="">Selecione um responsável</option>
                  {/* Filtra por gestor ou vendedor, pois ambos podem ser responsáveis */}
                  {usuarios.filter(u => u.role === 'vendedor' || u.role === 'gestor').map((user) => (
                    <option key={user.id} value={user.id}>
                      {user.name} ({user.role})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Valor Total (R$)</label>
                <input
                  type="number"
                  step="0.01"
                  value={newProjeto.valor_total}
                  onChange={(e) => setNewProjeto({...newProjeto, valor_total: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Potência (kWp)</label>
                <input
                  type="number"
                  step="0.01"
                  value={newProjeto.potencia_kwp}
                  onChange={(e) => setNewProjeto({...newProjeto, potencia_kwp: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder="Ex: 8.54"
                />
              </div>

              {/* Os campos abaixo não existem no seu schema 'ProjetoCreate'.
                Você deve adicioná-los no backend (schema.py e models.py) para poder salvá-los.
                Vou mantê-los aqui comentados.
              */}
              {/*
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Endereço da Instalação</label>
                <textarea
                  value={newProjeto.endereco_instalacao}
                  onChange={(e) => setNewProjeto({...newProjeto, endereco_instalacao: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  rows={3}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Descrição</Tabel>
                <textarea
                  value={newProjeto.descricao}
                  onChange={(e) => setNewProjeto({...newProjeto, descricao: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  rows={4}
                  required
                />
              </div>
              */}

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
                >
                  Criar Projeto
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}