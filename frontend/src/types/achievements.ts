// Interface para um selo (badge)
export interface AchievementBadge {
  id: string
  name: string
  color?: string
  icon?: string
}

// Interface para uma conquista (achievement)
export interface Achievement {
  id: string
  title: string
  description: string
  points: number
  date: string
  proof?: string
  verifiedBy?: string
  awardedAt?: string
  icon?: string
  badges?: AchievementBadge[] // <- array de badges, não string
}
