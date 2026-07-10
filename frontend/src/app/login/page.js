"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { login } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user = await login(form.username, form.password);
      router.push(user.role === "manager" ? "/dashboard" : "/reports");
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid username or password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-sm border rounded-xl p-8 w-full max-w-sm space-y-4"
      >
        <h1 className="text-xl font-semibold text-slate-800">Log in</h1>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div>
          <label className="text-sm text-slate-600">Username</label>
          <input
            className="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            required
          />
        </div>
        <div>
          <label className="text-sm text-slate-600">Password</label>
          <input
            type="password"
            className="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />
        </div>
        <button
          disabled={loading}
          className="w-full bg-brand-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-brand-700 disabled:opacity-60"
        >
          {loading ? "Logging in…" : "Log in"}
        </button>
        <p className="text-sm text-slate-500 text-center">
          No account?{" "}
          <Link href="/register" className="text-brand-600 hover:underline">
            Register
          </Link>
        </p>
      </form>
    </div>
  );
}
