import { reactive } from 'vue'

export type Rule = (value: any) => string | true

export function useValidate<T extends Record<string, any>>(model: T) {
  const errors = reactive<Record<string, string | null>>({})

  const validateField = (key: keyof T, rules: Rule[]) => {
    const value = model[key]
    for (const rule of rules) {
      const res = rule(value)
      if (res !== true) {
        errors[key as string] = res
        return false
      }
    }
    errors[key as string] = null
    return true
  }

  const validateAll = (schema: Record<keyof T, Rule[]>) => {
    let ok = true
    for (const key in schema) {
      const valid = validateField(key, schema[key])
      if (!valid) ok = false
    }
    return ok
  }

  return { errors, validateField, validateAll }
}

// Built-in rules
export const required = (msg = 'Campo obrigatório'): Rule => (v) => {
  if (v === undefined || v === null) return msg
  if (typeof v === 'string' && v.trim().length === 0) return msg
  if (Array.isArray(v) && v.length === 0) return msg
  return true
}

export const minLength = (n: number, msg?: string): Rule => (v) => {
  if (typeof v === 'string' && v.trim().length < n) return msg || `Mínimo de ${n} caracteres`
  return true
}

export const isEmail: Rule = (v) => {
  if (typeof v !== 'string') return 'E-mail inválido'
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(v) || 'E-mail inválido'
}
