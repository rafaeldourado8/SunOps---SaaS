import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  iconColor: string;
}

export function StatCard({ label, value, icon: Icon, iconColor }: StatCardProps) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-400 text-sm">{label}</p>
          <p className="text-white text-3xl font-bold mt-2">{value}</p>
        </div>
        <Icon className="w-12 h-12" style={{ color: iconColor }} />
      </div>
    </div>
  );
}
