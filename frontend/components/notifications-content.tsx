"use client"

import { useState } from "react"
import {
  Bell,
  BellOff,
  Check,
  CheckCheck,
  MessageSquare,
  UserPlus,
  AlertTriangle,
  Package,
  CreditCard,
  Settings,
  Filter,
} from "lucide-react"
import { StatsCard } from "@/components/stats-card"
import { NotificationItem } from "@/components/notification-item"
import { Button } from "@/components/ui/button"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface Notification {
  id: string
  title: string
  description: string
  time: string
  read: boolean
  type: "message" | "user" | "alert" | "order" | "payment" | "system"
}

const initialNotifications: Notification[] = [
  {
    id: "1",
    title: "Nova mensagem de Carlos Silva",
    description: "Olá, gostaria de saber mais sobre o projeto de redesign. Podemos agendar uma reunião?",
    time: "Há 5 minutos",
    read: false,
    type: "message",
  },
  {
    id: "2",
    title: "Novo usuário registrado",
    description: "Maria Santos acabou de criar uma conta na plataforma.",
    time: "Há 15 minutos",
    read: false,
    type: "user",
  },
  {
    id: "3",
    title: "Alerta de sistema",
    description: "O uso de CPU atingiu 85%. Considere otimizar os recursos ou fazer upgrade do plano.",
    time: "Há 1 hora",
    read: false,
    type: "alert",
  },
  {
    id: "4",
    title: "Novo pedido #12847",
    description: "Um novo pedido foi realizado no valor de R$ 1.250,00.",
    time: "Há 2 horas",
    read: true,
    type: "order",
  },
  {
    id: "5",
    title: "Pagamento confirmado",
    description: "O pagamento da fatura de Janeiro foi confirmado com sucesso.",
    time: "Há 3 horas",
    read: true,
    type: "payment",
  },
  {
    id: "6",
    title: "Atualização de sistema",
    description: "Uma nova versão do sistema está disponível. Clique para atualizar.",
    time: "Há 5 horas",
    read: true,
    type: "system",
  },
  {
    id: "7",
    title: "Comentário em projeto",
    description: "João Pedro comentou no projeto 'App Mobile v2.0': 'Excelente progresso!'",
    time: "Há 6 horas",
    read: true,
    type: "message",
  },
  {
    id: "8",
    title: "Convite para equipe",
    description: "Você foi convidado para participar da equipe 'Marketing Digital'.",
    time: "Ontem",
    read: true,
    type: "user",
  },
  {
    id: "9",
    title: "Limite de armazenamento",
    description: "Você está usando 90% do seu limite de armazenamento. Considere fazer upgrade.",
    time: "Ontem",
    read: true,
    type: "alert",
  },
  {
    id: "10",
    title: "Pedido enviado",
    description: "O pedido #12845 foi enviado e está a caminho do destino.",
    time: "2 dias atrás",
    read: true,
    type: "order",
  },
]

const typeConfig = {
  message: {
    icon: MessageSquare,
    iconColor: "text-chart-2",
    iconBg: "bg-chart-2/10",
  },
  user: {
    icon: UserPlus,
    iconColor: "text-chart-1",
    iconBg: "bg-chart-1/10",
  },
  alert: {
    icon: AlertTriangle,
    iconColor: "text-yellow-500",
    iconBg: "bg-yellow-500/10",
  },
  order: {
    icon: Package,
    iconColor: "text-purple-500",
    iconBg: "bg-purple-500/10",
  },
  payment: {
    icon: CreditCard,
    iconColor: "text-chart-1",
    iconBg: "bg-chart-1/10",
  },
  system: {
    icon: Settings,
    iconColor: "text-muted-foreground",
    iconBg: "bg-secondary",
  },
}

export function NotificationsContent() {
  const [notifications, setNotifications] = useState(initialNotifications)
  const [activeTab, setActiveTab] = useState("all")

  const unreadCount = notifications.filter((n) => !n.read).length
  const readCount = notifications.filter((n) => n.read).length

  const stats = [
    {
      title: "Total",
      value: notifications.length.toString(),
      change: "+5 hoje",
      changeType: "neutral" as const,
      icon: Bell,
    },
    {
      title: "Não Lidas",
      value: unreadCount.toString(),
      change: unreadCount > 0 ? "Requer atenção" : "Tudo em dia",
      changeType: unreadCount > 0 ? "negative" : ("positive" as const),
      icon: Bell,
    },
    {
      title: "Lidas",
      value: readCount.toString(),
      change: `${Math.round((readCount / notifications.length) * 100)}% do total`,
      changeType: "neutral" as const,
      icon: Check,
    },
    {
      title: "Alertas",
      value: notifications.filter((n) => n.type === "alert").length.toString(),
      change: "Monitorando",
      changeType: "neutral" as const,
      icon: AlertTriangle,
    },
  ]

  const filteredNotifications = notifications.filter((notification) => {
    if (activeTab === "all") return true
    if (activeTab === "unread") return !notification.read
    if (activeTab === "read") return notification.read
    return true
  })

  const handleMarkAsRead = (id: string) => {
    setNotifications((prev) => prev.map((n) => (n.id === id ? { ...n, read: true } : n)))
  }

  const handleMarkAllAsRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })))
  }

  const handleDelete = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id))
  }

  const handleClearAll = () => {
    setNotifications([])
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Notificações</h1>
          <p className="text-muted-foreground mt-1">Gerencie suas notificações e alertas</p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={handleMarkAllAsRead}
            disabled={unreadCount === 0}
            className="border-border bg-transparent"
          >
            <CheckCheck size={16} className="mr-2" />
            Marcar todas como lidas
          </Button>
          <Button
            variant="outline"
            onClick={handleClearAll}
            disabled={notifications.length === 0}
            className="border-border text-destructive hover:text-destructive bg-transparent"
          >
            <BellOff size={16} className="mr-2" />
            Limpar tudo
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <StatsCard key={stat.title} {...stat} />
        ))}
      </div>

      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row gap-3 p-4 rounded-xl bg-card border border-border">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1">
          <TabsList className="bg-secondary">
            <TabsTrigger value="all">Todas ({notifications.length})</TabsTrigger>
            <TabsTrigger value="unread">Não lidas ({unreadCount})</TabsTrigger>
            <TabsTrigger value="read">Lidas ({readCount})</TabsTrigger>
          </TabsList>
        </Tabs>
        <Select defaultValue="all">
          <SelectTrigger className="w-[160px] bg-secondary border-transparent">
            <Filter size={14} className="mr-2 text-muted-foreground" />
            <SelectValue placeholder="Tipo" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Todos os tipos</SelectItem>
            <SelectItem value="message">Mensagens</SelectItem>
            <SelectItem value="user">Usuários</SelectItem>
            <SelectItem value="alert">Alertas</SelectItem>
            <SelectItem value="order">Pedidos</SelectItem>
            <SelectItem value="payment">Pagamentos</SelectItem>
            <SelectItem value="system">Sistema</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Notifications List */}
      <div className="space-y-3">
        {filteredNotifications.map((notification) => {
          const config = typeConfig[notification.type]
          return (
            <NotificationItem
              key={notification.id}
              id={notification.id}
              title={notification.title}
              description={notification.description}
              time={notification.time}
              read={notification.read}
              icon={config.icon}
              iconColor={config.iconColor}
              iconBg={config.iconBg}
              onMarkAsRead={handleMarkAsRead}
              onDelete={handleDelete}
            />
          )
        })}
      </div>

      {/* Empty State */}
      {filteredNotifications.length === 0 && (
        <div className="text-center py-12">
          <Bell size={48} className="mx-auto text-muted-foreground/50 mb-4" />
          <h3 className="text-lg font-medium text-foreground mb-1">Nenhuma notificação</h3>
          <p className="text-muted-foreground">
            {activeTab === "unread"
              ? "Você não tem notificações não lidas"
              : activeTab === "read"
                ? "Você não tem notificações lidas"
                : "Você não tem notificações ainda"}
          </p>
        </div>
      )}
    </div>
  )
}
