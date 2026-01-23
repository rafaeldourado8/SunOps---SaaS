// SunOPS/frontend/src/pages/ConfiguracoesPage.jsx
import { useState, useEffect } from 'react';
import { premissasApi } from '../services/api';
import toast from 'react-hot-toast';

const ConfiguracoesPage = () => {
  const [config, setConfig] = useState({
    imposto_percentual: 0,
    comissao_percentual: 0,
    lucro_percentual: 0,
    montagem_por_painel: 0,
    projeto_fixo: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      // CORREÇÃO: Usar getConfig() em vez de getAll()
      const { data } = await premissasApi.getConfig();
      
      // CORREÇÃO: Converter decimais do backend (0.18) para porcentagem (18)
      // e mapear nomes de campos divergentes
      setConfig({
        montagem_por_painel: data.montagem_por_painel || 0,
        projeto_fixo: data.custo_projeto || 0, // Backend: custo_projeto -> Frontend: projeto_fixo
        lucro_percentual: (data.margem_lucro || 0) * 100,
        comissao_percentual: (data.comissao || 0) * 100,
        imposto_percentual: (data.imposto || 0) * 100
      });
      setLoading(false);
    } catch (error) {
      console.error(error);
      toast.error('Erro ao carregar configurações');
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // CORREÇÃO: Converter de volta para decimal e usar nomes do Backend
      const payload = {
        montagem_por_painel: config.montagem_por_painel,
        custo_projeto: config.projeto_fixo, // Frontend: projeto_fixo -> Backend: custo_projeto
        margem_lucro: config.lucro_percentual / 100,
        comissao: config.comissao_percentual / 100,
        imposto: config.imposto_percentual / 100
      };

      await premissasApi.updateConfig(payload);
      toast.success('Configurações atualizadas!');
      
      // Recarrega para garantir que os dados foram salvos corretamente
      loadConfig();
    } catch (error) {
      console.error(error);
      toast.error('Erro ao salvar configurações');
    }
  };

  if (loading) return <div className="p-8">Carregando...</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-6">Configurações Globais</h1>

      <div className="glass-card p-6 max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="label-solar">Imposto (%)</label>
            <input
              type="number"
              step="0.01"
              className="input-solar"
              value={config.imposto_percentual}
              onChange={(e) => setConfig({ ...config, imposto_percentual: parseFloat(e.target.value) })}
            />
          </div>

          <div>
            <label className="label-solar">Comissão (%)</label>
            <input
              type="number"
              step="0.01"
              className="input-solar"
              value={config.comissao_percentual}
              onChange={(e) => setConfig({ ...config, comissao_percentual: parseFloat(e.target.value) })}
            />
          </div>

          <div>
            <label className="label-solar">Lucro (%)</label>
            <input
              type="number"
              step="0.01"
              className="input-solar"
              value={config.lucro_percentual}
              onChange={(e) => setConfig({ ...config, lucro_percentual: parseFloat(e.target.value) })}
            />
          </div>

          <div>
            <label className="label-solar">Montagem por Painel (R$)</label>
            <input
              type="number"
              step="0.01"
              className="input-solar"
              value={config.montagem_por_painel}
              onChange={(e) => setConfig({ ...config, montagem_por_painel: parseFloat(e.target.value) })}
            />
          </div>

          <div>
            <label className="label-solar">Projeto Fixo (R$)</label>
            <input
              type="number"
              step="0.01"
              className="input-solar"
              value={config.projeto_fixo}
              onChange={(e) => setConfig({ ...config, projeto_fixo: parseFloat(e.target.value) })}
            />
          </div>

          <button type="submit" className="btn-solar w-full">
            Salvar Configurações
          </button>
        </form>
      </div>
    </div>
  );
};

export default ConfiguracoesPage;