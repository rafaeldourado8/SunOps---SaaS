import { useState, useEffect } from 'react';
import { FiPlus, FiEdit, FiTrash, FiTrendingUp } from 'react-icons/fi';
import { clientesApi } from '../services/api';
import toast from 'react-hot-toast';

const ClientesPage = () => {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    nome: '', email: '', telefone: '', cpf_cnpj: '',
    endereco: '', cidade: '', estado: '', cep: ''
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    loadClientes();
  }, []);

  const loadClientes = async () => {
    try {
      const { data } = await clientesApi.getAll();
      setClientes(data);
    } catch (error) {
      toast.error('Erro ao carregar clientes');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await clientesApi.update(editingId, formData);
        toast.success('Cliente atualizado!');
      } else {
        await clientesApi.create(formData);
        toast.success('Cliente criado!');
      }
      setShowModal(false);
      resetForm();
      loadClientes();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erro ao salvar');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Deseja excluir este cliente?')) return;
    try {
      await clientesApi.delete(id);
      toast.success('Cliente excluído!');
      loadClientes();
    } catch (error) {
      toast.error('Erro ao excluir');
    }
  };

  const handlePromover = async (id) => {
    try {
      await clientesApi.promover(id);
      toast.success('Cliente promovido!');
      loadClientes();
    } catch (error) {
      toast.error('Erro ao promover');
    }
  };

  const resetForm = () => {
    setFormData({ nome: '', email: '', telefone: '', cpf_cnpj: '', endereco: '', cidade: '', estado: '', cep: '' });
    setEditingId(null);
  };

  const openEdit = (cliente) => {
    setFormData({
      nome: cliente.nome || '',
      email: typeof cliente.email === 'object' ? cliente.email?.value || '' : cliente.email || '',
      telefone: typeof cliente.telefone === 'object' ? cliente.telefone?.value || '' : cliente.telefone || '',
      cpf_cnpj: cliente.cpf_cnpj || '',
      endereco: cliente.endereco || '',
      cidade: cliente.cidade || '',
      estado: cliente.estado || '',
      cep: cliente.cep || ''
    });
    setEditingId(cliente.id);
    setShowModal(true);
  };

  if (loading) return <div className="p-8">Carregando...</div>;

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-white">Clientes</h1>
        <button onClick={() => setShowModal(true)} className="btn-solar flex items-center gap-2">
          <FiPlus /> Novo Cliente
        </button>
      </div>

      <div className="glass-card overflow-hidden">
        <table className="w-full">
          <thead className="bg-dark-800/50">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Nome</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Email</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Telefone</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Tipo</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Ações</th>
            </tr>
          </thead>
          <tbody>
            {clientes.map((cliente) => (
              <tr key={cliente.id} className="border-b border-dark-700/50 hover:bg-dark-800/30">
                <td className="px-6 py-4 text-sm text-gray-200">{cliente.nome}</td>
                <td className="px-6 py-4 text-sm text-gray-200">{typeof cliente.email === 'object' ? cliente.email?.value || '-' : cliente.email || '-'}</td>
                <td className="px-6 py-4 text-sm text-gray-200">{typeof cliente.telefone === 'object' ? cliente.telefone?.value || '-' : cliente.telefone || '-'}</td>
                <td className="px-6 py-4">
                  <span className={`badge ${
                    cliente.status === 'CLIENTE' ? 'badge-success' :
                    cliente.status === 'PROSPECT' ? 'badge-warning' : 'badge-info'
                  }`}>
                    {cliente.status}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex gap-2">
                    <button onClick={() => openEdit(cliente)} className="p-2 text-blue-400 hover:bg-blue-500/10 rounded">
                      <FiEdit />
                    </button>
                    {cliente.status === 'LEAD' && (
                      <button onClick={() => handlePromover(cliente.id)} className="p-2 text-green-400 hover:bg-green-500/10 rounded">
                        <FiTrendingUp />
                      </button>
                    )}
                    <button onClick={() => handleDelete(cliente.id)} className="p-2 text-red-400 hover:bg-red-500/10 rounded">
                      <FiTrash />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="glass-card w-full max-w-2xl p-6 m-4">
            <h2 className="text-2xl font-bold text-white mb-4">
              {editingId ? 'Editar Cliente' : 'Novo Cliente'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Nome"
                  className="input-solar"
                  value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                  required
                />
                <input
                  type="email"
                  placeholder="Email"
                  className="input-solar"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
                <input
                  type="text"
                  placeholder="Telefone"
                  className="input-solar"
                  value={formData.telefone}
                  onChange={(e) => setFormData({ ...formData, telefone: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="CPF/CNPJ"
                  className="input-solar"
                  value={formData.cpf_cnpj}
                  onChange={(e) => setFormData({ ...formData, cpf_cnpj: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="Endereço"
                  className="input-solar col-span-2"
                  value={formData.endereco}
                  onChange={(e) => setFormData({ ...formData, endereco: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="Cidade"
                  className="input-solar"
                  value={formData.cidade}
                  onChange={(e) => setFormData({ ...formData, cidade: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="Estado"
                  className="input-solar"
                  value={formData.estado}
                  onChange={(e) => setFormData({ ...formData, estado: e.target.value })}
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button type="button" onClick={() => { setShowModal(false); resetForm(); }} className="btn-ghost">
                  Cancelar
                </button>
                <button type="submit" className="btn-solar">
                  Salvar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClientesPage;
