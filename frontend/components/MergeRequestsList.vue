<template>
    <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center">
            <img src="/images/gitlab.svg" alt="GitHub Icon" class="w-6 h-6 mr-2">
            <h2 class="text-lg leading-6 font-medium text-gray-900 dark:text-white">GitLab Merge Requests</h2>
          </div>
          <button @click="refreshPullRequests" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
        <div class="flex flex-wrap items-center">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap mr-3 mb-2">Filter by repository:</span>
          <div class="flex flex-wrap">
            <button
              v-for="repo in ['ALL', ...repoTypes]"
              :key="repo"
              @click="selectedRepo = repo"
              :class="[
                'px-3 py-1 rounded-full text-xs font-semibold mr-2 mb-2',
                selectedRepo === repo ? 'bg-indigo-600 text-white' : repoColor(repo)
              ]"
            >
              {{ repo }}
            </button>
          </div>
        </div>
      </div>
      <div class="border-t border-gray-200 dark:border-gray-700">
        <div v-if="loading" class="flex justify-center items-center py-8">
          <div class="spinner dark:border-gray-600 dark:border-l-blue-500"></div>
        </div>
        <div v-else-if="error" class="px-4 py-5 sm:px-6 text-center text-red-600 dark:text-red-400">
          {{ error }}
        </div>
        <ul v-else-if="filteredPullRequests.length" role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
          <li v-for="pr in filteredPullRequests" :key="pr.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50 dark:hover:bg-gray-700">
            <div class="flex items-center justify-between">
              <a :href="pr.url" target="_blank" rel="noopener noreferrer" class="text-sm font-medium text-indigo-600 dark:text-indigo-400 truncate hover:underline">
                {{ pr.title }}
              </a>
              <div class="ml-2 flex-shrink-0 flex">
                <p :class="[
                  'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                  pr.is_assigned ? 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100' : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200'
                ]">
                  {{ pr.is_assigned ? 'Assigned' : 'Review' }}
                </p>
              </div>
            </div>
            <div class="mt-2 sm:flex sm:justify-between">
              <div class="sm:flex">
                <p class="flex items-center text-sm text-gray-500 dark:text-gray-400">
                  {{ pr.repository }}
                </p>
              </div>
              <div class="mt-2 flex items-center text-sm text-gray-500 dark:text-gray-400 sm:mt-0">
                <p>
                  Created: {{ formatDate(pr.created_at) }}
                </p>
              </div>
            </div>
          </li>
        </ul>
        <div v-else class="px-4 py-5 sm:px-6 text-center text-gray-500 dark:text-gray-400">
          No pull requests found.
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { API_BASE_URL } from '~/config';
  import { getColor } from '~/utils/colors';
  
  const pullRequests = ref([]);
  const loading = ref(true);
  const error = ref(null);
  const selectedRepo = ref('ALL');
  const repoTypes = ref([]);
  
  const emit = defineEmits(['loading']);
  
  const filteredPullRequests = computed(() => {
    if (selectedRepo.value === 'ALL') {
      return pullRequests.value;
    }
    return pullRequests.value.filter(pr => pr.repository === selectedRepo.value);
  });
  
  const refreshPullRequests = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await fetch(`${API_BASE_URL}/merge-requests`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || 'Failed to fetch pull requests');
      }
      const data = await response.json();
      pullRequests.value = data.merge_requests;
      
      const uniqueRepos = new Set(pullRequests.value.map(pr => pr.repository));
      repoTypes.value = Array.from(uniqueRepos);
    } catch (err) {
      console.error('Error fetching pull requests:', err);
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };
  
  onMounted(async () => {
    emit('loading', 'MergeRequestsList', true);
    await refreshPullRequests();
    emit('loading', 'MergeRequestsList', false);
  });
  
  const repoColor = (repo) => getColor(repo);
  
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };
  </script>
  
  <style scoped>
  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border-left-color: #09f;
    animation: spin 1s ease infinite;
  }
  
  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  </style>