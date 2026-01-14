import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const activities = [
  {
    id: 1,
    user: "João Silva",
    action: "criou um novo projeto",
    time: "2 min atrás",
    avatar: "JS",
  },
  {
    id: 2,
    user: "Maria Santos",
    action: "atualizou configurações",
    time: "15 min atrás",
    avatar: "MS",
  },
  {
    id: 3,
    user: "Pedro Costa",
    action: "adicionou novo usuário",
    time: "1 hora atrás",
    avatar: "PC",
  },
  {
    id: 4,
    user: "Ana Oliveira",
    action: "exportou relatório",
    time: "3 horas atrás",
    avatar: "AO",
  },
  {
    id: 5,
    user: "Carlos Lima",
    action: "completou uma tarefa",
    time: "5 horas atrás",
    avatar: "CL",
  },
]

export function RecentActivity() {
  return (
    <div className="rounded-xl bg-card border border-border p-6">
      <h3 className="text-lg font-semibold text-foreground mb-4">Atividade Recente</h3>
      <div className="space-y-4">
        {activities.map((activity) => (
          <div key={activity.id} className="flex items-center gap-4 py-2 border-b border-border last:border-0">
            <Avatar className="h-9 w-9">
              <AvatarImage src={`/.jpg?height=36&width=36&query=${activity.user} avatar`} />
              <AvatarFallback className="bg-secondary text-foreground text-xs">{activity.avatar}</AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-foreground">
                <span className="font-medium">{activity.user}</span>{" "}
                <span className="text-muted-foreground">{activity.action}</span>
              </p>
            </div>
            <span className="text-xs text-muted-foreground whitespace-nowrap">{activity.time}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
