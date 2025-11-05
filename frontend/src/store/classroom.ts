import { defineStore } from 'pinia'
import axios from 'axios'
import type { Student, Group, Classroom } from '@/types/classroom'

export interface ClassroomState {
  students: Student[]
  groups: Group[]
  activeClassroom: Classroom | null
  isLoading: boolean
  error: string | null
  lastUpdated: Date | null
}

export const useClassroomStore = defineStore('classroom', {
  state: (): ClassroomState => ({
    students: [],
    groups: [],
    activeClassroom: null,
    isLoading: false,
    error: null,
    lastUpdated: null
  }),

  getters: {
    studentCount: (state): number => state.students.length,
    
    groupCount: (state): number => state.groups.length,
    
    hasVisionIssues: (state): number => 
      state.students.filter(s => s.hasVisionIssue).length,
    
    studentsWithoutGroup: (state): Student[] => 
      state.students.filter(s => !s.groupId),
    
    groupsWithStudents: (state) => 
      state.groups.map(group => ({
        ...group,
        studentsList: state.students.filter(s => s.groupId === group.id)
      }))
  },

  actions: {
    async loadClassroom(classroomId: number): Promise<boolean> {
      this.isLoading = true
      this.error = null
      
      try {
        const [studentsRes, groupsRes, classroomRes] = await Promise.all([
          axios.get(`/api/classrooms/${classroomId}/students/`),
          axios.get(`/api/classrooms/${classroomId}/groups/`),
          axios.get(`/api/classrooms/${classroomId}/`)
        ])
        
        this.students = studentsRes.data
        this.groups = groupsRes.data
        this.activeClassroom = classroomRes.data
        this.lastUpdated = new Date()
        
        return true
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Falha ao carregar sala de aula'
        console.error('Erro ao carregar sala:', error)
        return false
      } finally {
        this.isLoading = false
      }
    },

    async updateStudentPosition(
      studentId: number, 
      position: { x: number; y: number; z: number }
    ): Promise<boolean> {
      try {
        await axios.patch(`/api/students/${studentId}/position/`, { position })
        
        const index = this.students.findIndex(s => s.id === studentId)
        if (index !== -1) {
          this.students[index].position = position
        }
        
        return true
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Erro ao atualizar posição'
        console.error('Erro ao atualizar posição:', error)
        return false
      }
    },

    async createGroup(groupData: Omit<Group, 'id'>): Promise<Group | null> {
      this.isLoading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/groups/', groupData)
        this.groups.push(response.data)
        this.lastUpdated = new Date()
        return response.data
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Falha ao criar grupo'
        console.error('Erro ao criar grupo:', error)
        return null
      } finally {
        this.isLoading = false
      }
    },

    async updateGroup(groupId: number, groupData: Partial<Group>): Promise<boolean> {
      try {
        const response = await axios.patch(`/api/groups/${groupId}/`, groupData)
        
        const index = this.groups.findIndex(g => g.id === groupId)
        if (index !== -1) {
          this.groups[index] = { ...this.groups[index], ...response.data }
        }
        
        this.lastUpdated = new Date()
        return true
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Erro ao atualizar grupo'
        console.error('Erro ao atualizar grupo:', error)
        return false
      }
    },

    async deleteGroup(groupId: number): Promise<boolean> {
      try {
        await axios.delete(`/api/groups/${groupId}/`)
        
        // Remove alunos do grupo
        this.students = this.students.map(student =>
          student.groupId === groupId ? { ...student, groupId: undefined } : student
        )
        
        // Remove o grupo
        this.groups = this.groups.filter(g => g.id !== groupId)
        
        this.lastUpdated = new Date()
        return true
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Erro ao deletar grupo'
        console.error('Erro ao deletar grupo:', error)
        return false
      }
    },

    async assignStudentToGroup(studentId: number, groupId: number): Promise<boolean> {
      try {
        await axios.post(`/api/groups/${groupId}/assign/`, { studentId })
        
        // Atualiza o aluno
        this.students = this.students.map(student =>
          student.id === studentId ? { ...student, groupId } : student
        )
        
        // Atualiza o grupo
        const groupIndex = this.groups.findIndex(g => g.id === groupId)
        if (groupIndex !== -1 && !this.groups[groupIndex].students.includes(studentId)) {
          this.groups[groupIndex].students.push(studentId)
        }
        
        this.lastUpdated = new Date()
        return true
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Erro ao atribuir aluno'
        console.error('Erro ao atribuir aluno:', error)
        return false
      }
    },

    async removeStudentFromGroup(studentId: number): Promise<boolean> {
      try {
        const student = this.students.find(s => s.id === studentId)
        if (!student?.groupId) return false

        await axios.post(`/api/groups/${student.groupId}/remove/`, { studentId })
        
        // Remove do array de estudantes do grupo
        const groupIndex = this.groups.findIndex(g => g.id === student.groupId)
        if (groupIndex !== -1) {
          this.groups[groupIndex].students = this.groups[groupIndex].students.filter(
            id => id !== studentId
          )
        }
        
        // Remove groupId do estudante
        this.students = this.students.map(s =>
          s.id === studentId ? { ...s, groupId: undefined } : s
        )
        
        this.lastUpdated = new Date()
        return true
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Erro ao remover aluno do grupo'
        console.error('Erro ao remover aluno do grupo:', error)
        return false
      }
    },

    async saveClassroomLayout(): Promise<boolean> {
      if (!this.activeClassroom) return false
      
      this.isLoading = true
      this.error = null
      
      try {
        await axios.post(`/api/classrooms/${this.activeClassroom.id}/save-layout/`, {
          students: this.students.map(s => ({ id: s.id, position: s.position })),
          groups: this.groups
        })
        
        this.lastUpdated = new Date()
        return true
      } catch (error: any) {
        this.error = error.response?.data?.message || 'Falha ao salvar layout'
        console.error('Erro ao salvar layout:', error)
        return false
      } finally {
        this.isLoading = false
      }
    },

    clearError(): void {
      this.error = null
    },

    resetClassroom(): void {
      this.students = []
      this.groups = []
      this.activeClassroom = null
      this.error = null
      this.lastUpdated = null
    }
  }
})