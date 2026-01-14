"use client"

import { Users, UserCheck, UserX, UserPlus } from "lucide-react"
import { StatsCard } from "@/components/stats-card"
import { UsersTable } from "@/components/users-table"

const stats = [
  {
    title: "Total de Usuários",
    value: "2,847",
    change: "+12.5% este mês",
    changeType: "positive" as const,
    icon: Users,
  },
  {
    title: "Usuários Ativos",
    value: "2,156",
    change: "75.7% do total",
    changeType: "neutral" as const,
    icon: UserCheck,
  },
  {
    title: "Usuários Inativos",
    value: "584",
    change: "-8.2% este mês",
    changeType: "positive" as const,
    icon: UserX,
  },
  {
    title: "Novos Este Mês",
    value: "127",
    change: "+23 vs mês passado",
    changeType: "positive" as const,
    icon: UserPlus,
  },
]

export function UsersContent() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Usuários</h1>
        <p className="text-muted-foreground mt-1">Gerencie os usuários da plataforma</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <StatsCard key={stat.title} {...stat} />
        ))}
      </div>

      {/* Users Table */}
      <UsersTable />
    </div>
  )
}
