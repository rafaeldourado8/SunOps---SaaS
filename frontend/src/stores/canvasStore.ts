import { create } from 'zustand';
import { WorkflowNode } from '../types';
import { api } from '../lib/api';

interface CanvasStore {
  nodes: WorkflowNode[];
  selectedNode: WorkflowNode | null;
  workflowName: string;
  workflowId: string | null;
  viewMode: 'canvas' | 'dashboard';
  setNodes: (nodes: WorkflowNode[]) => void;
  setSelectedNode: (node: WorkflowNode | null) => void;
  setWorkflowName: (name: string) => void;
  setWorkflowId: (id: string | null) => void;
  setViewMode: (mode: 'canvas' | 'dashboard') => void;
  addNode: (node: WorkflowNode) => void;
  updateNode: (id: string, data: Partial<WorkflowNode>) => void;
  saveWorkflow: () => Promise<void>;
  executeWorkflow: () => Promise<void>;
  loadWorkflows: () => Promise<any[]>;
}

export const useCanvasStore = create<CanvasStore>((set, get) => ({
  nodes: [],
  selectedNode: null,
  workflowName: 'Workflow SunwOps',
  workflowId: null,
  viewMode: 'canvas',
  setNodes: (nodes) => set({ nodes }),
  setSelectedNode: (node) => set({ selectedNode: node }),
  setWorkflowName: (name) => set({ workflowName: name }),
  setWorkflowId: (id) => set({ workflowId: id }),
  setViewMode: (mode) => set({ viewMode: mode }),
  addNode: (node) => set((state) => ({ nodes: [...state.nodes, node] })),
  updateNode: (id, data) =>
    set((state) => ({
      nodes: state.nodes.map((n) => 
        n.id === id 
          ? { ...n, data: { ...n.data, ...data } } 
          : n
      ),
      selectedNode: state.selectedNode?.id === id 
        ? { ...state.selectedNode, data: { ...state.selectedNode.data, ...data } }
        : state.selectedNode
    })),
  saveWorkflow: async () => {
    const { workflowName, workflowId, nodes } = get();
    const data_json = { nodes };
    
    try {
      if (workflowId) {
        await api.updateWorkflow(workflowId, workflowName, data_json);
      } else {
        const result = await api.createWorkflow(workflowName, data_json);
        set({ workflowId: result.id });
      }
    } catch (error) {
      console.error('Error saving workflow:', error);
      throw error;
    }
  },
  executeWorkflow: async () => {
    const { workflowId } = get();
    if (!workflowId) {
      throw new Error('No workflow to execute');
    }
    
    try {
      await api.executeWorkflow(workflowId);
    } catch (error) {
      console.error('Error executing workflow:', error);
      throw error;
    }
  },
  loadWorkflows: async () => {
    try {
      return await api.listWorkflows();
    } catch (error) {
      console.error('Error loading workflows:', error);
      throw error;
    }
  },
}));
