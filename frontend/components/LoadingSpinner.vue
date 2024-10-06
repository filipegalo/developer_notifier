<template>
  <div class="fixed inset-0 flex items-center justify-center bg-gray-100/50 dark:bg-gray-900/50 backdrop-blur-sm z-50">
    <div class="relative w-16 h-16">
      <div class="absolute top-0 left-0 right-0 bottom-0 border-4 border-blue-200 rounded-full"></div>
      <div class="absolute top-0 left-0 right-0 bottom-0 border-4 border-blue-500 rounded-full animate-spin" style="border-top-color: transparent"></div>
    </div>
  </div>
</template>

<style scoped>
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>