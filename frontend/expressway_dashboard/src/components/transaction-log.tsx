"use client"

import { useState } from "react"
import { ArrowRight, Clock } from "lucide-react"

interface Transaction {
  id: string
  rfidName: string
  carType: string
  timeIn: string
  timeOut: string
  tollFee: number
  status: "COMPLETED" | "IN_PROGRESS" | "DENIED"
}

export default function TransactionLog() {
  // HARDCODED: Mock transaction data - Replace with Firebase real-time listener
  // TODO: Connect to Firebase to fetch actual transactions from /transactions node
  const [transactions, setTransactions] = useState<Transaction[]>([
    {
      id: "1",
      rfidName: "John Doe",
      carType: "PRIVATE",
      timeIn: "14:32",
      timeOut: "14:47",
      tollFee: 8.5,
      status: "COMPLETED",
    },
    {
      id: "2",
      rfidName: "Bus Line 1",
      carType: "PUBLIC",
      timeIn: "14:28",
      timeOut: "14:43",
      tollFee: 5.0,
      status: "COMPLETED",
    },
    {
      id: "3",
      rfidName: "Ambulance 911",
      carType: "EMERGENCY",
      timeIn: "14:25",
      timeOut: "14:31",
      tollFee: 0.0,
      status: "COMPLETED",
    },
    {
      id: "4",
      rfidName: "John Doe",
      carType: "PRIVATE",
      timeIn: "14:15",
      timeOut: "-",
      tollFee: 0.0,
      status: "IN_PROGRESS",
    },
  ])

  const getStatusColor = (status: string) => {
    switch (status) {
      case "COMPLETED":
        return "bg-green-500/20 text-green-300"
      case "IN_PROGRESS":
        return "bg-blue-500/20 text-blue-300"
      case "DENIED":
        return "bg-red-500/20 text-red-300"
      default:
        return "bg-slate-500/20 text-slate-300"
    }
  }

  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      {transactions.length === 0 ? (
        <p className="text-slate-400 text-center py-8">No transactions yet</p>
      ) : (
        transactions.map((tx) => (
          <div
            key={tx.id}
            className="bg-slate-700/30 border border-slate-600 rounded-lg p-3 hover:border-orange-500/30 transition-colors"
          >
            <div className="flex items-center justify-between mb-2">
              <p className="font-semibold text-white text-sm">{tx.rfidName}</p>
              <span className={`text-xs px-2 py-1 rounded ${getStatusColor(tx.status)}`}>{tx.status}</span>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-400">
              <div className="flex items-center gap-2">
                <Clock className="w-3 h-3" />
                <span>{tx.timeIn}</span>
              </div>
              <ArrowRight className="w-3 h-3" />
              <span>{tx.timeOut}</span>
              <span className="text-green-400 font-semibold">${tx.tollFee.toFixed(2)}</span>
            </div>
          </div>
        ))
      )}
    </div>
  )
}