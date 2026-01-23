import { useState, useEffect } from 'react';
import { FiUpload, FiTrash, FiFile, FiPlus } from 'react-icons/fi';
import { templatesApi } from '../services/api';
import toast from 'react-hot-toast';

const TemplatesPage = () => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    nome: '',
    tipo: 'CONTRATO',
    file: null
  });

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const { data } = await templatesApi.getAll();
      setTemplates(data);
    } catch (error) {
      toast.error('Erro ao carregar templates');
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setFormData({ ...formData, file });
    } else {
      toast.error('Apenas arquivos PDF são permitidos');
    }
  };

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!formData.file) {
      toast.error('Selecione um arquivo PDF');
      return;
    }

    setUploading(true);
    try {
      // Tenta pegar o ID do usuário do localStorage. Se não houver, usa um ID de "fallback" (ex: seed)
      // Nota: Idealmente o backend pegaria isso do token, mas a API pede Form param.
      const userStr = localStorage.getItem('user');
      const user = userStr ? JSON.parse(userStr) : {};
      const vendedorId = user.id || "00000000-0000-0000-0000-000000000000"; // Fallback ou trate erro

      await templatesApi.upload(formData.file, formData.tipo, formData.nome, vendedorId);
      toast.success('Template enviado!');
      setShowModal(false);
      setFormData({ nome: '', tipo: 'CONTRATO', file: null });
      loadTemplates();
    } catch (error) {
      console.error(error);
      toast.error('Erro ao enviar template');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Deseja excluir este template?')) return;
    try {
      await templatesApi.delete(id);
      toast.success('Template excluído!');
      loadTemplates();
    } catch (error) {
      toast.error('Erro ao excluir');
    }
  };

  if (loading) return <div className="p-8">Carregando...</div>;

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-white">Templates PDF</h1>
        <button onClick={() => setShowModal(true)} className="btn-solar flex items-center gap-2">
          <FiPlus /> Novo Template
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {templates.map((template) => (
          <div key={template.id} className="glass-card p-6">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="p-3 bg-solar-500/20 rounded-lg">
                  <FiFile className="w-6 h-6 text-solar-400" />
                </div>
                <div>
                  <h3 className="text-white font-medium">{template.nome}</h3>
                  <p className="text-sm text-gray-400">{template.tipo}</p>
                </div>
              </div>
              <button
                onClick={() => handleDelete(template.id)}
                className="p-2 text-red-400 hover:bg-red-500/10 rounded"
              >
                <FiTrash />
              </button>
            </div>
          </div>
        ))}
      </div>

      {templates.length === 0 && (
        <div className="glass-card p-12 text-center">
          <FiFile className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">Nenhum template cadastrado</p>
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="glass-card w-full max-w-md p-6 m-4">
            <h2 className="text-2xl font-bold text-white mb-4">Novo Template</h2>
            <form onSubmit={handleUploadSubmit} className="space-y-4">
              <input
                type="text"
                placeholder="Nome do Template"
                className="input-solar"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                required
              />
              <select
                className="input-solar"
                value={formData.tipo}
                onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
              >
                <option value="CONTRATO">Contrato</option>
                <option value="PROPOSTA">Proposta</option>
              </select>
              
              <div className="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                  {formData.file ? (
                    <span className="text-solar-400">{formData.file.name}</span>
                  ) : (
                    <span className="text-gray-400 flex flex-col items-center gap-2">
                      <FiUpload className="w-8 h-8" />
                      Clique para selecionar PDF
                    </span>
                  )}
                </label>
              </div>

              <div className="flex gap-2 justify-end mt-6">
                <button 
                  type="button" 
                  onClick={() => { setShowModal(false); setFormData({ nome: '', tipo: 'CONTRATO', file: null }); }} 
                  className="btn-ghost"
                >
                  Cancelar
                </button>
                <button type="submit" className="btn-solar" disabled={uploading}>
                  {uploading ? 'Enviando...' : 'Salvar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TemplatesPage;