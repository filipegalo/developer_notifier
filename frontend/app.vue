<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 flex flex-col">
    <SettingsModal :show="showSettings" @close="closeSettings" @settings-updated="fetchSettings" />
    <header class="bg-white dark:bg-gray-800 shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            {{ greeting }}{{ userName ? `, ${userName}` : '' }}
          </h1>
          <div class="flex items-center">
            <ApiStatus class="mr-4" />
            <button @click="openSettings" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
            <DarkModeToggle />
          </div>
        </div>
      </div>
    </header>
    <main class="flex-grow">
      <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
          <div v-if="isLoading" class="text-center py-12">
            <LoadingSpinner />
            <p class="mt-4 text-xl text-gray-600 dark:text-gray-400">Loading settings...</p>
          </div>
          <div v-else-if="showComponents" class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <IssuesList v-if="showJira" @loading="updateLoadingState" />
            <PullRequestsList v-if="showGithub" @loading="updateLoadingState" />
          </div>
          <div v-else class="text-center py-12">
            <p class="text-xl text-gray-600 dark:text-gray-400 mb-4">
              {{ settingsError || "Configure your project settings to get started" }}
            </p>
            <button @click="openSettings" class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition ease-in-out duration-150">
              Open Settings
            </button>
          </div>
        </div>
      </div>
    </main>
    <footer class="bg-white dark:bg-gray-800 shadow">
      <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
        <p class="text-center text-gray-500 dark:text-gray-400 text-sm">
          Made by Filipe Galo
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import IssuesList from '~/components/IssuesList.vue';
import PullRequestsList from '~/components/PullRequestsList.vue';
import ApiStatus from '~/components/ApiStatus.vue';
import DarkModeToggle from '~/components/DarkModeToggle.vue';
import LoadingSpinner from '~/components/LoadingSpinner.vue';
import SettingsModal from '~/components/SettingsModal.vue';
import { API_BASE_URL } from '~/config';

const isLoading = ref(true);
const loadingComponents = ref(new Set());
const showSettings = ref(false);
const hasSettings = ref(false);
const settingsError = ref(null);
const showJira = ref(false);
const showGithub = ref(false);
const userName = ref('');

const showComponents = computed(() => {
  return showJira.value || showGithub.value;
});

const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 6) return 'Good night';
  if (hour < 12) return 'Good morning';
  if (hour < 18) return 'Good afternoon';
  if (hour < 22) return 'Good evening';
});

const updateLoadingState = (componentName, loading) => {
  if (loading) {
    loadingComponents.value.add(componentName);
  } else {
    loadingComponents.value.delete(componentName);
  }
};

const openSettings = () => {
  showSettings.value = true;
};

const closeSettings = () => {
  showSettings.value = false;
  fetchSettings();
};

const fetchSettings = async () => {
  isLoading.value = true;
  settingsError.value = null;
  try {
    const response = await fetch(`${API_BASE_URL}/settings`);
    if (!response.ok) {
      if (response.status === 404) {
        hasSettings.value = false;
        settingsError.value = "Settings not found. Please configure your settings.";
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } else {
      const data = await response.json();
      hasSettings.value = Object.keys(data).length > 0;
      if (hasSettings.value) {
        showJira.value = !!data.jira_api_url;
        showGithub.value = !!data.github_api_url;
        userName.value = data.user_name || '';
        if (!showJira.value && !showGithub.value) {
          settingsError.value = "Configure your project settings to get started.";
        }
      } else {
        settingsError.value = "No settings found. Please configure your settings.";
      }
    }
  } catch (error) {
    console.error('Error fetching settings:', error);
    hasSettings.value = false;
    settingsError.value = "An error occurred while fetching settings. Please try again.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchSettings();
});

</script>