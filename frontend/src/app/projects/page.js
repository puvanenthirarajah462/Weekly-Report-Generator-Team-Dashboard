"use client";
import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import api from "@/lib/api";

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({ name: "", description: "" });
  const [error, setError] = useState("");

  async function load() {
    const { data } = await api.get("/projects/");
    setProjects(data);
  }

  useEffect(() => {
    load();
  }, []);

  async function createProject(e) {
    e.preventDefault();
    setError("");
    try {
      await api.post("/projects/", form);
      setForm({ name: "", description: "" });
      load();
    } catch (err) {
      setError(err.response?.data?.name?.[0] || "Failed to create project.");
    }
  }

  async function toggleActive(p) {
    await api.patch(`/projects/${p.id}/`, { is_active: !p.is_active });
    load();
  }

  async function remove(p) {
    if (!confirm(`Delete project "${p.name}"?`)) return;
    await api.delete(`/projects/${p.id}/`);
    load();
  }

  return (
    <div>
      <Navbar />
      <main className="max-w-4xl mx-auto p-6 space-y-6">
        <section className="bg-white border rounded-xl p-6">
          <h2 className="font-semibold text-slate-800 mb-4">Add project / category</h2>
          {error && <p className="text-sm text-red-600 mb-2">{error}</p>}
          <form onSubmit={createProject} className="flex gap-3">
            <input
              placeholder="Name (e.g. Client A)"
              className="flex-1 border rounded-lg px-3 py-2 text-sm"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
            <input
              placeholder="Description (optional)"
              className="flex-1 border rounded-lg px-3 py-2 text-sm"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
            />
            <button className="px-4 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700">
              Add
            </button>
          </form>
        </section>

        <section className="bg-white border rounded-xl divide-y">
          {projects.map((p) => (
            <div key={p.id} className="flex items-center justify-between px-6 py-4">
              <div>
                <p className="font-medium text-slate-800">{p.name}</p>
                <p className="text-xs text-slate-500">{p.description}</p>
              </div>
              <div className="flex items-center gap-3">
                <span
                  className={`text-xs px-2 py-1 rounded-full ${
                    p.is_active ? "bg-green-100 text-green-700" : "bg-slate-100 text-slate-500"
                  }`}
                >
                  {p.is_active ? "Active" : "Inactive"}
                </span>
                <button onClick={() => toggleActive(p)} className="text-xs text-brand-600 hover:underline">
                  Toggle
                </button>
                <button onClick={() => remove(p)} className="text-xs text-red-600 hover:underline">
                  Delete
                </button>
              </div>
            </div>
          ))}
          {projects.length === 0 && (
            <p className="text-sm text-slate-500 px-6 py-4">No projects yet.</p>
          )}
        </section>
      </main>
    </div>
  );
}
