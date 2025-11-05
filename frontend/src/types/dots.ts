export interface DotsProfile {
  id: number
  studentId: number
  achievements: {
    academic: AcademicAchievement[]
    sports: SportsAchievement[]
    arts: ArtsAchievement[]
    community: CommunityAchievement[]
    social?: SocialAchievement[]      // ADICIONADO
    technical?: TechnicalAchievement[] // ADICIONADO
  }
  skills: Skill[]
  badges: Badge[]
  portfolio: PortfolioItem[]
  visibilitySettings: {
    public: boolean
    shareToken?: string
    allowedViewers: number[]
  }
}

export interface Skill {
  name: string
  level: number
  verified: boolean
  category?: string
}

export interface Badge {
  id: string
  name: string
  description: string
  icon: string
  awardedAt: string
}

export interface PortfolioItem {
  id: string
  title: string
  description: string
  url?: string
  media?: string[]
  createdAt: string
}

// Conquistas existentes
export interface AcademicAchievement {
  id?: number
  subject: string
  title: string
  description: string
  date: Date
  proof?: string
  verifiedBy?: number
  awardedAt?: Date
}

export interface SportsAchievement {
  id?: number
  sport: string
  achievement: string
  season: string
  stats: Record<string, number>
  media?: string[]
  awardedAt?: Date
}

export interface ArtsAchievement {
  id?: number
  title: string
  type: string
  description: string
  date: Date
  media?: string[]
  awardedAt?: Date
}

export interface CommunityAchievement {
  id?: number
  title: string
  organization: string
  description: string
  date: Date
  proof?: string
  awardedAt?: Date
}

// Conquistas adicionadas
export interface SocialAchievement {
  id?: number
  title: string
  description: string
  category: 'teamwork' | 'leadership' | 'communication' | 'empathy'
  date: Date
  proof?: string
  awardedAt?: Date
}

export interface TechnicalAchievement {
  id?: number
  title: string
  description: string
  technology: string
  projectUrl?: string
  date: Date
  awardedAt?: Date
}

// Tipo genérico para Achievement (usado no composable)
export type Achievement = 
  | AcademicAchievement 
  | SportsAchievement 
  | ArtsAchievement 
  | CommunityAchievement
  | SocialAchievement
  | TechnicalAchievement

// Helper type para criar achievements sem ID e data
export type CreateAchievementData = Omit<Achievement, 'id' | 'awardedAt'>

// Tipos para análise e relatórios
export interface DotsAnalysis {
  studentId: number
  overallScore: number
  strengths: string[]
  weaknesses: string[]
  recommendations: string[]
  comparisonWithClass: {
    rank: number
    percentile: number
  }
  generatedAt: Date
}

export interface DotsLeaderboardEntry {
  studentId: number
  studentName: string
  overallScore: number
  topSkills: Skill[]
  totalAchievements: number
  rank: number
}