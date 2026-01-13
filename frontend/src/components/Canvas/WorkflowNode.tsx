import React from 'react';
import { Handle, Position } from '@xyflow/react';
import {Settings} from 'lucide-react';

interface WorkflowNodeProps {
  data: {
    label: string;
    type: string;
    icon: string;
    status?: string;
    statusColor?: string;
    metrics?: { label: string; value: string }[];
  };
}

export const WorkflowNode: React.FC<WorkflowNodeProps> = ({ data }) => {
  return (
    <div className="bg-[#1a1a1a] border-2 border-[#2a2a2a] rounded-lg min-w-[260px] hover:border-[#3b82f6] transition-all shadow-lg">
      <Handle type="target" position={Position.Left} className="w-3 h-3 !bg-[#3b82f6]" />
      
      {/* Header */}
      <div className="px-4 py-3 border-b border-[#2a2a2a]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-lg">{data.icon}</span>
            <span className="text-white font-medium text-sm">{data.label}</span>
          </div>
          <button className="text-[#666666] hover:text-white transition-colors">
            <Settings className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="px-4 py-3 space-y-2">
        {data.status && (
          <div className="flex items-center gap-2 text-xs">
            <span className="text-[#666666]">Status:</span>
            <div className="flex items-center gap-1.5">
              <div
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: data.statusColor }}
              />
              <span className="text-white">{data.status}</span>
            </div>
          </div>
        )}
        
        {data.metrics?.map((metric, index) => (
          <div key={index} className="flex items-center gap-2 text-xs">
            <span className="text-[#666666]">{metric.label}:</span>
            <span className="text-white">{metric.value}</span>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="px-4 py-2 border-t border-[#2a2a2a]">
        <button className="text-[#3b82f6] hover:text-[#2563eb] text-xs font-medium transition-colors">
          Configurar
        </button>
      </div>

      <Handle type="source" position={Position.Right} className="w-3 h-3 !bg-[#3b82f6]" />
    </div>
  );
};
