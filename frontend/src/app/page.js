"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getCurrentUser, isAuthenticated } from "@/lib/auth";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const user = getCurrentUser();
    const authenticated = isAuthenticated();

    if (!authenticated || !user) {
      router.replace("/login");
    } else if (user.role === "manager") {
      router.replace("/dashboard");
    } else {
      router.replace("/reports");
    }
  }, [router]);

  return <p className="p-8 text-slate-500">Redirecting…</p>;
}
