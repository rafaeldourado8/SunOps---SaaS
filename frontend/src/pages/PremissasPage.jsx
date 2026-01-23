import { useState, useEffect } from 'react';
import { FiPlus, FiEdit, FiTrash } from 'react-icons/fi';
import { premissasApi } from '../services/api';
import toast from 'react-hot-toast';

const PremissasPage = () => {
  const [premissas, setPremissas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  
  // CORREÇÃO: Renomeado preco_base para custo_unitario para bater com a API
  const [formData, setFormData] = useState({
    categoria: 'KIT',
    item: '',
    custo_unitario: 0
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    loadPremissas();
  }, []);

  const loadPremissas = async () => {
    try {
      const { data } = await premissasApi.getAll();
      setPremissas(data);
    } catch (error) {
      toast.error('Erro ao carregar premissas');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await premissasApi.update(editingId, formData);
        toast.success('Premissa atualizada!');
      } else {
        await premissasApi.create(formData);
        toast.success('Premissa criada!');
      }
      setShowModal(false);
      resetForm();
      loadPremissas();
    } catch (error) {
      toast.error('Erro ao salvar');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Deseja excluir esta premissa?')) return;
    try {
      await premissasApi.delete(id);
      toast.success('Premissa excluída!');
      loadPremissas();
    } catch (error) {
      toast.error('Erro ao excluir');
    }
  };

  const resetForm = () => {
    // CORREÇÃO: Reset usando custo_unitario
    setFormData({ categoria: 'KIT', item: '', custo_unitario: 0 });
    setEditingId(null);
  };

  const openEdit = (premissa) => {
    setFormData({
      categoria: premissa.categoria,
      item: premissa.item,
      custo_unitario: premissa.custo_unitario
    });
    setEditingId(premissa.id);
    setShowModal(true);
  };

  if (loading) return <div className="p-8">Carregando...</div>;

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-white">Premissas de Preço</h1>
        <button onClick={() => setShowModal(true)} className="btn-solar flex items-center gap-2">
          <FiPlus /> Nova Premissa
        </button>
      </div>

      <div className="glass-card overflow-hidden">
        <table className="w-full">
          <thead className="bg-dark-800/50">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Categoria</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Item</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Custo Unit.</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Ações</th>
            </tr>
          </thead>
          <tbody>
            {premissas.map((premissa) => (
              <tr key={premissa.id} className="border-b border-dark-700/50 hover:bg-dark-800/30">
                <td className="px-6 py-4 text-sm text-gray-200">{premissa.categoria}</td>
                <td className="px-6 py-4 text-sm text-gray-200">{premissa.item}</td>
                <td className="px-6 py-4 text-sm text-gray-200">
                  R$ {premissa.custo_unitario?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </td>
                <td className="px-6 py-4">
                  <div className="flex gap-2">
                    <button onClick={() => openEdit(premissa)} className="p-2 text-blue-400 hover:bg-blue-500/10 rounded">
                      <FiEdit />
                    </button>
                    <button onClick={() => handleDelete(premissa.id)} className="p-2 text-red-400 hover:bg-red-500/10 rounded">
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
          <div className="glass-card w-full max-w-md p-6 m-4">
            <h2 className="text-2xl font-bold text-white mb-4">
              {editingId ? 'Editar Premissa' : 'Nova Premissa'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <select
                className="input-solar"
                value={formData.categoria}
                onChange={(e) => setFormData({ ...formData, categoria: e.target.value })}
                required
              >
                <option value="KIT">Kit</option>
                <option value="SERVICO">Serviço</option>
                <option value="CUSTO">Custo</option>
              </select>
              <input
                type="text"
                placeholder="Item"
                className="input-solar"
                value={formData.item}
                onChange={(e) => setFormData({ ...formData, item: e.target.value })}
                required
              />
              <input
                type="number"
                step="0.01"
                placeholder="Custo Unitário"
                className="input-solar"
                value={formData.custo_unitario}
                onChange={(e) => setFormData({ ...formData, custo_unitario: parseFloat(e.target.value) })}
                required
              />
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

export default PremissasPage;