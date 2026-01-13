import React, { useCallback } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { WorkflowNode } from './WorkflowNode';
import { useCanvasStore } from '../../stores/canvasStore';

const nodeTypes = {
  custom: WorkflowNode,
};

const initialNodes = [
  {
    id: '1',
    type: 'custom',
    position: { x: 250, y: 100 },
    data: {
      label: 'Bot de Vendas',
      type: 'botVendas',
      icon: '🏷️',
      status: 'Ativo',
      statusColor: '#22c55e',
      metrics: [
        { label: 'Modelo', value: 'Claude 3.5' },
        { label: 'Respostas', value: '234/dia' },
      ],
    },
  },
  {
    id: '2',
    type: 'custom',
    position: { x: 250, y: 280 },
    data: {
      label: 'WhatsApp',
      type: 'whatsapp',
      icon: '📱',
      status: 'Conectado',
      statusColor: '#22c55e',
      metrics: [
        { label: 'Número', value: '+55 67 9xxxx' },
        { label: 'Mensagens', value: '1.2k/dia' },
      ],
    },
  },
  {
    id: '3',
    type: 'custom',
    position: { x: 550, y: 100 },
    data: {
      label: 'Bot de Suporte',
      type: 'botSuporte',
      icon: '💬',
      status: 'Ativo',
      statusColor: '#22c55e',
      metrics: [
        { label: 'Tickets', value: '23 abertos' },
        { label: 'SLA', value: '< 2h' },
      ],
    },
  },
  {
    id: '4',
    type: 'custom',
    position: { x: 550, y: 280 },
    data: {
      label: 'Monitor Inversor',
      type: 'inversor',
      icon: '⚡',
      status: 'Online',
      statusColor: '#22c55e',
      metrics: [
        { label: 'Plataformas', value: 'Solis, Growatt' },
        { label: 'Inversores', value: '42 online' },
      ],
    },
  },
  {
    id: '5',
    type: 'custom',
    position: { x: 400, y: 450 },
    data: {
      label: 'Gerador PDF',
      type: 'orcamento',
      icon: '📄',
      metrics: [
        { label: 'Template', value: 'Padrão v2' },
        { label: 'Gerados hoje', value: '47' },
      ],
    },
  },
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e2-3', source: '2', target: '3', animated: true },
  { id: 'e2-4', source: '2', target: '4', animated: true },
  { id: 'e3-5', source: '3', target: '5' },
  { id: 'e4-5', source: '4', target: '5' },
];

export const WorkflowCanvas: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const { setSelectedNode, setNodes: setStoreNodes } = useCanvasStore();

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: any) => {
      setSelectedNode(node);
    },
    [setSelectedNode]
  );
  
  // Sync nodes to store
  React.useEffect(() => {
    setStoreNodes(nodes as any);
  }, [nodes, setStoreNodes]);

  return (
    <div className="flex-1 bg-[#0a0a0a]">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        fitView
        className="bg-[#0a0a0a]"
      >
        <Background color="#2a2a2a" gap={16} />
        <Controls className="bg-[#1a1a1a] border border-[#2a2a2a]" />
        <MiniMap
          className="bg-[#1a1a1a] border border-[#2a2a2a]"
          nodeColor="#3b82f6"
          maskColor="rgba(10, 10, 10, 0.6)"
        />
      </ReactFlow>
    </div>
  );
};
