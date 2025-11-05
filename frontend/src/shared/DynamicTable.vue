<template>
  <div class="table-wrapper">
    <div v-if="searchable || title" class="table-header">
      <h3 v-if="title" class="table-title">{{ title }}</h3>
      <div v-if="searchable" class="search-box">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="m21 21-4.35-4.35"/>
        </svg>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Buscar..."
          class="search-input"
        />
      </div>
    </div>
    
    <div class="table-container">
      <table class="dynamic-table">
        <thead>
          <tr>
            <th 
              v-for="column in columns" 
              :key="column.key"
              :class="{ 'sortable': column.sortable }"
              @click="column.sortable ? sortBy(column.key) : null"
            >
              <div class="th-content">
                {{ column.label }}
                <span v-if="column.sortable" class="sort-icon">
                  <svg v-if="sortKey === column.key && sortOrder === 'asc'" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M7 14l5-5 5 5z"/>
                  </svg>
                  <svg v-else-if="sortKey === column.key && sortOrder === 'desc'" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M7 10l5 5 5-5z"/>
                  </svg>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="currentColor" opacity="0.3">
                    <path d="M7 10l5 5 5-5z"/>
                  </svg>
                </span>
              </div>
            </th>
            <th v-if="actions" class="actions-column">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredData.length === 0">
            <td :colspan="columns.length + (actions ? 1 : 0)" class="empty-state">
              <div class="empty-content">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 8v4M12 16h.01"/>
                </svg>
                <p>Nenhum dado encontrado</p>
              </div>
            </td>
          </tr>
          <tr 
            v-for="(row, index) in paginatedData" 
            :key="index"
            @click="$emit('row-click', row)"
            :class="{ 'clickable': $attrs['onRow-click'] }"
          >
            <td v-for="column in columns" :key="column.key">
              <slot :name="`cell-${column.key}`" :row="row" :value="row[column.key]">
                {{ formatCell(row[column.key], column) }}
              </slot>
            </td>
            <td v-if="actions" class="actions-cell">
              <slot name="actions" :row="row"></slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="paginated && filteredData.length > 0" class="pagination">
      <button 
        @click="currentPage--" 
        :disabled="currentPage === 1"
        class="pagination-btn"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M15 18l-6-6 6-6"/>
        </svg>
      </button>
      
      <div class="page-info">
        Página {{ currentPage }} de {{ totalPages }}
      </div>
      
      <button 
        @click="currentPage++" 
        :disabled="currentPage === totalPages"
        class="pagination-btn"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 18l6-6-6-6"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

interface Column {
  key: string
  label: string
  sortable?: boolean
  format?: (value: any) => string
  width?: string
  align?: 'left' | 'center' | 'right'
  type?: 'text' | 'number' | 'date' | 'boolean' | 'custom'
}

interface TableRow {
  [key: string]: any
}

const props = withDefaults(defineProps<{
  columns: Column[]
  data: TableRow[]
  searchable?: boolean
  paginated?: boolean
  perPage?: number
  actions?: boolean
  title?: string
  loading?: boolean
  selectable?: boolean
  multiSelect?: boolean
  sortable?: boolean
  filterable?: boolean
  exportable?: boolean
  refreshable?: boolean
  striped?: boolean
  hoverable?: boolean
  compact?: boolean
  bordered?: boolean
  showSummary?: boolean
  summaryColumns?: string[]
  customFilters?: Array<{
    key: string
    label: string
    type: 'select' | 'input' | 'date' | 'number'
    options?: Array<{ value: any; label: string }>
  }>
}>(), {
  searchable: false,
  paginated: false,
  perPage: 10,
  actions: false,
  title: '',
  loading: false,
  selectable: false,
  multiSelect: false,
  sortable: true,
  filterable: false,
  exportable: false,
  refreshable: false,
  striped: true,
  hoverable: true,
  compact: false,
  bordered: false,
  showSummary: false,
  summaryColumns: () => [],
  customFilters: () => []
})

const emit = defineEmits<{
  'row-click': [row: TableRow, index: number]
  'row-select': [row: TableRow, selected: boolean]
  'selection-change': [selectedRows: TableRow[]]
  'sort-change': [column: string, direction: 'asc' | 'desc']
  'filter-change': [filters: Record<string, any>]
  'export': [format: 'csv' | 'excel' | 'pdf']
  'refresh': []
}>()

const searchQuery = ref('')
const sortKey = ref('')
const sortOrder = ref<'asc' | 'desc'>('asc')
const currentPage = ref(1)
const selectedRows = ref<Set<number>>(new Set())
const customFilters = ref<Record<string, any>>({})
const isLoading = ref(props.loading)

// Computed properties
const filteredData = computed(() => {
  let result = [...props.data]
  
  // Apply search
  if (searchQuery.value) {
    result = result.filter(row => {
      return props.columns.some(col => {
        const value = String(row[col.key]).toLowerCase()
        return value.includes(searchQuery.value.toLowerCase())
      })
    })
  }
  
  // Apply custom filters
  Object.entries(customFilters.value).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      result = result.filter(row => {
        const rowValue = row[key]
        if (typeof value === 'string') {
          return String(rowValue).toLowerCase().includes(value.toLowerCase())
        }
        return rowValue === value
      })
    }
  })
  
  // Apply sorting
  if (sortKey.value && props.sortable) {
    result.sort((a, b) => {
      const aVal = a[sortKey.value]
      const bVal = b[sortKey.value]
      
      if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
      if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
      return 0
    })
  }
  
  return result
})

const totalPages = computed(() => {
  if (!props.paginated) return 1
  return Math.ceil(filteredData.value.length / props.perPage)
})

const paginatedData = computed(() => {
  if (!props.paginated) return filteredData.value
  
  const start = (currentPage.value - 1) * props.perPage
  const end = start + props.perPage
  return filteredData.value.slice(start, end)
})

const summaryData = computed(() => {
  if (!props.showSummary || props.summaryColumns.length === 0) return {}
  
  const summary: Record<string, any> = {}
  
  props.summaryColumns.forEach(columnKey => {
    const column = props.columns.find(col => col.key === columnKey)
    if (!column) return
    
    const values = filteredData.value.map(row => row[columnKey])
    
    if (column.type === 'number') {
      summary[columnKey] = {
        sum: values.reduce((sum, val) => sum + (Number(val) || 0), 0),
        avg: values.reduce((sum, val) => sum + (Number(val) || 0), 0) / values.length,
        min: Math.min(...values.map(val => Number(val) || 0)),
        max: Math.max(...values.map(val => Number(val) || 0))
      }
    } else {
      summary[columnKey] = {
        count: values.length,
        unique: new Set(values).size
      }
    }
  })
  
  return summary
})

// Methods
const sortBy = (key: string) => {
  if (!props.sortable) return
  
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  
  emit('sort-change', key, sortOrder.value)
}

const formatCell = (value: any, column: Column) => {
  if (column.format && typeof column.format === 'function') {
    return column.format(value)
  }
  
  if (column.type === 'date' && value) {
    return new Date(value).toLocaleDateString()
  }
  
  if (column.type === 'boolean') {
    return value ? 'Sim' : 'Não'
  }
  
  return value
}

const handleRowClick = (row: TableRow, index: number) => {
  emit('row-click', row, index)
}

const handleRowSelect = (row: TableRow, index: number, selected: boolean) => {
  if (selected) {
    selectedRows.value.add(index)
  } else {
    selectedRows.value.delete(index)
  }
  
  emit('row-select', row, selected)
  emit('selection-change', Array.from(selectedRows.value).map(i => props.data[i]))
}

const handleSelectAll = (selected: boolean) => {
  if (selected) {
    paginatedData.value.forEach((_, index) => {
      selectedRows.value.add(index)
    })
  } else {
    paginatedData.value.forEach((_, index) => {
      selectedRows.value.delete(index)
    })
  }
  
  emit('selection-change', Array.from(selectedRows.value).map(i => props.data[i]))
}

const handleFilterChange = (key: string, value: any) => {
  customFilters.value[key] = value
  emit('filter-change', customFilters.value)
}

const exportData = (format: 'csv' | 'excel' | 'pdf') => {
  emit('export', format)
}

const refresh = () => {
  emit('refresh')
}

const clearFilters = () => {
  customFilters.value = {}
  searchQuery.value = ''
  emit('filter-change', {})
}

// Watchers
watch(() => props.loading, (newVal) => {
  isLoading.value = newVal
})

watch(() => props.data, () => {
  selectedRows.value.clear()
}, { deep: true })

// Lifecycle
onMounted(() => {
  if (props.customFilters.length > 0) {
    props.customFilters.forEach(filter => {
      customFilters.value[filter.key] = null
    })
  }
})
</script>

<style scoped>
.table-wrapper {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid #e5e7eb;
  flex-wrap: wrap;
}

.table-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.search-box {
  position: relative;
  min-width: 250px;
}

.search-icon {
  position: absolute;
  left: 0.875rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 0.625rem 1rem 0.625rem 2.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.9375rem;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.table-container {
  overflow-x: auto;
}

.dynamic-table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
}

th {
  padding: 1rem 1.5rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #6b7280;
  white-space: nowrap;
}

th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}

th.sortable:hover {
  background: rgba(102, 126, 234, 0.05);
}

.th-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-icon {
  display: flex;
  align-items: center;
  color: #667eea;
}

.actions-column {
  text-align: center;
}

td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f3f4f6;
  color: #374151;
  font-size: 0.9375rem;
}

tr.clickable {
  cursor: pointer;
  transition: background 0.2s;
}

tr.clickable:hover {
  background: #f9fafb;
}

tbody tr:last-child td {
  border-bottom: none;
}

.actions-cell {
  text-align: center;
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.empty-state {
  padding: 3rem 1.5rem;
  text-align: center;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #9ca3af;
}

.empty-content svg {
  opacity: 0.5;
}

.empty-content p {
  margin: 0;
  font-size: 1rem;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.pagination-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #6b7280;
}

.pagination-btn:not(:disabled):hover {
  border-color: #667eea;
  color: #667eea;
  background: #f9fafb;
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}
</style>