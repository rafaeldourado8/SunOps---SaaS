"use client"

import { MoreHorizontal, Calendar, Users, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { cn } from "@/lib/utils"

interface ProjectCardProps {
  name: string
  description: string
  status: "em andamento" | "concluído" | "pausado" | "planejamento"
  progress: number
  dueDate: string
  members: { name: string; avatar: string }[]
  category: string
}

const statusStyles = {
  "em andamento": "bg-chart-2/10 text-chart-2 border-chart-2/20",
  concluído: "bg-chart-1/10 text-chart-1 border-chart-1/20",
  pausado: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20",
  planejamento: "bg-muted text-muted-foreground border-border",
}

export function ProjectCard({ name, description, status, progress, dueDate, members, category }: ProjectCardProps) {
  return (
    <div className="p-5 rounded-xl bg-card border border-border hover:border-ring/50 transition-all group">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="outline" className="text-xs font-normal text-muted-foreground">
              {category}
            </Badge>
          </div>
          <h3 className="font-semibold text-foreground truncate">{name}</h3>
          <p className="text-sm text-muted-foreground line-clamp-2 mt-1">{description}</p>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <MoreHorizontal size={16} />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-48">
            <DropdownMenuItem>
              <ExternalLink size={14} className="mr-2" />
              Abrir projeto
            </DropdownMenuItem>
            <DropdownMenuItem>Editar</DropdownMenuItem>
            <DropdownMenuItem>Duplicar</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem className="text-destructive">Arquivar</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between text-xs mb-1.5">
          <span className="text-muted-foreground">Progresso</span>
          <span className="text-foreground font-medium">{progress}%</span>
        </div>
        <div className="h-1.5 bg-secondary rounded-full overflow-hidden">
          <div
            className={cn("h-full rounded-full transition-all", progress === 100 ? "bg-chart-1" : "bg-chart-2")}
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between pt-3 border-t border-border">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Calendar size={14} />
            <span>{dueDate}</span>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Users size={14} />
            <span>{members.length}</span>
          </div>
        </div>
        <Badge variant="outline" className={cn("text-xs font-normal border", statusStyles[status])}>
          {status}
        </Badge>
      </div>
    </div>
  )
}
