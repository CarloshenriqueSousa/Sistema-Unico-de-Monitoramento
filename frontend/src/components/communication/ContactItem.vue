<template>
  <button
    @click="$emit('select', contact)"
    class="contact-item group w-full text-left bg-white hover:bg-[#e1d4c2]/30 border border-[#e1d4c2] rounded-xl p-4 transition-all duration-200"
    :class="{ 'ring-2 ring-[#2d531a] bg-[#e1d4c2]/20': isSelected }"
  >
    <div class="flex items-center gap-3">
      <!-- Avatar with Online Status -->
      <div class="relative flex-shrink-0">
        <div 
          class="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg transition-transform group-hover:scale-105"
          :class="contact?.online 
            ? 'bg-gradient-to-br from-[#2d531a] to-[#0f1e3f]' 
            : 'bg-[#1f1d20]/40'"
        >
          {{ getInitials(contact?.name) }}
        </div>
        
        <!-- Online Indicator -->
        <div 
          v-if="contact?.online"
          class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-400 rounded-full border-2 border-white animate-pulse"
        ></div>
        <div 
          v-else
          class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-[#1f1d20]/30 rounded-full border-2 border-white"
        ></div>
      </div>

      <!-- Contact Info -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center justify-between mb-1">
          <h4 class="font-semibold text-[#1f1d20] truncate">
            {{ contact?.name }}
          </h4>
          <span v-if="contact?.lastMessageTime" class="text-xs text-[#1f1d20]/50 flex-shrink-0">
            {{ contact.lastMessageTime }}
          </span>
        </div>

        <div class="flex items-center justify-between">
          <p class="text-sm text-[#1f1d20]/60 truncate">
            {{ contact?.lastMessage || (contact?.online ? 'Online' : 'Offline') }}
          </p>
          
          <!-- Unread Badge -->
          <div 
            v-if="contact?.unreadCount && contact.unreadCount > 0"
            class="flex-shrink-0 ml-2 w-5 h-5 rounded-full bg-[#2d531a] flex items-center justify-center"
          >
            <span class="text-xs text-white font-bold">
              {{ contact.unreadCount > 9 ? '9+' : contact.unreadCount }}
            </span>
          </div>
        </div>
      </div>

      <!-- Chevron -->
      <svg 
        class="w-5 h-5 text-[#1f1d20]/40 transform transition-transform group-hover:translate-x-1" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </div>

    <!-- Additional Info (Role/Position) -->
    <div v-if="contact?.role" class="mt-2 pt-2 border-t border-[#e1d4c2]">
      <div class="flex items-center gap-2">
        <svg class="w-3.5 h-3.5 text-[#1f1d20]/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
        <span class="text-xs text-[#1f1d20]/50">{{ contact.role }}</span>
      </div>
    </div>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Contact {
  id: string;
  name: string;
  online: boolean;
  lastMessage?: string;
  lastMessageTime?: string;
  unreadCount?: number;
  role?: string;
}

const props = defineProps<{
  contact?: Contact;
  isSelected?: boolean;
}>();

defineEmits<{
  select: [contact?: Contact];
}>();

const getInitials = (name?: string) => {
  if (!name) return '?';
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};
</script>