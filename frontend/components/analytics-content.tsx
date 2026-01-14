"use client"

import { TrendingUp, Eye, Clock, MousePointerClick } from "lucide-react"
import { StatsCard } from "@/components/stats-card"
import { AnalyticsChart } from "@/components/analytics-chart"
import { AnalyticsBarChart } from "@/components/analytics-bar-chart"
import { TopPagesTable } from "@/components/top-pages-table"

const stats = [
  {
    title: "Visitantes Totais",
    value: "48,352",
    change: "+18.2% vs mês passado",
    changeType: "positive" as const,
    icon: Eye,
  },
  {
    title: "Taxa de Conversão",
    value: "3.24%",
    change: "+0.8% vs mês passado",
    changeType: "positive" as const,
    icon: TrendingUp,
  },
  {
    title: "Tempo Médio",
    value: "4m 32s",
    change: "-12s vs mês passado",
    changeType: "negative" as const,
    icon: Clock,
  },
  {
    title: "Taxa de Cliques",
    value: "12.8%",
    change: "+2.1% vs mês passado",
    changeType: "positive" as const,
    icon: MousePointerClick,
  },
]

const revenueData = [
  { name: "Jan", value: 4000, value2: 2400 },
  { name: "Fev", value: 3000, value2: 1398 },
  { name: "Mar", value: 5000, value2: 3800 },
  { name: "Abr", value: 4780, value2: 3908 },
  { name: "Mai", value: 5890, value2: 4800 },
  { name: "Jun", value: 6390, value2: 3800 },
  { name: "Jul", value: 7490, value2: 4300 },
  { name: "Ago", value: 6800, value2: 4100 },
  { name: "Set", value: 7200, value2: 4500 },
  { name: "Out", value: 8100, value2: 5200 },
  { name: "Nov", value: 8900, value2: 5800 },
  { name: "Dez", value: 9400, value2: 6100 },
]

const visitorsData = [
  { name: "Seg", value: 1200 },
  { name: "Ter", value: 1900 },
  { name: "Qua", value: 1600 },
  { name: "Qui", value: 2100 },
  { name: "Sex", value: 2400 },
  { name: "Sáb", value: 1100 },
  { name: "Dom", value: 800 },
]

export function AnalyticsContent() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Analytics</h1>
        <p className="text-muted-foreground mt-1">Acompanhe o desempenho da plataforma</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <StatsCard key={stat.title} {...stat} />
        ))}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AnalyticsChart
          title="Receita vs Custos"
          description="Comparativo mensal de receita e custos"
          data={revenueData}
          showSecondLine
        />
        <AnalyticsBarChart
          title="Visitantes por Dia"
          description="Distribuição semanal de visitantes"
          data={visitorsData}
        />
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TopPagesTable />
        <AnalyticsChart
          title="Crescimento de Usuários"
          description="Novos usuários registrados por mês"
          data={revenueData.map((d) => ({ name: d.name, value: Math.floor(d.value / 10) }))}
        />
      </div>
    </div>
  )
}
