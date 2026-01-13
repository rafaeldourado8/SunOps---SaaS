import { LogOut } from 'lucide-react';

interface UserProfileProps {
  email: string;
  onLogout: () => void;
}

export function UserProfile({ email, onLogout }: UserProfileProps) {
  return (
    <div className="p-4 border-t border-gray-700">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 rounded-full bg-yellow-500 flex items-center justify-center text-gray-900 font-bold">
          {email[0]?.toUpperCase() || 'U'}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-white text-sm font-medium truncate">{email}</p>
          <p className="text-gray-400 text-xs">Administrador</p>
        </div>
      </div>
      <button
        onClick={onLogout}
        className="w-full flex items-center gap-2 px-4 py-2 text-red-400 hover:bg-gray-700 rounded-lg transition"
      >
        <LogOut className="w-4 h-4" />
        <span className="text-sm">Sair</span>
      </button>
    </div>
  );
}
