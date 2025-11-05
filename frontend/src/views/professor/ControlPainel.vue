<template>
  <div class="classroom-dashboard">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>{{ classroom.name }}</h2>
      <div class="btn-group">
        <button class="btn btn-primary" @click="toggleViewMode">
          {{ is3DView ? '2D' : '3D' }} View
        </button>
        <button class="btn btn-outline-primary" @click="showAutoArrangeModal">
          Auto Arranjo
        </button>
      </div>
    </div>
    
    <div class="row">
      <div class="col-md-8">
        <Classroom3DView 
          v-if="is3DView" 
          :students="classroom.students"
          @studentSelected="handleStudentSelection"
        />
        <Classroom2DView v-else />
      </div>
      
      <div class="col-md-4">
        <StudentInfoPanel :student="selectedStudent" />
        <LearningAnalytics :classroom="classroom" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Classroom3DView from '@components/classroom/Classroom3DView.vue';
import Classroom2DView from '@components/classroom/Classroom2DView.vue';
import StudentInfoPanel from '@components/classroom/StudentInfoPanel.vue';
import LearningAnalytics from '@components/classroom/LearningAnalytics.vue';

export default defineComponent({
  name: 'ControlPainel',
  components: {
    Classroom3DView,
    Classroom2DView,
    StudentInfoPanel,
    LearningAnalytics
  },
  setup() {
    // Adapte a lógica conforme sua store e props
    const classroom = ref({ name: 'Turma 1A', students: [] });
    const selectedStudent = ref(null);
    const is3DView = ref(true);

    function toggleViewMode() {
      is3DView.value = !is3DView.value;
    }
    function showAutoArrangeModal() {
      // lógica para abrir modal
    }
    function handleStudentSelection(student: any) {
      selectedStudent.value = student;
    }

    return {
      classroom,
      selectedStudent,
      is3DView,
      toggleViewMode,
      showAutoArrangeModal,
      handleStudentSelection
    };
  }
});
</script>

<style scoped>
.classroom-dashboard {
  padding: 20px;
}

.btn-group {
  margin-left: auto;
}

.row {
  margin-top: 20px;
}
</style>