import { useEffect, useState } from 'react';
import {Plus, Users as UsersIcon, Mail, Calendar, Shield} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

// --- INTERFACE CORRIGIDA (baseada em users/schema.py) ---
interface Usuario {
  id: number;
  name: string;
  email: string;
  role: 'gestor' | 'vendedor' | 'suporte';
  // O campo 'created_at' não existe no seu backend (model/schema.py)
}

export default function Usuarios() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  // O schema UserCreate aceita 'suporte' também, mas o frontend só mostra gestor/vendedor
  const [newUsuario, setNewUsuario] = useState({
    name: '',
    email: '',
    password: '',
    role: 'vendedor' as 'gestor' | 'vendedor' | 'suporte'
  });

  const fetchUsuarios = async () => {
    try {
      const response = await api.get('/users/');
      setUsuarios(response.data);
    } catch (error) {
      toast.error('Erro ao carregar usuários');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsuarios();
  }, []);

  const handleCreateUsuario = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/users/', newUsuario);
      toast.success('Usuário criado com sucesso!');
      setShowModal(false);
      setNewUsuario({ name: '', email: '', password: '', role: 'vendedor' });
      fetchUsuarios();
    } catch (any: any) {
      const errorMessage = any.response?.data?.detail || 'Erro ao criar usuário';
      toast.error(errorMessage);
    }
  };

  const getRoleColor = (role: string) => {
    const colors = {
      'gestor': 'bg-purple-100 text-purple-800',
      'vendedor': 'bg-blue-100 text-blue-800',
      'suporte': 'bg-gray-100 text-gray-800',
    };
    return colors[role as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const getRoleIcon = (role: string) => {
    return role === 'gestor' ? Shield : UsersIcon;
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
          <h1 className="text-2xl font-bold text-gray-900">Usuários</h1>
          <p className="text-gray-600">Gerencie os usuários do sistema</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Novo Usuário
        </button>
      </div>

      {/* Usuários Grid (Campos corrigidos) */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {usuarios.map((usuario) => {
          const RoleIcon = getRoleIcon(usuario.role);

          return (
            <div key={usuario.id} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold text-lg">
                      {usuario.name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{usuario.name}</h3>
                    <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full capitalize ${getRoleColor(usuario.role)}`}>
                      <RoleIcon className="w-3 h-3" />
                      {usuario.role}
                    </span>
                  </div>
                </div>
                {/* created_at removido */}
              </div>

              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  <span>{usuario.email}</span>
                </div>
                {/* Bloco 'Criado em' removido */}
              </div>
            </div>
          );
        })}
      </div>

      {usuarios.length === 0 && (
        <div className="text-center py-12">
          <UsersIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">Nenhum usuário encontrado</p>
        </div>
      )}

      {/* Modal Novo Usuário (Formulário parece correto) */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <h2 className="text-xl font-semibold mb-4">Novo Usuário</h2>
            <form onSubmit={handleCreateUsuario} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nome</label>
                <input
                  type="text"
                  value={newUsuario.name}
                  onChange={(e) => setNewUsuario({...newUsuario, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={newUsuario.email}
                  onChange={(e) => setNewUsuario({...newUsuario, email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Senha</label>
                <input
                  type="password"
                  value={newUsuario.password}
                  onChange={(e) => setNewUsuario({...newUsuario, password: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                  minLength={6}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Função</label>
                <select
                  value={newUsuario.role}
                  onChange={(e) => setNewUsuario({...newUsuario, role: e.target.value as 'gestor' | 'vendedor' | 'suporte'})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                >
                  <option value="vendedor">Vendedor</option>
                  <option value="gestor">Gestor</option>
                  <option value="suporte">Suporte</option>
                </select>
              </div>

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
                  Criar Usuário
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}