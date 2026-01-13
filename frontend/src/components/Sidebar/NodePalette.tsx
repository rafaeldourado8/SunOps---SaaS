import React, { useEffect, useState } from 'react';
import {Bot, MessageSquare, MessageCircleDashed as MessageCircle, Zap, FileText, GitBranch, Clock, TrendingUp, Users, Headphones} from 'lucide-react';
import { NodeTemplate } from '../../types';
import { api } from '../../lib/api';

const iconMap: Record<string, React.ElementType> = {
  'tag': Bot,
  'message-square': MessageSquare,
  'message-circle': MessageCircle,
  'zap': Zap,
  'file-text': FileText,
  'git-branch': GitBranch,
  'clock': Clock,
  'trending-up': TrendingUp,
  'users': Users,
  'headphones': Headphones,
};

export const NodePalette: React.FC = () => {
  const [nodeTypes, setNodeTypes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadNodeTypes();
  }, []);
  
  const loadNodeTypes = async () => {
    try {
      const types = await api.getNodeTypes();
      setNodeTypes(types);
    } catch (error) {
      console.error('Error loading node types:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const categories = {
    agents: 'Agentes IA',
    integrations: 'Integrações',
    utilities: 'Utilitários',
  };
  
  if (loading) {
    return (
      <div className="w-64 bg-[#0a0a0a] border-r border-[#2a2a2a] h-full flex items-center justify-center">
        <p className="text-[#666666] text-xs">Carregando...</p>
      </div>
    );
  }

  return (
    <div className="w-64 bg-[#0a0a0a] border-r border-[#2a2a2a] h-full overflow-y-auto">
      <div className="p-4 border-b border-[#2a2a2a]">
        <h2 className="text-white font-semibold text-sm">Componentes</h2>
        <p className="text-[#666666] text-xs mt-1">Arraste para o canvas</p>
      </div>

      {Object.entries(categories).map(([key, label]) => {
        const categoryNodes = nodeTypes.filter((n: any) => n.category === key);
        if (categoryNodes.length === 0) return null;
        
        return (
          <div key={key} className="p-4 border-b border-[#2a2a2a]">
            <h3 className="text-[#888888] text-xs font-medium uppercase mb-3">{label}</h3>
            <div className="space-y-2">
              {categoryNodes.map((node: any) => (
                <div
                  key={node.type}
                  className="bg-[#1a1a1a] border border-[#2a2a2a] rounded p-3 cursor-grab hover:border-[#3b82f6] transition-colors group"
                  draggable
                >
                  <div className="flex items-start gap-2">
                    <span className="text-lg">{node.icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="text-white text-xs font-medium">{node.name}</div>
                      <div className="text-[#666666] text-xs mt-0.5">{node.type}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};
