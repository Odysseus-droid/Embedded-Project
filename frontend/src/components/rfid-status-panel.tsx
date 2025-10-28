"use client"

import { useState, useEffect } from "react"
import  Badge  from "@/components/ui/badge"
import { Wallet, AlertCircle, Shield } from "lucide-react"

interface RFID {
  id: string
  name: string
  balance: number
  carType: "PRIVATE" | "PUBLIC" | "EMERGENCY"
  status: "AT_ENTRANCE" | "ON_EXPRESSWAY" | "AT_EXIT" | "OFFLINE"
  lastTransaction?: string
  entryTime?: string
}

export default function RFIDStatusPanel() {
  const [rfids, setRfids] = useState<RFID[]>([])

    useEffect(() => {
    async function fetchRFIDs() {
      try {
        const res = await fetch("http://localhost:8000/api/rfid-accounts/all_accounts/")
        const data = await res.json()

        // Map backend data to your frontend RFID type
        const mappedData: RFID[] = data.map((r: any) => ({
          id: r.rfid_uid,
          name: r.name,
          balance: r.balance,
          carType: r.vehicle_type.toUpperCase(), // ensure it matches "PRIVATE" | "PUBLIC" | "EMERGENCY"
          status: "OFFLINE", // default until you update location dynamically
          lastTransaction: r.last_transaction, // optional
          entryTime: r.entry_time // optional
        }))

        setRfids(mappedData)
      } catch (err) {
        console.error("Failed to fetch RFIDs:", err)
      }
    }

    fetchRFIDs()
  }, [])
  
  const getCarTypeColor = (type: string) => {
    switch (type) {
      case "PRIVATE":
        return "bg-blue-500/20 text-blue-300 border-blue-500/30"
      case "PUBLIC":
        return "bg-purple-500/20 text-purple-300 border-purple-500/30"
      case "EMERGENCY":
        return "bg-red-500/20 text-red-300 border-red-500/30"
      default:
        return "bg-slate-500/20 text-slate-300 border-slate-500/30"
    }
  }

  const getCarIcon = (type: string) => {
    switch (type) {
      case "EMERGENCY":
        return "🚑"
      case "PUBLIC":
        return "🚌"
      default:
        return "🚗"
    }
  }

  const getStatusInfo = (status: string) => {
    switch (status) {
      case "AT_ENTRANCE":
        return {
          color: "text-yellow-400",
          bgColor: "bg-yellow-500/20",
          label: "At Entrance Gate",
          icon: "🚪",
        }
      case "ON_EXPRESSWAY":
        return {
          color: "text-green-400",
          bgColor: "bg-green-500/20",
          label: "Inside Expressway",
          icon: "🛣️",
        }
      case "AT_EXIT":
        return {
          color: "text-blue-400",
          bgColor: "bg-blue-500/20",
          label: "At Exit Gate",
          icon: "🚪",
        }
      case "OFFLINE":
        return {
          color: "text-slate-400",
          bgColor: "bg-slate-500/20",
          label: "Exited",
          icon: "✓",
        }
      default:
        return {
          color: "text-slate-400",
          bgColor: "bg-slate-500/20",
          label: "Unknown",
          icon: "❓",
        }
    }
  }

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 backdrop-blur-sm">
      <h2 className="text-xl font-bold text-white mb-6">RFID Status</h2>

      <div className="space-y-4">
        {rfids.length === 0 ? (
          <p className="text-slate-400 text-center py-8">Waiting for RFID data from Firebase...</p>
        ) : (
          rfids.map((rfid) => {
            const statusInfo = getStatusInfo(rfid.status)
            const isEmergency = rfid.carType === "EMERGENCY"

            return (
              <div
                key={rfid.id}
                className="bg-slate-700/30 border border-slate-600 rounded-lg p-4 hover:border-orange-500/50 transition-colors"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="text-3xl">{getCarIcon(rfid.carType)}</div>
                    <div>
                      <h3 className="font-semibold text-white">{rfid.name}</h3>
                      <p className="text-xs text-slate-400">ID: {rfid.id}</p>
                    </div>
                  </div>
                  <Badge className={`${getCarTypeColor(rfid.carType)} border`}>{rfid.carType}</Badge>
                </div>

                <div className="grid grid-cols-3 gap-4 mb-3">
                  <div className="bg-slate-800/50 rounded p-3">
                    <p className="text-xs text-slate-400 mb-1">Balance</p>
                    {isEmergency ? (
                      <p className="text-sm font-bold text-red-400 flex items-center gap-1">
                        <Shield className="w-4 h-4" />
                        Priority Pass
                      </p>
                    ) : (
                      <p className="text-lg font-bold text-green-400 flex items-center gap-1">
                        <Wallet className="w-4 h-4" />${(rfid.balance ?? 0).toFixed(2)}
                      </p>

                    )}
                  </div>
                  <div className="bg-slate-800/50 rounded p-3">
                    <p className="text-xs text-slate-400 mb-1">Status</p>
                    <p className="text-sm font-semibold text-green-400">● {rfid.status}</p>
                  </div>
                  <div className="bg-slate-800/50 rounded p-3">
                    <p className="text-xs text-slate-400 mb-1">Last Tap</p>
                    <p className="text-sm font-semibold text-slate-300">{rfid.lastTransaction || "-"}</p>
                  </div>
                </div>

                <div className={`${statusInfo.bgColor} rounded p-3 mb-3 border border-slate-600`}>
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{statusInfo.icon}</span>
                    <div>
                      <p className="text-xs text-slate-400">Current Location</p>
                      <p className={`text-sm font-semibold ${statusInfo.color}`}>{statusInfo.label}</p>
                    </div>
                    {rfid.status !== "OFFLINE" && rfid.entryTime && (
                      <div className="ml-auto text-right">
                        <p className="text-xs text-slate-400">Entry Time</p>
                        <p className="text-sm font-semibold text-slate-300">{rfid.entryTime}</p>
                      </div>
                    )}
                  </div>
                </div>

                {!isEmergency && rfid.balance < 20 && (
                  <div className="flex items-center gap-2 text-yellow-400 text-sm">
                    <AlertCircle className="w-4 h-4" />
                    Low balance warning
                  </div>
                )}

                {isEmergency && (
                  <div className="flex items-center gap-2 text-red-400 text-sm">
                    <Shield className="w-4 h-4" />
                    Emergency vehicle - Always has priority access
                  </div>
                )}
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}
