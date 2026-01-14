import { cn } from "@/lib/utils"
import type { LucideIcon } from "lucide-react"

interface StatsCardProps {
  title: string
  value: string
  change?: string
  changeType?: "positive" | "negative" | "neutral"
  icon: LucideIcon
}

export function StatsCard({ title, value, change, changeType = "neutral", icon: Icon }: StatsCardProps) {
  return (
    <div className="p-6 rounded-xl bg-card border border-border hover:border-ring/50 transition-colors">
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-sm text-muted-foreground">{title}</p>
          <p className="text-2xl font-semibold text-foreground">{value}</p>
        </div>
        <div className="p-2.5 rounded-lg bg-secondary">
          <Icon size={20} className="text-muted-foreground" />
        </div>
      </div>
      {change && (
        <p
          className={cn(
            "text-sm mt-3",
            changeType === "positive" && "text-chart-1",
            changeType === "negative" && "text-destructive",
            changeType === "neutral" && "text-muted-foreground",
          )}
        >
          {change}
        </p>
      )}
    </div>
  )
}
