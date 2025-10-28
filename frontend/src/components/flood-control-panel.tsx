"use client"

import { useState } from "react"
import { Droplets } from "lucide-react"
import { Button } from "@/components/ui/button"

interface FloodControlPanelProps {
  waterLevel?: number // optional, might be undefined while fetching
  onEmergencyChange: (status: "ACTIVE" | "INACTIVE") => void
}

export default function FloodControlPanel({
  waterLevel,
  onEmergencyChange,
}: FloodControlPanelProps) {
  const [isEmergency, setIsEmergency] = useState(false)

  // Clamp waterLevel between 0 and 100 to prevent progress overflow
  const safeWaterLevel = Math.min(Math.max(waterLevel ?? 0, 0), 100)

  // Status text color
  const getStatusColor = () => {
    if (safeWaterLevel > 80) return "text-red-500"
    if (safeWaterLevel > 60) return "text-yellow-500"
    return "text-green-500"
  }

  // Progress bar color
  const getProgressColor = () => {
    if (safeWaterLevel > 80) return "bg-red-500"
    if (safeWaterLevel > 60) return "bg-yellow-500"
    return "bg-green-500"
  }

  return (
    <div
      className={`border rounded-lg p-6 backdrop-blur-sm transition-colors ${
        isEmergency ? "bg-red-900/20 border-red-500/50" : "bg-slate-800/50 border-slate-700"
      }`}
    >
      <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
        <Droplets className="w-5 h-5" />
        Flood Control
      </h2>

      <div className="space-y-6">
        {/* Water Level Display */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-slate-300">Water Level</p>
            {waterLevel === undefined ? (
              <p className="text-2xl font-bold text-slate-400">Loading...</p>
            ) : (
              <p className={`text-2xl font-bold ${getStatusColor()}`}>
                {safeWaterLevel.toFixed(1)}%
              </p>
            )}
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
            <div
              className={`h-full ${getProgressColor()} transition-all duration-500`}
              style={{ width: `${safeWaterLevel}%` }}
            />
          </div>
        </div>

        {/* Status Indicator */}
        <div className="bg-slate-700/50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <div
              className={`w-3 h-3 rounded-full ${
                isEmergency ? "bg-red-500 animate-pulse" : "bg-green-500"
              }`}
            />
            <p className="text-sm font-semibold text-white">
              {isEmergency ? "EMERGENCY MODE" : "Normal Operation"}
            </p>
          </div>
          <p className="text-xs text-slate-400">
            {isEmergency
              ? "All toll barriers are open for emergency evacuation"
              : "System operating normally"}
          </p>
        </div>

        {/* Alert Thresholds */}
        <div className="space-y-2 text-xs">
          <div className="flex justify-between text-slate-400">
            <span>Safe Zone</span>
            <span>0-60%</span>
          </div>
          <div className="flex justify-between text-yellow-400">
            <span>Warning Zone</span>
            <span>60-80%</span>
          </div>
          <div className="flex justify-between text-red-400">
            <span>Critical Zone</span>
            <span>80-100%</span>
          </div>
        </div>

        {/* Manual Emergency Override Button */}
        {isEmergency && (
          <Button
            onClick={() => {
              setIsEmergency(false)
              onEmergencyChange("INACTIVE")
            }}
            className="w-full bg-red-600 hover:bg-red-700 text-white"
          >
            Clear Emergency Override
          </Button>
        )}
      </div>
    </div>
  )
}
