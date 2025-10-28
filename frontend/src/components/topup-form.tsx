"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { AlertCircle, CheckCircle } from "lucide-react"

export default function TopUpForm() {
  const [rfidId, setRfidId] = useState("")
  const [amount, setAmount] = useState("")
  const [message, setMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!rfidId || !amount) {
      setMessage("Please fill in all fields")
      setIsSuccess(false)
      return
    }

    setIsLoading(true)
    setMessage("")

    try {
      // HARDCODED: Django API endpoint - Update with your actual backend URL
      // TODO: Replace "http://localhost:8000" with your production Django server URL
      const response = await fetch("http://localhost:8000/api/rfids/topup/", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          rfid_id: rfidId,
          amount: Number.parseFloat(amount),
        }),
      })

      if (response.ok) {
        setMessage(`✓ Successfully added $${amount} to RFID ${rfidId}`)
        setIsSuccess(true)
        setRfidId("")
        setAmount("")
        setTimeout(() => {
          setMessage("")
          setIsSuccess(false)
        }, 3000)
      } else {
        const error = await response.json()
        setMessage(`Error: ${error.error || "Failed to process top-up"}`)
        setIsSuccess(false)
      }
    } catch (error) {
      setMessage("Error: Unable to connect to backend. Make sure Django server is running.")
      setIsSuccess(false)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-slate-300 mb-2">RFID Tag ID</label>
        <Input
          type="text"
          placeholder="e.g., E3FE5D3171"
          value={rfidId}
          onChange={(e) => setRfidId(e.target.value)}
          className="bg-slate-700 border-slate-600 text-white placeholder-slate-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-300 mb-2">Amount ($)</label>
        <Input
          type="number"
          placeholder="50.00"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          min="1"
          step="0.01"
          className="bg-slate-700 border-slate-600 text-white placeholder-slate-500"
        />
      </div>

      <Button
        type="submit"
        disabled={isLoading}
        className="w-full bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-semibold"
      >
        {isLoading ? "Processing..." : "Top Up Balance"}
      </Button>

      {message && (
        <div
          className={`flex items-center gap-2 p-3 rounded-lg text-sm ${
            isSuccess
              ? "bg-green-500/20 text-green-300 border border-green-500/30"
              : "bg-red-500/20 text-red-300 border border-red-500/30"
          }`}
        >
          {isSuccess ? (
            <CheckCircle className="w-4 h-4 flex-shrink-0" />
          ) : (
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
          )}
          {message}
        </div>
      )}
    </form>
  )
}