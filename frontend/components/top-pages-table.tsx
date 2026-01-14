"use client"

import { ArrowUpRight, ArrowDownRight } from "lucide-react"

const topPages = [
  { page: "/dashboard", views: "12,847", change: "+15.2%", isPositive: true },
  { page: "/products", views: "8,432", change: "+8.7%", isPositive: true },
  { page: "/checkout", views: "6,218", change: "-2.4%", isPositive: false },
  { page: "/users/profile", views: "4,891", change: "+12.1%", isPositive: true },
  { page: "/settings", views: "3,654", change: "+5.8%", isPositive: true },
]

export function TopPagesTable() {
  return (
    <div className="p-6 rounded-xl bg-card border border-border">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-foreground">Páginas Mais Visitadas</h3>
        <p className="text-sm text-muted-foreground mt-1">Top 5 páginas por visualizações</p>
      </div>
      <div className="space-y-4">
        {topPages.map((item, index) => (
          <div key={item.page} className="flex items-center justify-between py-3 border-b border-border last:border-0">
            <div className="flex items-center gap-4">
              <span className="text-sm text-muted-foreground w-6">{index + 1}</span>
              <span className="text-sm font-medium text-foreground">{item.page}</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-foreground">{item.views}</span>
              <div
                className={`flex items-center gap-1 text-sm ${item.isPositive ? "text-chart-1" : "text-destructive"}`}
              >
                {item.isPositive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
                {item.change}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
