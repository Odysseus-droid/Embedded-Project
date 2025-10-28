"use client"

import { useState, useEffect } from "react"
import { Droplets } from "lucide-react"
import { Button } from "@/components/ui/button"

interface FloodControlPanelProps {
  waterLevel: number
  onEmergencyChange: (status: "ACTIVE" | "INACTIVE") => void
}

function FloodControlPanel({ waterLevel, onEmergencyChange }: FloodControlPanelProps) {
  const [level, setLevel] = useState(waterLevel)
  const [isEmergency, setIsEmergency] = useState(false)

  useEffect(() => {
    // HARDCODED: Simulated water level changes - Replace with Firebase real-time listener
    // TODO: Connect to Firebase to fetch actual flood sensor data from /flood_sensor node
    const interval = setInterval(() => {
      setLevel((prev) => {
        const change = (Math.random() - 0.5) * 10
        const newLevel = Math.max(0, Math.min(100, prev + change))

        // HARDCODED: Emergency threshold at 80% - Verify this matches your system requirements
        if (newLevel > 80 && !isEmergency) {
          setIsEmergency(true)
          onEmergencyChange("ACTIVE")
        } else if (newLevel < 60 && isEmergency) {
          setIsEmergency(false)
          onEmergencyChange("INACTIVE")
        }

        return newLevel
      })
    }, 3000)

    return () => clearInterval(interval)
  }, [isEmergency, onEmergencyChange])

  const getStatusColor = () => {
    if (level > 80) return "text-red-500"
    if (level > 60) return "text-yellow-500"
    return "text-green-500"
  }

  const getProgressColor = () => {
    if (level > 80) return "bg-red-500"
    if (level > 60) return "bg-yellow-500"
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
            <p className={`text-2xl font-bold ${getStatusColor()}`}>{level.toFixed(1)}%</p>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
            <div
              className={`h-full ${getProgressColor()} transition-all duration-500`}
              style={{ width: `${level}%` }}
            />
          </div>
        </div>

        {/* Status Indicator */}
        <div className="bg-slate-700/50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <div className={`w-3 h-3 rounded-full ${isEmergency ? "bg-red-500 animate-pulse" : "bg-green-500"}`} />
            <p className="text-sm font-semibold text-white">{isEmergency ? "EMERGENCY MODE" : "Normal Operation"}</p>
          </div>
          <p className="text-xs text-slate-400">
            {isEmergency ? "All toll barriers are open for emergency evacuation" : "System operating normally"}
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

        {/* Manual Override Button */}
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

export default FloodControlPanel;
