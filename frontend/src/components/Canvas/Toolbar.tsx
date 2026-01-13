import React, { useState } from 'react';
import {Save, Play, History, LayoutGrid, Workflow, Ticket, Smartphone} from 'lucide-react';
import { useCanvasStore } from '../../stores/canvasStore';

export const Toolbar: React.FC = () => {
  const { workflowName, viewMode, setViewMode, saveWorkflow, executeWorkflow } = useCanvasStore();
  const [isEditingName, setIsEditingName] = useState(false);
  const [name, setName] = useState(workflowName);
  const [saving, setSaving] = useState(false);
  const [executing, setExecuting] = useState(false);

  const handleNameSave = () => {
    setIsEditingName(false);
    useCanvasStore.getState().setWorkflowName(name);
  };
  
  const handleSave = async () => {
    setSaving(true);
    try {
      await saveWorkflow();
      alert('Workflow salvo com sucesso!');
    } catch (error) {
      alert('Erro ao salvar workflow');
    } finally {
      setSaving(false);
    }
  };
  
  const handleExecute = async () => {
    setExecuting(true);
    try {
      await executeWorkflow();
      alert('Workflow executado com sucesso!');
    } catch (error: any) {
      alert(error.message || 'Erro ao executar workflow');
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="h-14 bg-[#0a0a0a] border-b border-[#2a2a2a] flex items-center justify-between px-4">
      {/* Left: Workflow Name */}
      <div className="flex items-center gap-3">
        {isEditingName ? (
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onBlur={handleNameSave}
            onKeyDown={(e) => e.key === 'Enter' && handleNameSave()}
            className="bg-[#1a1a1a] border border-[#2a2a2a] rounded px-3 py-1.5 text-white text-sm focus:outline-none focus:border-[#3b82f6]"
            autoFocus
          />
        ) : (
          <h1
            onClick={() => setIsEditingName(true)}
            className="text-white font-semibold text-sm cursor-pointer hover:text-[#3b82f6] transition-colors"
          >
            {workflowName}
          </h1>
        )}
      </div>

      {/* Center: View Toggle */}
      <div className="flex items-center gap-1 bg-[#1a1a1a] rounded p-1">
        <button
          onClick={() => setViewMode('canvas')}
          className={`flex items-center gap-2 px-3 py-1.5 rounded text-xs font-medium transition-colors ${
            viewMode === 'canvas'
              ? 'bg-[#3b82f6] text-white'
              : 'text-[#888888] hover:text-white'
          }`}
        >
          <Workflow className="w-3.5 h-3.5" />
          Canvas
        </button>
        <button
          onClick={() => setViewMode('dashboard')}
          className={`flex items-center gap-2 px-3 py-1.5 rounded text-xs font-medium transition-colors ${
            viewMode === 'dashboard'
              ? 'bg-[#3b82f6] text-white'
              : 'text-[#888888] hover:text-white'
          }`}
        >
          <LayoutGrid className="w-3.5 h-3.5" />
          Dashboard
        </button>
        <button
          onClick={() => setViewMode('tickets')}
          className={`flex items-center gap-2 px-3 py-1.5 rounded text-xs font-medium transition-colors ${
            viewMode === 'tickets'
              ? 'bg-[#3b82f6] text-white'
              : 'text-[#888888] hover:text-white'
          }`}
        >
          <Ticket className="w-3.5 h-3.5" />
          Tickets
        </button>
        <button
          onClick={() => setViewMode('whatsapp')}
          className={`flex items-center gap-2 px-3 py-1.5 rounded text-xs font-medium transition-colors ${
            viewMode === 'whatsapp'
              ? 'bg-[#3b82f6] text-white'
              : 'text-[#888888] hover:text-white'
          }`}
        >
          <Smartphone className="w-3.5 h-3.5" />
          WhatsApp
        </button>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2">
        <button className="flex items-center gap-2 px-3 py-1.5 bg-[#1a1a1a] hover:bg-[#1e1e1e] text-[#888888] hover:text-white rounded text-xs font-medium transition-colors">
          <History className="w-3.5 h-3.5" />
          Histórico
        </button>
        <button 
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 px-3 py-1.5 bg-[#1a1a1a] hover:bg-[#1e1e1e] text-[#888888] hover:text-white rounded text-xs font-medium transition-colors disabled:opacity-50"
        >
          <Save className="w-3.5 h-3.5" />
          {saving ? 'Salvando...' : 'Salvar'}
        </button>
        <button 
          onClick={handleExecute}
          disabled={executing}
          className="flex items-center gap-2 px-3 py-1.5 bg-[#22c55e] hover:bg-[#16a34a] text-white rounded text-xs font-medium transition-colors disabled:opacity-50"
        >
          <Play className="w-3.5 h-3.5" />
          {executing ? 'Executando...' : 'Executar'}
        </button>
      </div>
    </div>
  );
};
