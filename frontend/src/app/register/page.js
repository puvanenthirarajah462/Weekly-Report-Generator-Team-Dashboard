"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { register } from "@/lib/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function update(field) {
    return (e) => setForm((prev) => ({ ...prev, [field]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const payload = {
        username: form.username.trim(),
        email: form.email.trim(),
        password: form.password,
        first_name: form.first_name.trim(),
        last_name: form.last_name.trim(),
      };
      await register(payload);
      router.replace("/login");
    } catch (err) {
      const data = err.response?.data;
      const message = data
        ? Object.entries(data)
            .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(" ") : value}`)
            .join(" ")
        : "Registration failed.";
      setError(message);
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
        <h1 className="text-xl font-semibold text-slate-800">Create account</h1>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-sm text-slate-600">First name</label>
            <input className="mt-1 w-full border rounded-lg px-3 py-2 text-sm" value={form.first_name} onChange={update("first_name")} />
          </div>
          <div>
            <label className="text-sm text-slate-600">Last name</label>
            <input className="mt-1 w-full border rounded-lg px-3 py-2 text-sm" value={form.last_name} onChange={update("last_name")} />
          </div>
        </div>
        <div>
          <label className="text-sm text-slate-600">Username</label>
          <input className="mt-1 w-full border rounded-lg px-3 py-2 text-sm" value={form.username} onChange={update("username")} required />
        </div>
        <div>
          <label className="text-sm text-slate-600">Email</label>
          <input type="email" className="mt-1 w-full border rounded-lg px-3 py-2 text-sm" value={form.email} onChange={update("email")} required />
        </div>
        <div>
          <label className="text-sm text-slate-600">Password</label>
          <input type="password" className="mt-1 w-full border rounded-lg px-3 py-2 text-sm" value={form.password} onChange={update("password")} required />
        </div>
        <button
          disabled={loading}
          className="w-full bg-brand-600 text-white rounded-lg py-2 text-sm font-medium hover:bg-brand-700 disabled:opacity-60"
        >
          {loading ? "Creating account…" : "Register"}
        </button>
        <p className="text-sm text-slate-500 text-center">
          Already have an account?{" "}
          <Link href="/login" className="text-brand-600 hover:underline">
            Log in
          </Link>
        </p>
      </form>
    </div>
  );
}
