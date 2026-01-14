"use client"

import { Users, BarChart3, FolderOpen, TrendingUp } from "lucide-react"
import { StatsCard } from "@/components/stats-card"
import { RecentActivity } from "@/components/recent-activity"

const stats = [
  {
    title: "Total de Usuários",
    value: "2,847",
    change: "+12.5% este mês",
    changeType: "positive" as const,
    icon: Users,
  },
  {
    title: "Projetos Ativos",
    value: "184",
    change: "+4 novos esta semana",
    changeType: "positive" as const,
    icon: FolderOpen,
  },
  {
    title: "Taxa de Conversão",
    value: "24.8%",
    change: "-2.1% desde ontem",
    changeType: "negative" as const,
    icon: TrendingUp,
  },
  {
    title: "Receita Mensal",
    value: "R$ 45.2k",
    change: "+8.3% este mês",
    changeType: "positive" as const,
    icon: BarChart3,
  },
]

export function DashboardContent() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
        <p className="text-muted-foreground mt-1">Visão geral das métricas e atividades</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <StatsCard key={stat.title} {...stat} />
        ))}
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart Placeholder */}
        <div className="lg:col-span-2 rounded-xl bg-card border border-border p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Visão Geral</h3>
          <div className="h-64 flex items-center justify-center border border-dashed border-border rounded-lg">
            <span className="text-muted-foreground text-sm">Gráfico de Analytics</span>
          </div>
        </div>

        {/* Recent Activity */}
        <RecentActivity />
      </div>
    </div>
  )
}
