import { ref, computed } from 'vue'
import { useClassroomStore } from '@/store/classroom'
import { useAI } from './useAI'
import type { Student, Group } from '@/types/classroom'

export const useClassroom = () => {
  const store = useClassroomStore()
  const { ask } = useAI()
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed properties
  const students = computed(() => store.students)
  const groups = computed(() => store.groups)
  const activeClassroom = computed(() => store.activeClassroom)
  const studentsWithoutGroup = computed(() => store.studentsWithoutGroup)
  const groupsWithStudents = computed(() => store.groupsWithStudents)
  const studentCount = computed(() => store.studentCount)
  const groupCount = computed(() => store.groupCount)
  const hasVisionIssues = computed(() => store.hasVisionIssues)

  // Load classroom data
  const loadClassroom = async (classroomId: number): Promise<boolean> => {
    isLoading.value = true
    error.value = null
    
    try {
      const success = await store.loadClassroom(classroomId)
      if (!success && store.error) {
        error.value = store.error
      }
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao carregar sala de aula'
      console.error('Erro ao carregar sala:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Optimize student placement using AI
  const optimizePlacement = async (): Promise<boolean> => {
    if (students.value.length === 0) {
      error.value = 'Nenhum aluno carregado'
      return false
    }

    isLoading.value = true
    error.value = null
    
    try {
      const studentData = students.value.map(s => ({
        id: s.id,
        name: s.name,
        hasVisionIssue: s.hasVisionIssue,
        difficultyLearning: s.difficultyLearning,
        learningStyle: s.learningStyle,
        grades: s.grades,
        strengths: s.strengths
      }))

      const prompt = `Com base nos seguintes alunos:
${JSON.stringify(studentData, null, 2)}

Gere um posicionamento otimizado 3D considerando:
1. Alunos com problemas de visão (hasVisionIssue) nas primeiras fileiras (y próximo de 0)
2. Distribuir diferentes estilos de aprendizagem (visual, auditory, kinesthetic)
3. Equilibrar notas e habilidades complementares
4. Considerar dificuldades de aprendizagem para melhor suporte

Retorne APENAS um JSON válido (sem markdown) com array de objetos:
[{ "studentId": number, "position": { "x": number, "y": number, "z": number } }]

Coordenadas: x (lateral -5 a 5), y (frente 0 a 5), z (altura, usar 0)`

      const response = await ask(prompt)
      
      if (!response) {
        throw new Error('Resposta vazia da IA')
      }

      // Remove markdown se existir
      const cleanResponse = response.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim()
      const positions = JSON.parse(cleanResponse)
      
      if (!Array.isArray(positions)) {
        throw new Error('Resposta da IA não é um array')
      }

      // Atualiza as posições de cada aluno
      const updatePromises = positions.map(({ studentId, position }) => {
        if (!position || typeof position.x !== 'number' || typeof position.y !== 'number') {
          console.warn(`Posição inválida para aluno ${studentId}`)
          return Promise.resolve(false)
        }
        return store.updateStudentPosition(studentId, {
          x: position.x,
          y: position.y,
          z: position.z || 0
        })
      })

      const results = await Promise.all(updatePromises)
      const successCount = results.filter(r => r).length
      
      if (successCount === 0) {
        throw new Error('Nenhuma posição foi atualizada')
      }

      console.log(`${successCount}/${positions.length} posições atualizadas`)
      return true

    } catch (err: any) {
      const errorMessage = err.message || 'Erro desconhecido'
      error.value = `Erro na otimização: ${errorMessage}`
      console.error('Erro ao otimizar posicionamento:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Create groups based on activity type using AI
  const createGroups = async (
    activityType: string, 
    groupSize: number = 4
  ): Promise<boolean> => {
    if (students.value.length === 0) {
      error.value = 'Nenhum aluno carregado'
      return false
    }

    if (students.value.length < groupSize) {
      error.value = `Número de alunos insuficiente para formar grupos de ${groupSize}`
      return false
    }

    isLoading.value = true
    error.value = null
    
    try {
      const studentData = students.value.map(s => ({
        id: s.id,
        name: s.name,
        learningStyle: s.learningStyle,
        grades: s.grades,
        strengths: s.strengths,
        hasVisionIssue: s.hasVisionIssue,
        difficultyLearning: s.difficultyLearning
      }))

      const prompt = `Com base nos alunos:
${JSON.stringify(studentData, null, 2)}

Crie grupos equilibrados para uma atividade de "${activityType}".
Cada grupo deve ter aproximadamente ${groupSize} alunos.

Considere:
1. Misturar diferentes estilos de aprendizagem
2. Equilibrar habilidades e notas entre grupos
3. Incluir alunos com dificuldades com alunos que podem ajudar
4. Distribuir forças complementares

Retorne APENAS um JSON válido (sem markdown) com array:
[{ "groupName": string, "studentIds": number[], "focus": string, "color": string }]

Cores sugeridas: "#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"`

      const response = await ask(prompt)
      
      if (!response) {
        throw new Error('Resposta vazia da IA')
      }

      // Remove markdown se existir
      const cleanResponse = response.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim()
      const groupsData = JSON.parse(cleanResponse)
      
      if (!Array.isArray(groupsData) || groupsData.length === 0) {
        throw new Error('Resposta da IA não contém grupos válidos')
      }

      // Valida que todos os alunos foram incluídos
      const allStudentIds = new Set(students.value.map(s => s.id))
      const assignedStudentIds = new Set<number>()
      
      groupsData.forEach(g => {
        g.studentIds?.forEach((id: number) => assignedStudentIds.add(id))
      })

      if (assignedStudentIds.size < allStudentIds.size) {
        console.warn('Nem todos os alunos foram atribuídos a grupos')
      }

      // Cria cada grupo
      const groupPromises = groupsData.map(async (groupData: any) => {
        const createdGroup = await store.createGroup({
          name: groupData.groupName || 'Grupo sem nome',
          students: [],
          focus: groupData.focus || '',
          color: groupData.color || '#3B82F6',
          createdAt: new Date()
        })

        if (!createdGroup) {
          console.error('Falha ao criar grupo:', groupData.groupName)
          return null
        }

        // Atribui os alunos ao grupo criado
        const assignPromises = (groupData.studentIds || []).map((studentId: number) =>
          store.assignStudentToGroup(studentId, createdGroup.id)
        )

        await Promise.all(assignPromises)
        return createdGroup
      })

      const results = await Promise.all(groupPromises)
      const successCount = results.filter(r => r !== null).length

      if (successCount === 0) {
        throw new Error('Nenhum grupo foi criado')
      }

      console.log(`${successCount}/${groupsData.length} grupos criados`)
      return true

    } catch (err: any) {
      const errorMessage = err.message || 'Erro desconhecido'
      error.value = `Erro na criação de grupos: ${errorMessage}`
      console.error('Erro ao criar grupos:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Update student position
  const updateStudentPosition = async (
    studentId: number, 
    position: { x: number; y: number; z: number }
  ): Promise<boolean> => {
    try {
      const success = await store.updateStudentPosition(studentId, position)
      if (!success && store.error) {
        error.value = store.error
      }
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao atualizar posição'
      return false
    }
  }

  // Create a single group
  const createGroup = async (groupData: Omit<Group, 'id'>): Promise<Group | null> => {
    try {
      const group = await store.createGroup(groupData)
      if (!group && store.error) {
        error.value = store.error
      }
      return group
    } catch (err: any) {
      error.value = err.message || 'Erro ao criar grupo'
      return null
    }
  }

  // Update group
  const updateGroup = async (
    groupId: number, 
    groupData: Partial<Group>
  ): Promise<boolean> => {
    try {
      const success = await store.updateGroup(groupId, groupData)
      if (!success && store.error) {
        error.value = store.error
      }
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao atualizar grupo'
      return false
    }
  }

  // Assign student to group
  const assignStudentToGroup = async (
    studentId: number, 
    groupId: number
  ): Promise<boolean> => {
    try {
      const success = await store.assignStudentToGroup(studentId, groupId)
      if (!success && store.error) {
        error.value = store.error
      }
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao atribuir aluno'
      return false
    }
  }

  // Remove student from group
  const removeStudentFromGroup = async (studentId: number): Promise<boolean> => {
    try {
      const success = await store.removeStudentFromGroup(studentId)
      if (!success && store.error) {
        error.value = store.error
      }
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao remover aluno'
      return false
    }
  }

  // Delete group
  const deleteGroup = async (groupId: number): Promise<boolean> => {
    try {
      const success = await store.deleteGroup(groupId)
      if (!success && store.error) {
        error.value = store.error
      }
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao deletar grupo'
      return false
    }
  }

  // Save classroom layout
  const saveClassroomLayout = async (): Promise<boolean> => {
    try {
      const success = await store.saveClassroomLayout()
      if (!success && store.error) {
        error.value = store.error
      }
      return success
    } catch (err: any) {
      error.value = err.message || 'Erro ao salvar layout'
      return false
    }
  }

  // Get student by ID
  const getStudentById = (id: number): Student | undefined => {
    return students.value.find(s => s.id === id)
  }

  // Get group by ID
  const getGroupById = (id: number): Group | undefined => {
    return groups.value.find(g => g.id === id)
  }

  // Clear error
  const clearError = (): void => {
    error.value = null
    store.clearError()
  }

  // Reset classroom
  const resetClassroom = (): void => {
    store.resetClassroom()
    error.value = null
  }

  return {
    // State
    students,
    groups,
    activeClassroom,
    studentsWithoutGroup,
    groupsWithStudents,
    studentCount,
    groupCount,
    hasVisionIssues,
    isLoading,
    error,
    
    // Actions
    loadClassroom,
    optimizePlacement,
    createGroups,
    updateStudentPosition,
    createGroup,
    updateGroup,
    assignStudentToGroup,
    removeStudentFromGroup,
    deleteGroup,
    saveClassroomLayout,
    getStudentById,
    getGroupById,
    clearError,
    resetClassroom
  }
}