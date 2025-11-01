// Em: frontend/src/pages/Clientes.tsx

import { useEffect, useState } from 'react';
// 1. Importar mais ícones e o hook de autenticação
import {
  Search, Plus, Mail, Phone, MapPin, User, FileText, 
  Trash, Edit, X, Loader2
} from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/authStore'; // <-- Importar store

// --- INTERFACES CORRIGIDAS (baseadas em clientes/schema.py) ---

enum TipoCliente {
  PESSOA_FISICA = "pessoa_fisica",
  PESSOA_JURIDICA = "pessoa_juridica",
}

interface Cliente {
  id: number;
  nome_razao_social: string;
  tipo: TipoCliente;
  documento: string;
  email: string | null;
  telefone: string | null;
  endereco: string | null;
  // data_criacao: string; // Você pode adicionar este campo se o backend o enviar
}

// Interface para o payload de criação (para tipagem)
interface ClienteCreate {
  nome_razao_social: string;
  tipo: TipoCliente;
  documento: string; // Enviado sem máscara
  email: string | null;
  telefone: string | null;
  endereco: string | null;
}

// Interface para o payload de atualização (para tipagem)
interface ClienteUpdate {
  nome_razao_social?: string;
  tipo?: TipoCliente;
  documento?: string; // Enviado sem máscara
  email?: string | null;
  telefone?: string | null;
  endereco?: string | null;
}

// --- FUNÇÃO DE MÁSCARA (REQUISITO 3) ---
const formatDocumento = (value: string, tipo: TipoCliente) => {
  const onlyDigits = value.replace(/\D/g, '');

  if (tipo === TipoCliente.PESSOA_JURIDICA) {
    // CNPJ: 00.000.000/0001-00
    return onlyDigits
      .slice(0, 14)
      .replace(/^(\d{2})(\d)/, '$1.$2')
      .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
      .replace(/\.(\d{3})(\d)/, '.$1/$2')
      .replace(/(\d{4})(\d)/, '$1-$2');
  } else {
    // CPF: 000.000.000-00
    return onlyDigits
      .slice(0, 11)
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  }
};


export default function Clientes() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showModal, setShowModal] = useState(false);

  // 2. Novos estados
  const { user } = useAuthStore(); // Pega o usuário logado
  const [isGestor, setIsGestor] = useState(false);
  const [editingCliente, setEditingCliente] = useState<Cliente | null>(null);
  const [selectedClientes, setSelectedClientes] = useState<number[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Estado inicial do formulário (tipado)
  const initialState: ClienteCreate & { email: string, telefone: string, endereco: string } = {
    nome_razao_social: '',
    tipo: TipoCliente.PESSOA_FISICA,
    documento: '', // Este será o valor formatado (com máscara)
    email: '',
    telefone: '',
    endereco: ''
  };
  
  // Renomeado de newCliente para formState para clareza
  const [formState, setFormState] = useState(initialState);

  // Verifica a role do usuário
  useEffect(() => {
    if (user?.role === 'gestor') {
      setIsGestor(true);
    }
  }, [user]);

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

  // 3. Funções de Abertura/Fechamento do Modal
  const handleOpenCreateModal = () => {
    setEditingCliente(null);
    setFormState(initialState);
    setShowModal(true);
  };

  const handleOpenEditModal = (cliente: Cliente) => {
    setEditingCliente(cliente);
    setFormState({
      ...cliente,
      // Garante que o documento no form venha formatado
      documento: formatDocumento(cliente.documento, cliente.tipo),
      email: cliente.email || '',
      telefone: cliente.telefone || '',
      endereco: cliente.endereco || '',
    });
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingCliente(null);
    setFormState(initialState);
  };

  // 4. Função unificada de Submit (Criação e Edição)
  const handleSubmitCliente = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Prepara o payload para enviar à API
    const payload: ClienteCreate | ClienteUpdate = {
      ...formState,
      documento: formState.documento.replace(/\D/g, ''), // Salva só os números
      email: formState.email || null,
      telefone: formState.telefone || null,
      endereco: formState.endereco || null,
    };
    
    // Remove o campo 'id' do payload de atualização, se existir
    if ('id' in payload) {
      delete (payload as any).id;
    }

    try {
      if (editingCliente) {
        // --- LÓGICA DE UPDATE (REQ 2) ---
        await api.put(`/clientes/${editingCliente.id}`, payload);
        toast.success('Cliente atualizado com sucesso!');
      } else {
        // --- LÓGICA DE CREATE ---
        await api.post('/clientes/', payload as ClienteCreate);
        toast.success('Cliente criado com sucesso!');
      }
      handleCloseModal();
      fetchClientes(); // Recarrega a lista
      setSelectedClientes([]); // Limpa seleção
    } catch (error: any) {
      const detail = error.response?.data?.detail || 'Erro ao salvar cliente';
      toast.error(detail);
    } finally {
      setIsSubmitting(false);
    }
  };

  // 5. Função de Deleção Única (Botão no Card)
  const handleDeleteCliente = async (cliente: Cliente) => {
    // Impede que o clique no botão de lixeira selecione o card
    event?.stopPropagation(); 
    
    if (window.confirm(`Tem certeza que deseja excluir "${cliente.nome_razao_social}"?`)) {
      try {
        await api.delete(`/clientes/${cliente.id}`);
        toast.success('Cliente excluído com sucesso!');
        fetchClientes();
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Erro ao excluir cliente.');
      }
    }
  };

  // 6. Funções de Seleção e Deleção em Massa
  const handleSelectCliente = (id: number) => {
    setSelectedClientes((prev) =>
      prev.includes(id)
        ? prev.filter((clienteId) => clienteId !== id)
        : [...prev, id]
    );
  };

  const handleBulkDelete = async () => {
    if (window.confirm(`Tem certeza que deseja excluir ${selectedClientes.length} cliente(s) selecionado(s)?`)) {
      try {
        // Envia o payload no formato { "cliente_ids": [...] }
        const payload = { cliente_ids: selectedClientes };
        const response = await api.post('/clientes/delete-bulk', payload);
        
        toast.success(response.data.detail || 'Clientes excluídos com sucesso!');
        fetchClientes();
        setSelectedClientes([]);
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Erro ao excluir clientes.');
      }
    }
  };

  // 7. Handler da máscara de documento
  const handleDocumentoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = formatDocumento(e.target.value, formState.tipo);
    setFormState({ ...formState, documento: formatted });
  };


  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clientes</h1>
          <p className="text-gray-600">Gerencie seus clientes</p>
        </div>
        <div className="flex gap-2">
          {/* Botão Deletar em Massa */}
          {isGestor && selectedClientes.length > 0 && (
            <button
              onClick={handleBulkDelete}
              className="inline-flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              <Trash className="w-5 h-5" />
              Excluir ({selectedClientes.length})
            </button>
          )}
          {/* Botão Novo Cliente */}
          <button
            onClick={handleOpenCreateModal}
            className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Novo Cliente
          </button>
        </div>
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

      {/* Clientes Grid (Modificado com checkbox e botões) */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {clientes.map((cliente) => (
          <div 
            key={cliente.id} 
            // Adiciona cursor-pointer se for gestor
            className={`bg-white rounded-xl p-6 shadow-sm border ${
              selectedClientes.includes(cliente.id) 
                ? 'border-orange-500 ring-2 ring-orange-200' 
                : 'border-gray-100'
            } ${isGestor ? 'cursor-pointer' : ''} hover:shadow-md transition-shadow relative`}
            // Ação de clique no card inteiro (só para gestor)
            onClick={() => isGestor && handleSelectCliente(cliente.id)}
          >
            
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                 {/* Checkbox de Seleção (Apenas para Gestor) */}
                {isGestor && (
                  <input
                    type="checkbox"
                    checked={selectedClientes.includes(cliente.id)}
                    // Impede que o clique no checkbox acione o clique do card
                    onClick={(e) => e.stopPropagation()} 
                    onChange={() => handleSelectCliente(cliente.id)}
                    className="h-5 w-5 rounded text-orange-600 focus:ring-orange-500 cursor-pointer"
                  />
                )}
                <div className="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-semibold text-lg">
                    {cliente.nome_razao_social.charAt(0).toUpperCase()}
                  </span>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                 <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${cliente.tipo === 'pessoa_fisica' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'}`}>
                  {cliente.tipo === 'pessoa_fisica' ? 'Pessoa Física' : 'Pessoa Jurídica'}
                </span>
                
                {/* Botões de Ação (Apenas para Gestor) */}
                {isGestor && (
                  <>
                    <button
                      onClick={(e) => {
                        e.stopPropagation(); // Impede clique no card
                        handleOpenEditModal(cliente);
                      }}
                      className="p-1 text-gray-400 hover:text-orange-600"
                      title="Editar Cliente"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation(); // Impede clique no card
                        handleDeleteCliente(cliente);
                      }}
                      className="p-1 text-gray-400 hover:text-red-600"
                      title="Excluir Cliente"
                    >
                      <Trash className="w-4 h-4" />
                    </button>
                  </>
                )}
              </div>
            </div>

            <h3 className="text-lg font-semibold text-gray-900 mb-3">{cliente.nome_razao_social}</h3>

            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4" />
                {/* Aplica a formatação no documento exibido */}
                <span>{formatDocumento(cliente.documento, cliente.tipo)}</span>
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

      {/* Modal Novo/Editar Cliente (com Máscara) */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-md w-full p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">
                {editingCliente ? 'Editar Cliente' : 'Novo Cliente'}
              </h2>
              <button onClick={handleCloseModal} className="text-gray-400 hover:text-gray-600">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <form onSubmit={handleSubmitCliente} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nome / Razão Social</label>
                <input
                  type="text"
                  value={formState.nome_razao_social}
                  onChange={(e) => setFormState({...formState, nome_razao_social: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tipo de Cliente</label>
                <select
                  value={formState.tipo}
                  onChange={(e) => setFormState({
                    ...formState, 
                    tipo: e.target.value as TipoCliente,
                    // Limpa o documento ao trocar o tipo para evitar máscara errada
                    documento: '' 
                  })}
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
                  value={formState.documento}
                  onChange={handleDocumentoChange} // <-- USA O HANDLER DA MÁSCARA
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder={
                    formState.tipo === TipoCliente.PESSOA_FISICA 
                      ? '000.000.000-00' 
                      : '00.000.000/0001-00'
                  }
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={formState.email}
                  onChange={(e) => setFormState({...formState, email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Telefone</label>
                <input
                  type="text"
                  value={formState.telefone}
                  onChange={(e) => setFormState({...formState, telefone: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Endereço</label>
                <textarea
                  value={formState.endereco}
                  onChange={(e) => setFormState({...formState, endereco: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  rows={3}
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors disabled:opacity-50"
                >
                  {isSubmitting 
                    ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> 
                    : (editingCliente ? 'Salvar Alterações' : 'Criar Cliente')
                  }
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}