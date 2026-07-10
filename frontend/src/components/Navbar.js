"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { getCurrentUser, logout } from "@/lib/auth";

export default function Navbar() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(getCurrentUser());
  }, []);

  return (
    <nav className="w-full border-b bg-white px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-6">
        <span className="font-semibold text-brand-700">Weekly Reports</span>
        {user && (
          <>
            <Link href="/reports" className="text-sm text-slate-600 hover:text-brand-600">
              My Reports
            </Link>
            {user.role === "manager" && (
              <>
                <Link href="/dashboard" className="text-sm text-slate-600 hover:text-brand-600">
                  Team Dashboard
                </Link>
                <Link href="/projects" className="text-sm text-slate-600 hover:text-brand-600">
                  Projects
                </Link>
              </>
            )}
          </>
        )}
      </div>
      <div className="flex items-center gap-4">
        {user ? (
          <>
            <span className="text-sm text-slate-500">
              {user.username} <span className="text-xs text-slate-400">({user.role})</span>
            </span>
            <button
              onClick={logout}
              className="text-sm text-red-600 hover:underline"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link href="/login" className="text-sm text-slate-600 hover:text-brand-600">
              Login
            </Link>
            <Link href="/register" className="text-sm text-slate-600 hover:text-brand-600">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
