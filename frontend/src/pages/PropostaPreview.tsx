// frontend/src/pages/PropostaPreview.tsx
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import toast from 'react-hot-toast';
import { ArrowLeft, Loader2 } from 'lucide-react';

// (Você pode reutilizar as interfaces de PropostaDimensionamento)
interface ShowProposta {
  id: number;
  nome: string | null;
  cliente: {
    nome_razao_social: string;
  };
  // ... outros campos
}

export default function PropostaPreview() {
  const { propostaId } = useParams();
  const navigate = useNavigate();
  const [proposta, setProposta] = useState<ShowProposta | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProposta = async () => {
      if (!propostaId) return;
      try {
        const response = await api.get(`/propostas/${propostaId}`);
        setProposta(response.data);
      } catch (error) {
        toast.error('Erro ao carregar proposta.');
        navigate('/app/propostas');
      } finally {
        setLoading(false);
      }
    };
    fetchProposta();
  }, [propostaId, navigate]);

  const handleProsseguir = () => {
    // (Lógica futura para gerar o PDF/Word)
    toast.success('Lógica de geração de PDF será implementada aqui.');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-12 h-12 animate-spin text-orange-500" />
      </div>
    );
  }

  if (!proposta) {
    return <div>Proposta não encontrada.</div>;
  }

  // Lista de templates (exemplo)
  const templates = [
    "Template Web", 
    "PROJETO PARA SICREDI", 
    "PROJETO PARA BRADESCO",
    "DEYE MONOFÁSICO",
    "GROWATT MONOFÁSICO",
    // ... etc.
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <button
          onClick={() => navigate(`/app/propostas/${propostaId}/dimensionamento`)}
          className="p-2 rounded-md text-gray-500 hover:bg-gray-100"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Etapa 3: Template e Geração
          </h1>
          <p className="text-gray-600">
            Proposta para: {proposta.cliente.nome_razao_social}
          </p>
        </div>
      </div>
      
      {/* Aviso */}
      <div className="p-4 bg-yellow-50 border border-yellow-200 text-yellow-800 rounded-lg">
        <strong>Atenção!</strong> O dimensionamento foi atualizado após a geração do arquivo. É possível que o arquivo não seja mais compatível. Gere um novo arquivo se necessário.
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Coluna de Templates */}
        <div className="lg:col-span-1 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="font-semibold mb-2">Selecione o template</h3>
          <select className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-4">
            {templates.map(t => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
          
          <h4 className="font-semibold text-sm mb-2">Visualizar template</h4>
          {/* (Aqui você pode adicionar lógica para mostrar/esconder templates) */}
          <div className="space-y-1">
            <p className="text-sm text-blue-600 cursor-pointer">Template Web</p>
            <p className="text-sm font-semibold text-gray-800 mt-2">Template Doc</p>
            <p className="text-sm text-gray-600 cursor-pointer pl-2">PROJETO PARA SICREDI</p>
            {/* ... etc */}
          </div>
        </div>
        
        {/* Coluna de Preview */}
        <div className="lg:col-span-3 bg-white p-6 rounded-xl shadow-sm border border-gray-100 min-h-[600px]">
          <div className="flex justify-center items-center h-full bg-gray-100 rounded-lg">
            <p className="text-gray-500">(Pré-visualização do PDF/Word aparecerá aqui)</p>
            {/* Exemplo de como a imagem se parece */}
            <div className="text-center hidden">
              <h2 className="text-3xl font-bold">Nacional Energia Solar</h2>
              <h1 className="text-5xl font-bold text-green-600">PROPOSTA</h1>
              <h1 className="text-5xl font-bold text-green-600">COMERCIAL</h1>
            </div>
          </div>
        </div>
      </div>
      
      {/* Botões de Navegação */}
      <div className="flex justify-between mt-6">
         <button
          onClick={() => navigate(`/app/propostas/${propostaId}/dimensionamento`)}
          className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
        >
          Voltar
        </button>
         <button
          onClick={handleProsseguir}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Prosseguir
        </button>
      </div>
    </div>
  );
}