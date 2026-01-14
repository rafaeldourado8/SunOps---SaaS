"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"
import {
  MoreHorizontal,
  Search,
  Filter,
  UserPlus,
  Mail,
  Shield,
  Ban,
  Trash2,
  Edit,
  ChevronLeft,
  ChevronRight,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

interface User {
  id: string
  name: string
  email: string
  role: "admin" | "editor" | "viewer"
  status: "active" | "inactive" | "pending"
  avatar: string
  lastActive: string
}

const users: User[] = [
  {
    id: "1",
    name: "Ana Silva",
    email: "ana.silva@email.com",
    role: "admin",
    status: "active",
    avatar: "AS",
    lastActive: "Agora",
  },
  {
    id: "2",
    name: "Bruno Costa",
    email: "bruno.costa@email.com",
    role: "editor",
    status: "active",
    avatar: "BC",
    lastActive: "2h atrás",
  },
  {
    id: "3",
    name: "Carla Mendes",
    email: "carla.mendes@email.com",
    role: "viewer",
    status: "inactive",
    avatar: "CM",
    lastActive: "3 dias atrás",
  },
  {
    id: "4",
    name: "Daniel Oliveira",
    email: "daniel.oliveira@email.com",
    role: "editor",
    status: "active",
    avatar: "DO",
    lastActive: "1h atrás",
  },
  {
    id: "5",
    name: "Elena Rodrigues",
    email: "elena.rodrigues@email.com",
    role: "viewer",
    status: "pending",
    avatar: "ER",
    lastActive: "Nunca",
  },
  {
    id: "6",
    name: "Felipe Santos",
    email: "felipe.santos@email.com",
    role: "admin",
    status: "active",
    avatar: "FS",
    lastActive: "30min atrás",
  },
  {
    id: "7",
    name: "Gabriela Lima",
    email: "gabriela.lima@email.com",
    role: "editor",
    status: "active",
    avatar: "GL",
    lastActive: "5h atrás",
  },
  {
    id: "8",
    name: "Henrique Alves",
    email: "henrique.alves@email.com",
    role: "viewer",
    status: "inactive",
    avatar: "HA",
    lastActive: "1 semana atrás",
  },
]

const roleLabels = {
  admin: "Administrador",
  editor: "Editor",
  viewer: "Visualizador",
}

const statusLabels = {
  active: "Ativo",
  inactive: "Inativo",
  pending: "Pendente",
}

export function UsersTable() {
  const [searchQuery, setSearchQuery] = useState("")

  const filteredUsers = users.filter(
    (user) =>
      user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
          <Input
            placeholder="Buscar usuários..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-secondary border-border"
          />
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="gap-2 bg-transparent">
            <Filter size={16} />
            <span className="hidden sm:inline">Filtrar</span>
          </Button>
          <Button size="sm" className="gap-2">
            <UserPlus size={16} />
            <span className="hidden sm:inline">Novo Usuário</span>
          </Button>
        </div>
      </div>

      {/* Table */}
      <div className="rounded-xl bg-card border border-border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border bg-secondary/50">
                <th className="text-left px-4 py-3 text-sm font-medium text-muted-foreground">Usuário</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-muted-foreground hidden md:table-cell">
                  Função
                </th>
                <th className="text-left px-4 py-3 text-sm font-medium text-muted-foreground hidden sm:table-cell">
                  Status
                </th>
                <th className="text-left px-4 py-3 text-sm font-medium text-muted-foreground hidden lg:table-cell">
                  Última Atividade
                </th>
                <th className="text-right px-4 py-3 text-sm font-medium text-muted-foreground">Ações</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map((user) => (
                <tr
                  key={user.id}
                  className="border-b border-border last:border-0 hover:bg-secondary/30 transition-colors"
                >
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full bg-secondary flex items-center justify-center text-sm font-medium text-foreground">
                        {user.avatar}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-foreground">{user.name}</p>
                        <p className="text-xs text-muted-foreground">{user.email}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 hidden md:table-cell">
                    <span
                      className={cn(
                        "text-xs font-medium px-2.5 py-1 rounded-full",
                        user.role === "admin" && "bg-chart-1/20 text-chart-1",
                        user.role === "editor" && "bg-chart-2/20 text-chart-2",
                        user.role === "viewer" && "bg-muted text-muted-foreground",
                      )}
                    >
                      {roleLabels[user.role]}
                    </span>
                  </td>
                  <td className="px-4 py-3 hidden sm:table-cell">
                    <span
                      className={cn(
                        "text-xs font-medium px-2.5 py-1 rounded-full",
                        user.status === "active" && "bg-chart-1/20 text-chart-1",
                        user.status === "inactive" && "bg-muted text-muted-foreground",
                        user.status === "pending" && "bg-chart-4/20 text-chart-4",
                      )}
                    >
                      {statusLabels[user.status]}
                    </span>
                  </td>
                  <td className="px-4 py-3 hidden lg:table-cell">
                    <span className="text-sm text-muted-foreground">{user.lastActive}</span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <MoreHorizontal size={16} />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end" className="w-48">
                        <DropdownMenuItem className="gap-2">
                          <Edit size={14} />
                          Editar
                        </DropdownMenuItem>
                        <DropdownMenuItem className="gap-2">
                          <Mail size={14} />
                          Enviar Email
                        </DropdownMenuItem>
                        <DropdownMenuItem className="gap-2">
                          <Shield size={14} />
                          Alterar Função
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="gap-2 text-chart-4">
                          <Ban size={14} />
                          Desativar
                        </DropdownMenuItem>
                        <DropdownMenuItem className="gap-2 text-destructive">
                          <Trash2 size={14} />
                          Excluir
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between px-4 py-3 border-t border-border">
          <p className="text-sm text-muted-foreground">
            Mostrando <span className="font-medium text-foreground">{filteredUsers.length}</span> de{" "}
            <span className="font-medium text-foreground">{users.length}</span> usuários
          </p>
          <div className="flex items-center gap-1">
            <Button variant="ghost" size="icon" className="h-8 w-8" disabled>
              <ChevronLeft size={16} />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 w-8 bg-secondary">
              1
            </Button>
            <Button variant="ghost" size="sm" className="h-8 w-8">
              2
            </Button>
            <Button variant="ghost" size="icon" className="h-8 w-8">
              <ChevronRight size={16} />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
