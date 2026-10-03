<template>
  <div class="flex items-center justify-center" :class="containerClass">
    <div class="relative">
      <!-- Main spinner -->
      <div 
        class="animate-spin rounded-full border-4 border-solid"
        :class="[
          size === 'sm' ? 'w-6 h-6 border-2' : size === 'lg' ? 'w-12 h-12' : 'w-8 h-8',
          `border-${color}/20 border-t-${color}`
        ]"
      ></div>
      
      <!-- Optional pulse effect -->
      <div 
        v-if="pulse"
        class="absolute inset-0 rounded-full animate-pulse"
        :class="[
          size === 'sm' ? 'w-6 h-6' : size === 'lg' ? 'w-12 h-12' : 'w-8 h-8',
          `bg-${color}/10`
        ]"
      ></div>
    </div>
    
    <!-- Optional text -->
    <span 
      v-if="text" 
      class="ml-3 text-sm font-medium animate-pulse"
      :class="`text-${color}`"
    >
      {{ text }}
    </span>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: 'md', // sm, md, lg
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  color: {
    type: String,
    default: 'primary'
  },
  text: {
    type: String,
    default: ''
  },
  pulse: {
    type: Boolean,
    default: false
  },
  containerClass: {
    type: String,
    default: 'py-4'
  }
})
</script>