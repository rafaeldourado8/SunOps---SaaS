import { useState, useEffect } from 'react';
import { FiPlus, FiEye, FiDownload } from 'react-icons/fi';
import { propostasApi, clientesApi } from '../services/api';
import toast from 'react-hot-toast';

const PropostasPage = () => {
  const [propostas, setPropostas] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ cliente_id: '' });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [propRes, cliRes] = await Promise.all([
        propostasApi.getAll(),
        clientesApi.getAll()
      ]);
      setPropostas(propRes.data);
      setClientes(cliRes.data);
    } catch (error) {
      toast.error('Erro ao carregar dados');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await propostasApi.create(formData);
      toast.success('Proposta criada!');
      setShowModal(false);
      setFormData({ cliente_id: '' });
      loadData();
    } catch (error) {
      toast.error('Erro ao criar proposta');
    }
  };

  const handleDownloadPDF = async (id) => {
    try {
      const { data } = await propostasApi.generatePDF(id);
      const url = window.URL.createObjectURL(new Blob([data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `proposta-${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('PDF gerado!');
    } catch (error) {
      toast.error('Erro ao gerar PDF');
    }
  };

  if (loading) return <div className="p-8">Carregando...</div>;

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-white">Propostas</h1>
        <button onClick={() => setShowModal(true)} className="btn-solar flex items-center gap-2">
          <FiPlus /> Nova Proposta
        </button>
      </div>

      <div className="glass-card overflow-hidden">
        <table className="w-full">
          <thead className="bg-dark-800/50">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Número</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Cliente</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Valor</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Status</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase">Ações</th>
            </tr>
          </thead>
          <tbody>
            {propostas.map((proposta) => (
              <tr key={proposta.id} className="border-b border-dark-700/50 hover:bg-dark-800/30">
                <td className="px-6 py-4 text-sm text-gray-200">{proposta.numero}</td>
                <td className="px-6 py-4 text-sm text-gray-200">{proposta.cliente?.nome}</td>
                <td className="px-6 py-4 text-sm text-gray-200">
                  R$ {proposta.valor_total?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </td>
                <td className="px-6 py-4">
                  <span className={`badge ${
                    proposta.status === 'APROVADA' ? 'badge-success' :
                    proposta.status === 'ENVIADA' ? 'badge-warning' :
                    proposta.status === 'REJEITADA' ? 'badge-danger' : 'badge-info'
                  }`}>
                    {proposta.status}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex gap-2">
                    <button className="p-2 text-blue-400 hover:bg-blue-500/10 rounded">
                      <FiEye />
                    </button>
                    <button onClick={() => handleDownloadPDF(proposta.id)} className="p-2 text-green-400 hover:bg-green-500/10 rounded">
                      <FiDownload />
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
            <h2 className="text-2xl font-bold text-white mb-4">Nova Proposta</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <select
                className="input-solar"
                value={formData.cliente_id}
                onChange={(e) => setFormData({ ...formData, cliente_id: e.target.value })}
                required
              >
                <option value="">Selecione um cliente</option>
                {clientes.map((cliente) => (
                  <option key={cliente.id} value={cliente.id}>
                    {cliente.nome}
                  </option>
                ))}
              </select>
              <div className="flex gap-2 justify-end">
                <button type="button" onClick={() => setShowModal(false)} className="btn-ghost">
                  Cancelar
                </button>
                <button type="submit" className="btn-solar">
                  Criar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default PropostasPage;
