"use client"

import { useState, useEffect } from "react"
import { AlertCircle, TrendingUp, Zap, AlertTriangle } from "lucide-react"
import RFIDStatusPanel from "@/components/rfid-status-panel"
import TransactionLog from "@/components/transaction-log"
import TopUpForm from "@/components/topup-form"
import FloodControlPanel from "@/components/flood-control-panel"

export default function Dashboard() {
  const [emergencyStatus, setEmergencyStatus] = useState<"ACTIVE" | "INACTIVE">("INACTIVE")
  // HARDCODED: Initial water level - Replace with Firebase real-time listener
  const [waterLevel, setWaterLevel] = useState(45)
  // HARDCODED: Simulated loading state - Remove when integrating with real backend
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // HARDCODED: Simulated loading delay - Remove when integrating with real backend
    const timer = setTimeout(() => setIsLoading(false), 1000)
    return () => clearTimeout(timer)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-300">Loading Expressway Dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg flex items-center justify-center">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Expressway Toll System</h1>
                <p className="text-sm text-slate-400">Real-time Monitoring & Control</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-slate-400">System Status</p>
              <p className="text-lg font-semibold text-green-400">● Online</p>
            </div>
          </div>
        </div>
      </header>

      {/* Emergency Alert */}
      {emergencyStatus === "ACTIVE" && (
        <div className="bg-red-900/20 border-b border-red-500/30 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-3">
            <AlertTriangle className="w-6 h-6 text-red-500 flex-shrink-0" />
            <div>
              <p className="font-semibold text-red-400">🚨 EMERGENCY OVERRIDE ACTIVE</p>
              <p className="text-sm text-red-300">
                All toll barriers are open due to critical flood warning. Vehicles are passing through without toll
                deduction.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* RFID Status Panel */}
          <div className="lg:col-span-2">
            <RFIDStatusPanel />
          </div>

          {/* Flood Control Panel */}
          <div>
            <FloodControlPanel waterLevel={waterLevel} onEmergencyChange={setEmergencyStatus} />
          </div>
        </div>

        {/* Top-Up Form and Transaction Log */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Top-Up Form */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 backdrop-blur-sm">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-orange-500" />
              Balance Top-Up
            </h2>
            <TopUpForm />
          </div>

          {/* Transaction Log */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 backdrop-blur-sm">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-orange-500" />
              Recent Transactions
            </h2>
            <TransactionLog />
          </div>
        </div>
      </main>
    </div>
  )
}
