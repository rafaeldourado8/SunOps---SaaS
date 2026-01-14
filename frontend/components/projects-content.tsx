"use client"

import { useState } from "react"
import { FolderKanban, CheckCircle2, Clock, PauseCircle, Plus, Search, Filter, LayoutGrid, List } from "lucide-react"
import { StatsCard } from "@/components/stats-card"
import { ProjectCard } from "@/components/project-card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { cn } from "@/lib/utils"

const stats = [
  {
    title: "Total de Projetos",
    value: "24",
    change: "+3 este mês",
    changeType: "positive" as const,
    icon: FolderKanban,
  },
  {
    title: "Em Andamento",
    value: "12",
    change: "50% do total",
    changeType: "neutral" as const,
    icon: Clock,
  },
  {
    title: "Concluídos",
    value: "8",
    change: "+2 esta semana",
    changeType: "positive" as const,
    icon: CheckCircle2,
  },
  {
    title: "Pausados",
    value: "4",
    change: "-1 vs semana passada",
    changeType: "positive" as const,
    icon: PauseCircle,
  },
]

const projects = [
  {
    name: "Redesign do Website",
    description: "Atualização completa do site institucional com nova identidade visual",
    status: "em andamento" as const,
    progress: 75,
    dueDate: "15 Mar 2026",
    members: [
      { name: "Ana", avatar: "A" },
      { name: "Carlos", avatar: "C" },
      { name: "Maria", avatar: "M" },
    ],
    category: "Design",
  },
  {
    name: "App Mobile v2.0",
    description: "Nova versão do aplicativo com funcionalidades de pagamento integrado",
    status: "em andamento" as const,
    progress: 45,
    dueDate: "28 Fev 2026",
    members: [
      { name: "João", avatar: "J" },
      { name: "Pedro", avatar: "P" },
    ],
    category: "Desenvolvimento",
  },
  {
    name: "Sistema de CRM",
    description: "Implementação de sistema de gestão de relacionamento com clientes",
    status: "planejamento" as const,
    progress: 10,
    dueDate: "30 Abr 2026",
    members: [
      { name: "Lucas", avatar: "L" },
      { name: "Fernanda", avatar: "F" },
      { name: "Rafael", avatar: "R" },
      { name: "Julia", avatar: "J" },
    ],
    category: "Infraestrutura",
  },
  {
    name: "Campanha Q1 2026",
    description: "Planejamento e execução da campanha de marketing do primeiro trimestre",
    status: "concluído" as const,
    progress: 100,
    dueDate: "10 Jan 2026",
    members: [
      { name: "Beatriz", avatar: "B" },
      { name: "Diego", avatar: "D" },
    ],
    category: "Marketing",
  },
  {
    name: "Migração Cloud",
    description: "Migração de servidores on-premise para infraestrutura em nuvem",
    status: "pausado" as const,
    progress: 30,
    dueDate: "20 Mar 2026",
    members: [{ name: "Thiago", avatar: "T" }],
    category: "Infraestrutura",
  },
  {
    name: "Dashboard Analytics",
    description: "Desenvolvimento de painel de métricas e análises em tempo real",
    status: "em andamento" as const,
    progress: 60,
    dueDate: "05 Fev 2026",
    members: [
      { name: "Camila", avatar: "C" },
      { name: "Eduardo", avatar: "E" },
      { name: "Isabela", avatar: "I" },
    ],
    category: "Desenvolvimento",
  },
  {
    name: "Treinamento Equipe",
    description: "Programa de capacitação em novas tecnologias para a equipe de TI",
    status: "concluído" as const,
    progress: 100,
    dueDate: "05 Jan 2026",
    members: [
      { name: "Roberto", avatar: "R" },
      { name: "Mariana", avatar: "M" },
    ],
    category: "RH",
  },
  {
    name: "Integração API Parceiros",
    description: "Desenvolvimento de APIs para integração com sistemas de parceiros",
    status: "em andamento" as const,
    progress: 55,
    dueDate: "18 Feb 2026",
    members: [
      { name: "Felipe", avatar: "F" },
      { name: "Amanda", avatar: "A" },
    ],
    category: "Desenvolvimento",
  },
]

export function ProjectsContent() {
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid")
  const [search, setSearch] = useState("")

  const filteredProjects = projects.filter((project) => project.name.toLowerCase().includes(search.toLowerCase()))

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Projetos</h1>
          <p className="text-muted-foreground mt-1">Gerencie e acompanhe todos os projetos</p>
        </div>
        <Button className="bg-foreground text-background hover:bg-foreground/90">
          <Plus size={16} className="mr-2" />
          Novo Projeto
        </Button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <StatsCard key={stat.title} {...stat} />
        ))}
      </div>

      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row gap-3 p-4 rounded-xl bg-card border border-border">
        <div className="relative flex-1">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Buscar projetos..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9 bg-secondary border-transparent focus:border-ring"
          />
        </div>
        <div className="flex gap-2">
          <Select defaultValue="todos">
            <SelectTrigger className="w-[140px] bg-secondary border-transparent">
              <Filter size={14} className="mr-2 text-muted-foreground" />
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="todos">Todos</SelectItem>
              <SelectItem value="em andamento">Em andamento</SelectItem>
              <SelectItem value="concluído">Concluídos</SelectItem>
              <SelectItem value="pausado">Pausados</SelectItem>
              <SelectItem value="planejamento">Planejamento</SelectItem>
            </SelectContent>
          </Select>
          <Select defaultValue="todas">
            <SelectTrigger className="w-[140px] bg-secondary border-transparent">
              <SelectValue placeholder="Categoria" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="todas">Todas</SelectItem>
              <SelectItem value="design">Design</SelectItem>
              <SelectItem value="desenvolvimento">Desenvolvimento</SelectItem>
              <SelectItem value="marketing">Marketing</SelectItem>
              <SelectItem value="infraestrutura">Infraestrutura</SelectItem>
              <SelectItem value="rh">RH</SelectItem>
            </SelectContent>
          </Select>
          <div className="flex rounded-lg bg-secondary p-1">
            <Button
              variant="ghost"
              size="icon"
              className={cn("h-8 w-8", viewMode === "grid" && "bg-background")}
              onClick={() => setViewMode("grid")}
            >
              <LayoutGrid size={16} />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className={cn("h-8 w-8", viewMode === "list" && "bg-background")}
              onClick={() => setViewMode("list")}
            >
              <List size={16} />
            </Button>
          </div>
        </div>
      </div>

      {/* Projects Grid */}
      <div
        className={cn("grid gap-4", viewMode === "grid" ? "grid-cols-1 md:grid-cols-2 xl:grid-cols-3" : "grid-cols-1")}
      >
        {filteredProjects.map((project) => (
          <ProjectCard key={project.name} {...project} />
        ))}
      </div>

      {/* Empty State */}
      {filteredProjects.length === 0 && (
        <div className="text-center py-12">
          <FolderKanban size={48} className="mx-auto text-muted-foreground/50 mb-4" />
          <h3 className="text-lg font-medium text-foreground mb-1">Nenhum projeto encontrado</h3>
          <p className="text-muted-foreground">Tente ajustar os filtros ou criar um novo projeto</p>
        </div>
      )}
    </div>
  )
}
