import { LoginForm } from "@/components/login-form"

export default function LoginPage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md">
        <div className="p-8 rounded-2xl bg-card border border-border shadow-2xl shadow-black/20">
          <LoginForm />
        </div>
      </div>
    </main>
  )
}
