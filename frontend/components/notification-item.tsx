"use client"

import { cn } from "@/lib/utils"
import { Check, Trash2, MoreHorizontal } from "lucide-react"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import type { LucideIcon } from "lucide-react"

interface NotificationItemProps {
  id: string
  title: string
  description: string
  time: string
  read: boolean
  icon: LucideIcon
  iconColor: string
  iconBg: string
  onMarkAsRead?: (id: string) => void
  onDelete?: (id: string) => void
}

export function NotificationItem({
  id,
  title,
  description,
  time,
  read,
  icon: Icon,
  iconColor,
  iconBg,
  onMarkAsRead,
  onDelete,
}: NotificationItemProps) {
  return (
    <div
      className={cn(
        "relative flex items-start gap-4 p-4 rounded-xl border border-border transition-colors",
        read ? "bg-card" : "bg-secondary/50",
      )}
    >
      {!read && <div className="absolute top-4 right-4 w-2 h-2 rounded-full bg-chart-2" />}
      <div className={cn("p-2.5 rounded-lg shrink-0", iconBg)}>
        <Icon size={18} className={iconColor} />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <div className="space-y-1">
            <p className={cn("text-sm font-medium", read ? "text-muted-foreground" : "text-foreground")}>{title}</p>
            <p className="text-sm text-muted-foreground line-clamp-2">{description}</p>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8 shrink-0 mr-4">
                <MoreHorizontal size={16} />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {!read && (
                <DropdownMenuItem onClick={() => onMarkAsRead?.(id)}>
                  <Check size={14} className="mr-2" />
                  Marcar como lida
                </DropdownMenuItem>
              )}
              <DropdownMenuItem onClick={() => onDelete?.(id)} className="text-destructive">
                <Trash2 size={14} className="mr-2" />
                Excluir
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <p className="text-xs text-muted-foreground mt-2">{time}</p>
      </div>
    </div>
  )
}
