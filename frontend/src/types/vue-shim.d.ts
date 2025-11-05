declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module '@/shared/InteractiveChart.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{
    data: any
    type?: string
    chartTypes?: string[]
    options?: any
    title?: string
    subtitle?: string
    showLegend?: boolean
    loading?: boolean
    responsive?: boolean
    animated?: boolean
  }>
  export default component
}

declare module '@/shared/SkillRadar.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{
    skills: Array<{ name: string; value: number }>
    size?: number
    levels?: number
    title?: string
    subtitle?: string
    showLegend?: boolean
    glow?: boolean
    animated?: boolean
  }>
  export default component
}

declare module '@/shared/DynamicTable.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{
    columns: Array<{ key: string; label: string; sortable?: boolean; format?: Function }>
    data: any[]
    searchable?: boolean
    paginated?: boolean
    perPage?: number
    actions?: boolean
    title?: string
  }>
  export default component
}

declare module '@/components/classroom/ClassroomMap3D.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{
    classroomId: string
    height?: string
    interactive?: boolean
    simulationMode?: boolean
    simulationOptions?: any
    editMode?: boolean
    seats?: { rows: number; cols: number }
    showLabels?: boolean
    showHeatmap?: boolean
  }>
  export default component
}
