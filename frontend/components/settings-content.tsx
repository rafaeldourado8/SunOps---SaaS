"use client"

import { useState } from "react"
import {
  User,
  Bell,
  Shield,
  Palette,
  Globe,
  Key,
  Monitor,
  Moon,
  Sun,
  Mail,
  Smartphone,
  Save,
  Camera,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export function SettingsContent() {
  const [activeTab, setActiveTab] = useState("profile")
  const [theme, setTheme] = useState("dark")

  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    marketing: false,
    updates: true,
    security: true,
  })

  const [privacy, setPrivacy] = useState({
    profilePublic: false,
    showEmail: false,
    showActivity: true,
    twoFactor: false,
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Configurações</h1>
        <p className="text-muted-foreground mt-1">Gerencie suas preferências e configurações da conta</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <div className="p-1 rounded-xl bg-card border border-border">
          <TabsList className="bg-transparent w-full flex flex-wrap gap-1">
            <TabsTrigger value="profile" className="flex-1 min-w-[120px] data-[state=active]:bg-secondary">
              <User size={16} className="mr-2" />
              Perfil
            </TabsTrigger>
            <TabsTrigger value="notifications" className="flex-1 min-w-[120px] data-[state=active]:bg-secondary">
              <Bell size={16} className="mr-2" />
              Notificações
            </TabsTrigger>
            <TabsTrigger value="privacy" className="flex-1 min-w-[120px] data-[state=active]:bg-secondary">
              <Shield size={16} className="mr-2" />
              Privacidade
            </TabsTrigger>
            <TabsTrigger value="appearance" className="flex-1 min-w-[120px] data-[state=active]:bg-secondary">
              <Palette size={16} className="mr-2" />
              Aparência
            </TabsTrigger>
          </TabsList>
        </div>

        <TabsContent value="profile" className="space-y-6">
          <div className="p-6 rounded-xl bg-card border border-border">
            <h2 className="text-lg font-semibold text-foreground mb-6">Informações Pessoais</h2>

            <div className="flex items-center gap-6 mb-8">
              <div className="relative">
                <Avatar className="h-24 w-24 border-2 border-border">
                  <AvatarImage src="/diverse-user-avatars.png" alt="Avatar" />
                  <AvatarFallback className="bg-secondary text-2xl">JD</AvatarFallback>
                </Avatar>
                <button className="absolute bottom-0 right-0 p-2 rounded-full bg-primary text-primary-foreground hover:bg-primary/90 transition-colors">
                  <Camera size={14} />
                </button>
              </div>
              <div>
                <h3 className="font-medium text-foreground">Foto de Perfil</h3>
                <p className="text-sm text-muted-foreground mt-1">JPG, PNG ou GIF. Máximo 2MB.</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="firstName">Nome</Label>
                <Input id="firstName" defaultValue="João" className="bg-secondary border-transparent" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="lastName">Sobrenome</Label>
                <Input id="lastName" defaultValue="Da Silva" className="bg-secondary border-transparent" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  defaultValue="joao@exemplo.com"
                  className="bg-secondary border-transparent"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">Telefone</Label>
                <Input id="phone" defaultValue="+55 11 99999-9999" className="bg-secondary border-transparent" />
              </div>
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="bio">Bio</Label>
                <Textarea
                  id="bio"
                  placeholder="Conte um pouco sobre você..."
                  defaultValue="Desenvolvedor full-stack apaixonado por criar experiências digitais incríveis."
                  className="bg-secondary border-transparent min-h-[100px]"
                />
              </div>
            </div>

            <div className="flex justify-end mt-6">
              <Button>
                <Save size={16} className="mr-2" />
                Salvar Alterações
              </Button>
            </div>
          </div>

          <div className="p-6 rounded-xl bg-card border border-border">
            <h2 className="text-lg font-semibold text-foreground mb-6">Alterar Senha</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="currentPassword">Senha Atual</Label>
                <Input id="currentPassword" type="password" className="bg-secondary border-transparent" />
              </div>
              <div />
              <div className="space-y-2">
                <Label htmlFor="newPassword">Nova Senha</Label>
                <Input id="newPassword" type="password" className="bg-secondary border-transparent" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirmar Nova Senha</Label>
                <Input id="confirmPassword" type="password" className="bg-secondary border-transparent" />
              </div>
            </div>
            <div className="flex justify-end mt-6">
              <Button variant="outline" className="border-border bg-transparent">
                <Key size={16} className="mr-2" />
                Atualizar Senha
              </Button>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-6">
          <div className="p-6 rounded-xl bg-card border border-border">
            <h2 className="text-lg font-semibold text-foreground mb-6">Preferências de Notificação</h2>

            <div className="space-y-6">
              <div className="flex items-center justify-between py-3 border-b border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Mail size={18} className="text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground">Notificações por Email</h3>
                    <p className="text-sm text-muted-foreground">Receba atualizações importantes por email</p>
                  </div>
                </div>
                <Switch
                  checked={notifications.email}
                  onCheckedChange={(checked) => setNotifications((prev) => ({ ...prev, email: checked }))}
                />
              </div>

              <div className="flex items-center justify-between py-3 border-b border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Smartphone size={18} className="text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground">Notificações Push</h3>
                    <p className="text-sm text-muted-foreground">Receba alertas em tempo real no seu dispositivo</p>
                  </div>
                </div>
                <Switch
                  checked={notifications.push}
                  onCheckedChange={(checked) => setNotifications((prev) => ({ ...prev, push: checked }))}
                />
              </div>

              <div className="flex items-center justify-between py-3 border-b border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Bell size={18} className="text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground">Atualizações de Produto</h3>
                    <p className="text-sm text-muted-foreground">Novidades e melhorias da plataforma</p>
                  </div>
                </div>
                <Switch
                  checked={notifications.updates}
                  onCheckedChange={(checked) => setNotifications((prev) => ({ ...prev, updates: checked }))}
                />
              </div>

              <div className="flex items-center justify-between py-3 border-b border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Mail size={18} className="text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground">Emails de Marketing</h3>
                    <p className="text-sm text-muted-foreground">Promoções, ofertas e novidades</p>
                  </div>
                </div>
                <Switch
                  checked={notifications.marketing}
                  onCheckedChange={(checked) => setNotifications((prev) => ({ ...prev, marketing: checked }))}
                />
              </div>

              <div className="flex items-center justify-between py-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Shield size={18} className="text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground">Alertas de Segurança</h3>
                    <p className="text-sm text-muted-foreground">Atividades suspeitas e logins</p>
                  </div>
                </div>
                <Switch
                  checked={notifications.security}
                  onCheckedChange={(checked) => setNotifications((prev) => ({ ...prev, security: checked }))}
                />
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="privacy" className="space-y-6">
          <div className="p-6 rounded-xl bg-card border border-border">
            <h2 className="text-lg font-semibold text-foreground mb-6">Configurações de Privacidade</h2>

            <div className="space-y-6">
              <div className="flex items-center justify-between py-3 border-b border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Globe size={18} className="text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground">Perfil Público</h3>
                    <p className="text-sm text-muted-foreground">Permitir que outros usuários vejam seu perfil</p>
                  </div>
                </div>
                <Switch
                  checked={privacy.profilePublic}
                  onCheckedChange={(checked) => setPrivacy((prev) => ({ ...prev, profilePublic: checked }))}
                />
              </div>

              <div className="flex items-center justify-between py-3 border-b border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Mail size={18} className="text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground">Mostrar Email</h3>
                    <p className="text-sm text-muted-foreground">Exibir email no seu perfil público</p>
                  </div>
                </div>
                <Switch
                  checked={privacy.showEmail}
                  onCheckedChange={(checked) => setPrivacy((prev) => ({ ...prev, showEmail: checked }))}
                />
              </div>

              <div className="flex items-center justify-between py-3 border-b border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Monitor size={18} className="text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground">Status de Atividade</h3>
                    <p className="text-sm text-muted-foreground">Mostrar quando você está online</p>
                  </div>
                </div>
                <Switch
                  checked={privacy.showActivity}
                  onCheckedChange={(checked) => setPrivacy((prev) => ({ ...prev, showActivity: checked }))}
                />
              </div>

              <div className="flex items-center justify-between py-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Key size={18} className="text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-foreground">Autenticação de Dois Fatores</h3>
                    <p className="text-sm text-muted-foreground">Adicione uma camada extra de segurança</p>
                  </div>
                </div>
                <Switch
                  checked={privacy.twoFactor}
                  onCheckedChange={(checked) => setPrivacy((prev) => ({ ...prev, twoFactor: checked }))}
                />
              </div>
            </div>
          </div>

          <div className="p-6 rounded-xl bg-card border border-destructive/30">
            <h2 className="text-lg font-semibold text-destructive mb-2">Zona de Perigo</h2>
            <p className="text-sm text-muted-foreground mb-6">
              Ações irreversíveis que afetam permanentemente sua conta
            </p>
            <div className="flex flex-wrap gap-3">
              <Button
                variant="outline"
                className="border-destructive/50 text-destructive hover:bg-destructive/10 bg-transparent"
              >
                Desativar Conta
              </Button>
              <Button variant="destructive">Excluir Conta</Button>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="appearance" className="space-y-6">
          <div className="p-6 rounded-xl bg-card border border-border">
            <h2 className="text-lg font-semibold text-foreground mb-6">Tema</h2>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <button
                onClick={() => setTheme("light")}
                className={`p-4 rounded-xl border-2 transition-colors ${
                  theme === "light" ? "border-primary bg-primary/5" : "border-border hover:border-ring/50"
                }`}
              >
                <div className="flex flex-col items-center gap-3">
                  <div className="p-3 rounded-full bg-secondary">
                    <Sun size={24} className="text-yellow-500" />
                  </div>
                  <span className="font-medium text-foreground">Claro</span>
                </div>
              </button>

              <button
                onClick={() => setTheme("dark")}
                className={`p-4 rounded-xl border-2 transition-colors ${
                  theme === "dark" ? "border-primary bg-primary/5" : "border-border hover:border-ring/50"
                }`}
              >
                <div className="flex flex-col items-center gap-3">
                  <div className="p-3 rounded-full bg-secondary">
                    <Moon size={24} className="text-blue-400" />
                  </div>
                  <span className="font-medium text-foreground">Escuro</span>
                </div>
              </button>

              <button
                onClick={() => setTheme("system")}
                className={`p-4 rounded-xl border-2 transition-colors ${
                  theme === "system" ? "border-primary bg-primary/5" : "border-border hover:border-ring/50"
                }`}
              >
                <div className="flex flex-col items-center gap-3">
                  <div className="p-3 rounded-full bg-secondary">
                    <Monitor size={24} className="text-muted-foreground" />
                  </div>
                  <span className="font-medium text-foreground">Sistema</span>
                </div>
              </button>
            </div>
          </div>

          <div className="p-6 rounded-xl bg-card border border-border">
            <h2 className="text-lg font-semibold text-foreground mb-6">Idioma e Região</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label>Idioma</Label>
                <Select defaultValue="pt-BR">
                  <SelectTrigger className="bg-secondary border-transparent">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="pt-BR">Português (Brasil)</SelectItem>
                    <SelectItem value="en-US">English (US)</SelectItem>
                    <SelectItem value="es">Español</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Fuso Horário</Label>
                <Select defaultValue="america-sao-paulo">
                  <SelectTrigger className="bg-secondary border-transparent">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="america-sao-paulo">América/São Paulo (GMT-3)</SelectItem>
                    <SelectItem value="america-new-york">América/New York (GMT-5)</SelectItem>
                    <SelectItem value="europe-london">Europa/London (GMT+0)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Formato de Data</Label>
                <Select defaultValue="dd-mm-yyyy">
                  <SelectTrigger className="bg-secondary border-transparent">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="dd-mm-yyyy">DD/MM/AAAA</SelectItem>
                    <SelectItem value="mm-dd-yyyy">MM/DD/AAAA</SelectItem>
                    <SelectItem value="yyyy-mm-dd">AAAA-MM-DD</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Moeda</Label>
                <Select defaultValue="brl">
                  <SelectTrigger className="bg-secondary border-transparent">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="brl">Real (R$)</SelectItem>
                    <SelectItem value="usd">Dollar ($)</SelectItem>
                    <SelectItem value="eur">Euro (€)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
