import { useEffect, useState } from 'react';
import {Search, Plus, Mail, Phone, MapPin, User, FileText} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

// --- INTERFACES CORRIGIDAS (baseadas em clientes/schema.py) ---

// Enum para TipoCliente
enum TipoCliente {
  PESSOA_FISICA = "pessoa_fisica",
  PESSOA_JURIDICA = "pessoa_juridica",
}

// Interface corrigida para ShowCliente
interface Cliente {
  id: number;
  nome_razao_social: string;
  tipo: TipoCliente;
  documento: string;
  email: string | null;
  telefone: string | null;
  endereco: string | null;
  // O campo 'created_at' não existe no seu backend (model/schema.py)
}

export default function Clientes() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showModal, setShowModal] = useState(false);

  // Estado do novo cliente corrigido (baseado em clientes/schema.py -> ClienteCreate)
  const [newCliente, setNewCliente] = useState({
    nome_razao_social: '',
    tipo: TipoCliente.PESSOA_FISICA,
    documento: '',
    email: '',
    telefone: '',
    endereco: ''
  });

  const fetchClientes = async (query = '') => {
    setLoading(true);
    try {
      const params = query ? { q: query } : {};
      const response = await api.get('/clientes/', { params });
      setClientes(response.data);
    } catch (error) {
      toast.error('Erro ao carregar clientes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClientes();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchClientes(searchQuery);
  };

  const handleCreateCliente = async (e: React.FormEvent) => {
    e.preventDefault();

    // Payload corrigido para corresponder ao schema ClienteCreate
    const payload = {
      ...newCliente,
      email: newCliente.email || null,
      telefone: newCliente.telefone || null,
      endereco: newCliente.endereco || null,
    };

    try {
      await api.post('/clientes/', payload);
      toast.success('Cliente criado com sucesso!');
      setShowModal(false);
      setNewCliente({ // Resetar o estado
        nome_razao_social: '',
        tipo: TipoCliente.PESSOA_FISICA,
        documento: '',
        email: '',
        telefone: '',
        endereco: ''
      });
      fetchClientes();
    } catch (error: any) {
      const detail = error.response?.data?.detail || 'Erro ao criar cliente';
      toast.error(detail);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clientes</h1>
          <p className="text-gray-600">Gerencie seus clientes</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Novo Cliente
        </button>
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Buscar clientes por nome ou razão social..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
        </div>
        <button
          type="submit"
          className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          Buscar
        </button>
      </form>

      {/* Clientes Grid (Campos corrigidos) */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {clientes.map((cliente) => (
          <div key={cliente.id} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold text-lg">
                  {cliente.nome_razao_social.charAt(0).toUpperCase()}
                </span>
              </div>
              <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${cliente.tipo === 'pessoa_fisica' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'}`}>
                {cliente.tipo === 'pessoa_fisica' ? 'Pessoa Física' : 'Pessoa Jurídica'}
              </span>
            </div>

            <h3 className="text-lg font-semibold text-gray-900 mb-3">{cliente.nome_razao_social}</h3>

            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4" />
                <span>{cliente.documento}</span>
              </div>
              {cliente.email && (
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  <span>{cliente.email}</span>
                </div>
              )}
              {cliente.telefone && (
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4" />
                  <span>{cliente.telefone}</span>
                </div>
              )}
              {cliente.endereco && (
                <div className="flex items-start gap-2">
                  <MapPin className="w-4 h-4 mt-0.5" />
                  <span className="line-clamp-2">{cliente.endereco}</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {clientes.length === 0 && !loading && (
        <div className="text-center py-12">
          <User className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">Nenhum cliente encontrado</p>
        </div>
      )}

      {/* Modal Novo Cliente (Campos corrigidos e adicionados) */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-md w-full p-6 max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-semibold mb-4">Novo Cliente</h2>
            <form onSubmit={handleCreateCliente} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nome / Razão Social</label>
                <input
                  type="text"
                  value={newCliente.nome_razao_social}
                  onChange={(e) => setNewCliente({...newCliente, nome_razao_social: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tipo de Cliente</label>
                <select
                  value={newCliente.tipo}
                  onChange={(e) => setNewCliente({...newCliente, tipo: e.target.value as TipoCliente})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                >
                  <option value={TipoCliente.PESSOA_FISICA}>Pessoa Física</option>
                  <option value={TipoCliente.PESSOA_JURIDICA}>Pessoa Jurídica</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">CPF / CNPJ</label>
                <input
                  type="text"
                  value={newCliente.documento}
                  onChange={(e) => setNewCliente({...newCliente, documento: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder="Apenas números"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={newCliente.email}
                  onChange={(e) => setNewCliente({...newCliente, email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Telefone</label>
                <input
                  type="text"
                  value={newCliente.telefone}
                  onChange={(e) => setNewCliente({...newCliente, telefone: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Endereço</label>
                <textarea
                  value={newCliente.endereco}
                  onChange={(e) => setNewCliente({...newCliente, endereco: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  rows={3}
                />
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
                  Criar Cliente
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}