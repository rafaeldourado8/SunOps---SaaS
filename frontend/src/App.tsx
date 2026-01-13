import { Login } from './components/Login';
import { useAuthStore } from './stores/authStore';
import { Toolbar } from './components/Canvas/Toolbar';
import { NodePalette } from './components/Sidebar/NodePalette';
import { ConfigPanel } from './components/Sidebar/ConfigPanel';
import { WorkflowCanvas } from './components/Canvas/WorkflowCanvas';
import { Dashboard } from './components/Dashboard/Dashboard';
import { TicketsPage } from './components/Pages/TicketsPage';
import { WhatsAppPage } from './components/Pages/WhatsAppPage';
import { useCanvasStore } from './stores/canvasStore';

function App() {
  const { selectedNode, viewMode } = useCanvasStore();
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-[#0a0a0a]">
      <Toolbar />

      <div className="flex-1 flex overflow-hidden">
        {viewMode === 'canvas' ? (
          <>
            <NodePalette />
            <WorkflowCanvas />
            {selectedNode && <ConfigPanel />}
          </>
        ) : viewMode === 'tickets' ? (
          <TicketsPage />
        ) : viewMode === 'whatsapp' ? (
          <WhatsAppPage />
        ) : (
          <Dashboard />
        )}
      </div>
    </div>
  );
}

export default App;
