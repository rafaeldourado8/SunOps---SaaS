import React, { useState, useEffect } from 'react';
import {X, Plus, Trash2} from 'lucide-react';
import { useCanvasStore } from '../../stores/canvasStore';
import { api } from '../../lib/api';

export const ConfigPanel: React.FC = () => {
  const { selectedNode, setSelectedNode, updateNode } = useCanvasStore();
  const [config, setConfig] = useState<any>({});
  const [metrics, setMetrics] = useState<any>(null);
  const [rules, setRules] = useState<string[]>([]);

  useEffect(() => {
    if (selectedNode?.data.type === 'botVendas') {
      loadVendasMetrics();
      setConfig(selectedNode.data.config || {
        model: 'gemini-1.5-flash',
        systemPrompt: 'Você é um vendedor especialista em energia solar da SunOps.',
        temperature: 0.7
      });
      setRules(selectedNode.data.config?.rules || [
        'Não inventar informações',
        'Manter contexto da conversa',
        'Linguagem humanizada'
      ]);
    } else if (selectedNode?.data.type === 'botSuporte') {
      loadSuporteMetrics();
      setConfig(selectedNode.data.config || {
        model: 'gemini-1.5-flash',
        systemPrompt: 'Você é um agente de suporte técnico especializado em energia solar.',
        temperature: 0.7
      });
      setRules(selectedNode.data.config?.rules || [
        'Criar ticket automaticamente',
        'Verificar garantia',
        'Diagnosticar problemas'
      ]);
    }
  }, [selectedNode]);

  const loadVendasMetrics = async () => {
    try {
      const response = await api.get('/agents/vendas/metrics');
      setMetrics(response.data);
    } catch (error) {
      console.error('Error loading metrics:', error);
    }
  };

  const loadSuporteMetrics = async () => {
    try {
      const response = await api.get('/agents/suporte/metrics');
      setMetrics(response.data);
    } catch (error) {
      console.error('Error loading metrics:', error);
    }
  };

  const handleSave = async () => {
    try {
      const endpoint = selectedNode.data.type === 'botVendas' 
        ? '/agents/vendas/config' 
        : '/agents/suporte/config';
      await api.post(endpoint, { config: { ...config, rules } });
      updateNode(selectedNode.id, { config: { ...config, rules } });
      alert('Configuração salva com sucesso!');
    } catch (error) {
      console.error('Error saving config:', error);
      alert('Erro ao salvar configuração');
    }
  };

  const addRule = () => {
    const newRule = prompt('Digite a nova regra:');
    if (newRule) setRules([...rules, newRule]);
  };

  const removeRule = (index: number) => {
    setRules(rules.filter((_, i) => i !== index));
  };

  if (!selectedNode) return null;

  return (
    <div className="w-80 bg-[#0a0a0a] border-l border-[#2a2a2a] h-full overflow-y-auto">
      <div className="p-4 border-b border-[#2a2a2a] flex items-center justify-between">
        <h2 className="text-white font-semibold text-sm">Configurar Node</h2>
        <button
          onClick={() => setSelectedNode(null)}
          className="text-[#888888] hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="p-4 space-y-6">
        {/* Informações */}
        <div>
          <h3 className="text-[#888888] text-xs font-medium uppercase mb-3">Informações</h3>
          <div className="space-y-3">
            <div>
              <label className="text-[#666666] text-xs mb-1 block">Nome</label>
              <input
                type="text"
                value={selectedNode.data.label}
                onChange={(e) => updateNode(selectedNode.id, { label: e.target.value })}
                className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-[#3b82f6]"
              />
            </div>
            <div>
              <label className="text-[#666666] text-xs mb-1 block">Descrição</label>
              <textarea
                rows={3}
                placeholder="Descreva a função deste node..."
                className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-[#3b82f6] resize-none"
              />
            </div>
          </div>
        </div>

        {/* Comportamento */}
        <div>
          <h3 className="text-[#888888] text-xs font-medium uppercase mb-3">Comportamento</h3>
          <div className="space-y-3">
            <div>
              <label className="text-[#666666] text-xs mb-1 block">Modelo IA</label>
              <select 
                value={config.model || 'gemini-1.5-flash'}
                onChange={(e) => setConfig({...config, model: e.target.value})}
                className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-[#3b82f6]"
              >
                <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                <option value="gpt-4">GPT-4</option>
              </select>
            </div>
            <div>
              <label className="text-[#666666] text-xs mb-1 block">Prompt do Sistema</label>
              <textarea
                rows={4}
                value={config.systemPrompt || ''}
                onChange={(e) => setConfig({...config, systemPrompt: e.target.value})}
                placeholder="Você é um assistente que..."
                className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-[#3b82f6] resize-none"
              />
            </div>
          </div>
        </div>

        {/* Regras */}
        <div>
          <h3 className="text-[#888888] text-xs font-medium uppercase mb-3">Regras</h3>
          <button 
            onClick={addRule}
            className="w-full bg-[#1a1a1a] border border-[#2a2a2a] rounded px-3 py-2 text-[#3b82f6] text-sm hover:bg-[#1e1e1e] transition-colors flex items-center justify-center gap-2"
          >
            <Plus className="w-3 h-3" />
            Adicionar regra
          </button>
          <div className="mt-3 space-y-2">
            {rules.map((rule, index) => (
              <div key={index} className="text-[#888888] text-xs flex items-start gap-2 group">
                <span>•</span>
                <span className="flex-1">{rule}</span>
                <button
                  onClick={() => removeRule(index)}
                  className="opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-400"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Métricas */}
        {(selectedNode.data.type === 'botVendas' || selectedNode.data.type === 'botSuporte') && metrics && (
          <div>
            <h3 className="text-[#888888] text-xs font-medium uppercase mb-3">Métricas (Tempo Real)</h3>
            {selectedNode.data.type === 'botVendas' ? (
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded p-3">
                  <div className="text-white text-lg font-semibold">{metrics.total_conversations}</div>
                  <div className="text-[#666666] text-xs mt-1">Conversas</div>
                </div>
                <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded p-3">
                  <div className="text-[#22c55e] text-lg font-semibold">{metrics.orcamentos_gerados}</div>
                  <div className="text-[#666666] text-xs mt-1">Orçamentos</div>
                </div>
                <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded p-3">
                  <div className="text-[#3b82f6] text-lg font-semibold">{metrics.active_conversations}</div>
                  <div className="text-[#666666] text-xs mt-1">Ativas</div>
                </div>
                <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded p-3">
                  <div className="text-[#f59e0b] text-lg font-semibold">{(metrics.taxa_conversao * 100).toFixed(0)}%</div>
                  <div className="text-[#666666] text-xs mt-1">Conversão</div>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded p-3">
                  <div className="text-white text-lg font-semibold">{metrics.total_tickets}</div>
                  <div className="text-[#666666] text-xs mt-1">Tickets</div>
                </div>
                <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded p-3">
                  <div className="text-[#ef4444] text-lg font-semibold">{metrics.open_tickets}</div>
                  <div className="text-[#666666] text-xs mt-1">Abertos</div>
                </div>
                <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded p-3">
                  <div className="text-[#22c55e] text-lg font-semibold">{metrics.resolved_tickets}</div>
                  <div className="text-[#666666] text-xs mt-1">Resolvidos</div>
                </div>
                <div className="bg-[#1a1a1a] border border-[#2a2a2a] rounded p-3">
                  <div className="text-[#3b82f6] text-lg font-semibold">{metrics.avg_sla_hours}h</div>
                  <div className="text-[#666666] text-xs mt-1">SLA Médio</div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Botão Salvar */}
        <button 
          onClick={handleSave}
          className="w-full bg-[#3b82f6] hover:bg-[#2563eb] text-white rounded px-4 py-2 text-sm font-medium transition-colors"
        >
          Salvar Alterações
        </button>
      </div>
    </div>
  );
};
