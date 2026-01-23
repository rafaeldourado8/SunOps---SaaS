import { NavLink } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { 
  FiHome, 
  FiUsers, 
  FiFileText, 
  FiSettings, 
  FiFile, 
  FiLogOut,
  FiClock
} from 'react-icons/fi';
import { FaSolarPanel } from 'react-icons/fa';
import useAuthStore from '../store/authStore';

const Sidebar = () => {
  const { user, logout, lastActivity } = useAuthStore();
  const [timeLeft, setTimeLeft] = useState(240); // 4 minutos em segundos
  
  const navItems = [
    { to: '/', icon: FiHome, label: 'Dashboard' },
    { to: '/clientes', icon: FiUsers, label: 'Clientes' },
    { to: '/propostas', icon: FiFileText, label: 'Propostas' },
    { to: '/premissas', icon: FaSolarPanel, label: 'Premissas' },
    { to: '/templates', icon: FiFile, label: 'Templates' },
    { to: '/configuracoes', icon: FiSettings, label: 'Configurações' },
  ];

  // Atualizar contador de timeout
  useEffect(() => {
    const interval = setInterval(() => {
      if (lastActivity) {
        const elapsed = Date.now() - lastActivity;
        const remaining = Math.max(0, 240 - Math.floor(elapsed / 1000));
        setTimeLeft(remaining);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [lastActivity]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getTimeColor = () => {
    if (timeLeft > 120) return 'text-green-400';
    if (timeLeft > 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="w-64 bg-dark-900 border-r border-dark-800 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-dark-800">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-gradient-solar rounded-lg">
            <FaSolarPanel className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">SunOPS</h1>
            <p className="text-xs text-gray-400">Energy Solutions</p>
          </div>
        </div>
      </div>

      {/* Menu */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-solar-500/20 text-solar-400 border-l-4 border-solar-500'
                  : 'text-gray-400 hover:text-gray-300 hover:bg-white/5'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Timeout Indicator */}
      <div className="px-4 py-3 border-t border-dark-800">
        <div className="flex items-center justify-between p-3 bg-dark-800/50 rounded-lg">
          <div className="flex items-center gap-2">
            <FiClock className="w-4 h-4 text-gray-400" />
            <span className="text-xs text-gray-400">Sessão expira em</span>
          </div>
          <span className={`text-sm font-mono font-bold ${getTimeColor()}`}>
            {formatTime(timeLeft)}
          </span>
        </div>
      </div>

      {/* User Info */}
      <div className="p-4 border-t border-dark-800">
        <div className="flex items-center justify-between">
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">{user?.name}</p>
            <p className="text-xs text-gray-400 truncate">{user?.email}</p>
          </div>
          <button
            onClick={logout}
            className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors flex-shrink-0 ml-2"
            title="Sair"
          >
            <FiLogOut className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;