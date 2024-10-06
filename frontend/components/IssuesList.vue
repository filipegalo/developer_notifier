<template>
  <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
    <div class="px-4 py-5 sm:px-6">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center">
          <img src="/images/jira.svg" alt="Jira Icon" class="w-6 h-6 mr-2">
          <h2 class="text-lg leading-6 font-medium text-gray-900 dark:text-white">Jira Issues</h2>
        </div>
        <button @click="refreshIssues" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors duration-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
      <div class="flex flex-wrap items-center -mb-2">
        <span class="mr-3 mb-2 text-sm font-medium text-gray-700 dark:text-gray-300 whitespace-nowrap">Filter by project:</span>
        <div class="flex flex-wrap">
          <button
            v-for="project in ['ALL', ...projectTypes]"
            :key="project"
            @click="selectedProject = project"
            :class="[
              'px-3 py-1 rounded-full text-xs font-semibold mr-2 mb-2',
              selectedProject === project ? 'bg-indigo-600 text-white' : projectColor(project)
            ]"
          >
            {{ project }}
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
      <ul v-else-if="filteredIssues.length" role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
        <li v-for="issue in filteredIssues" :key="issue.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50 dark:hover:bg-gray-700">
          <div class="flex items-center justify-between">
            <a :href="issue.url" target="_blank" rel="noopener noreferrer" class="text-sm font-medium text-indigo-600 dark:text-indigo-400 truncate hover:underline">
              {{ issue.title }}
            </a>
            <div class="ml-2 flex-shrink-0 flex">
              <p :class="[
                'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                statusColor(issue.status)
              ]">
                {{ issue.status }}
              </p>
            </div>
          </div>
          <div class="mt-2 sm:flex sm:justify-between">
            <div class="sm:flex">
              <p class="flex items-center text-sm text-gray-500 dark:text-gray-400">
                {{ issue.issue }}
              </p>
            </div>
            <div class="mt-2 flex items-center text-sm text-gray-500 dark:text-gray-400 sm:mt-0">
              <p>
                Updated: {{ formatDate(issue.updated_at) }}
              </p>
            </div>
          </div>
        </li>
      </ul>
      <div v-else class="px-4 py-5 sm:px-6 text-center text-gray-500 dark:text-gray-400">
        No issues found.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { API_BASE_URL } from '~/config';
import { getColor } from '~/utils/colors';

const issues = ref([]);
const loading = ref(true);
const error = ref(null);
const selectedProject = ref('ALL');
const projectTypes = ref([]);

const emit = defineEmits(['loading']);

const filteredIssues = computed(() => {
  if (selectedProject.value === 'ALL') {
    return issues.value;
  }
  return issues.value.filter(issue => issue.issue.startsWith(selectedProject.value));
});

const refreshIssues = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await fetch(`${API_BASE_URL}/issues`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail?.message || 'Failed to fetch issues');
    }
    const data = await response.json();
    issues.value = data.issues;
    
    const uniqueProjects = new Set(issues.value.map(issue => issue.issue.split('-')[0]));
    projectTypes.value = Array.from(uniqueProjects);
  } catch (err) {
    console.error('Error fetching issues:', err);
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  emit('loading', 'IssuesList', true);
  await refreshIssues();
  emit('loading', 'IssuesList', false);
});

const statusColor = (status) => {
  switch (status.toLowerCase()) {
    case 'in progress':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100';
    case 'to do':
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100';
    case 'idea':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-100';
    case 'backlog':
      return 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100';
    default:
      return 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100';
  }
};

const projectColor = (project) => getColor(project);

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