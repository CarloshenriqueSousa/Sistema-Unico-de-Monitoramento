export interface Achievement {
  id: string;
  title: string;
  description: string;
  points: number;
  date: string;
  icon?: string;
  category?: string;
  awardedBy?: string;
}

export interface Activity {
  id: string;
  title: string;
  subject: string;
  dueDate: string;
  status: 'pending' | 'completed' | 'late' | 'review' | 'draft';
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  progress?: number;
  participants?: Array<{ id: string; name: string; initials: string; avatar?: string }>;
  description?: string;
  attachments?: string[];
  createdAt?: string;
  updatedAt?: string;
  tags?: string[];
}

export interface Question {
  id: string;
  text: string;
  type: 'multiple_choice' | 'true_false' | 'open_ended' | 'matching' | 'fill_in' | 'essay';
  options?: string[];
  correctAnswer?: string | string[];
  points: number;
  explanation?: string;
  media?: string[];
}

export interface Exam {
  id: string;
  title: string;
  subject: string;
  questions: Question[];
  timeLimit: number;
  totalPoints: number;
  difficulty: 'easy' | 'medium' | 'hard' | 'custom';
  createdBy?: string;
  createdAt?: string;
  attemptsAllowed?: number;
  tags?: string[];
}

export interface Note {
  id: string;
  title: string;
  content: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
  subject?: string;
  authorId?: string;
  attachments?: string[];
}