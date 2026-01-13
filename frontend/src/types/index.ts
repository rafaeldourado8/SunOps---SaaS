export type NodeType = 
  | 'botVendas'
  | 'botSuporte'
  | 'whatsapp'
  | 'inversor'
  | 'orcamento'
  | 'condicao'
  | 'delay'
  | 'marketing'
  | 'vendas'
  | 'suporte';

export interface NodeData {
  label: string;
  type: NodeType;
  icon: string;
  status?: string;
  statusColor?: string;
  metrics?: { label: string; value: string }[];
  config?: Record<string, any>;
}

export interface WorkflowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: NodeData;
}

export interface NodeTemplate {
  type: NodeType;
  label: string;
  icon: string;
  category: 'ai' | 'integration' | 'utility';
  description: string;
}
