<template>
  <div class="flex items-center">
    <span class="mr-2 dark:text-white">Backend API Status:</span>
    <button
      :class="[
        'px-3 py-1 rounded-full text-sm font-semibold',
        isApiUp ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      ]"
    >
      {{ isApiUp ? 'Up' : 'Down' }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '~/config';

const isApiUp = ref(false);

const checkApiStatus = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    isApiUp.value = response.ok;
  } catch (error) {
    console.error('Error checking API status:', error);
    isApiUp.value = false;
  }
};

onMounted(() => {
  checkApiStatus();
  setInterval(checkApiStatus, 300000);
});
</script>