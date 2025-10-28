interface BadgeProps {
  children: React.ReactNode
  className?: string
}

export default function Badge({ children, className }: BadgeProps) {
  return (
    <span className={`px-2 py-1 rounded text-xs font-semibold ${className}`}>
      {children}
    </span>
  )
}
