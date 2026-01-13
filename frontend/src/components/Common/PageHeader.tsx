interface PageHeaderProps {
  title: string;
  description: string;
  action?: React.ReactNode;
}

export function PageHeader({ title, description, action }: PageHeaderProps) {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h2 className="text-3xl font-bold text-white">{title}</h2>
        <p className="text-gray-400 mt-2">{description}</p>
      </div>
      {action}
    </div>
  );
}
