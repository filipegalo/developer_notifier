<template>
  <div v-if="show" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center">
    <div class="relative w-full max-w-md p-6 bg-white dark:bg-gray-800 rounded-lg shadow-xl transform transition-all">
      <div class="absolute top-0 right-0 pt-4 pr-4">
        <button @click="closeModal" class="text-gray-400 hover:text-gray-500 focus:outline-none focus:text-gray-500 transition ease-in-out duration-150">
          <svg class="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="mt-3">
        <h3 class="text-2xl leading-6 font-bold text-gray-900 dark:text-white text-center mb-6">Settings</h3>
        <div v-if="saveStatus" :class="['text-center p-2 mb-4 rounded', saveStatus === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']">
          {{ saveStatus === 'success' ? 'Settings saved successfully!' : 'Failed to save settings. Please try again.' }}
        </div>
        <div class="mt-2">
          <div v-if="settings" class="space-y-6">
            <div v-for="(value, key) in settings" :key="key" class="flex flex-col">
              <label :for="key" class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-1">
                {{ formatKey(key) }}
              </label>
              <input
                :id="key"
                v-model="settings[key]"
                :type="shouldMask(key) ? 'password' : 'text'"
                :placeholder="shouldMask(key) ? '******************' : ''"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white text-sm"
              />
            </div>
          </div>
          <div v-else class="text-gray-500 dark:text-gray-400 text-center">
            <svg class="animate-spin h-8 w-8 mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Loading settings...
          </div>
        </div>
        <div class="mt-8 flex justify-end space-x-3">
          <button
            @click="closeModal"
            class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition ease-in-out duration-150"
          >
            Cancel
          </button>
          <button
            @click="saveSettings"
            :disabled="!hasChanges || isSaving"
            :class="[
              'px-4 py-2 text-white text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition ease-in-out duration-150',
              hasChanges && !isSaving ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-400 cursor-not-allowed'
            ]"
          >
            {{ isSaving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { API_BASE_URL } from '~/config';

const props = defineProps({
  show: Boolean
});

const emit = defineEmits(['close', 'settings-updated']);

const settings = ref(null);
const originalSettings = ref(null);
const saveStatus = ref(null);
const isSaving = ref(false);

const fetchSettings = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/settings`);
    const data = await response.json();
    
    originalSettings.value = { ...data };
    settings.value = {
      jira_api_email: data.jira_api_email || '',
      jira_api_key: '',
      jira_api_url: data.jira_api_url || '',
      github_access_token: '',
      github_org: data.github_org || '',
      github_api_url: data.github_api_url || '',
      github_user: data.github_user || '',
      user_name: data.user_name || ''
    };
  } catch (error) {
    console.error('Error fetching settings:', error);
  }
};

const hasChanges = computed(() => {
  if (!settings.value || !originalSettings.value) return false;
  
  return Object.keys(settings.value).some(key => {
    if (key === 'jira_api_key' || key === 'github_access_token') {
      return settings.value[key] !== '';
    }
    return settings.value[key] !== originalSettings.value[key];
  });
});

const saveSettings = async () => {
  if (!hasChanges.value) return;
  
  isSaving.value = true;
  saveStatus.value = null;
  
  try {
    const settingsToSave = { ...settings.value };
    
    if (!settingsToSave.jira_api_key) {
      delete settingsToSave.jira_api_key;
    }
    if (!settingsToSave.github_access_token) {
      delete settingsToSave.github_access_token;
    }

    const response = await fetch(`${API_BASE_URL}/settings`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(settingsToSave),
    });
    
    if (response.ok) {
      saveStatus.value = 'success';
      emit('settings-updated');
      setTimeout(() => {
        closeModal();
      }, 1000);
    } else {
      saveStatus.value = 'error';
    }
  } catch (error) {
    console.error('Error saving settings:', error);
    saveStatus.value = 'error';
  } finally {
    isSaving.value = false;
  }
};

const closeModal = () => {
  saveStatus.value = null;
  emit('close');
};

const formatKey = (key) => {
  return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
};

const shouldMask = (key) => {
  return ['jira_api_key', 'github_access_token'].includes(key);
};

watch(() => props.show, (newValue) => {
  if (newValue) {
    fetchSettings();
    saveStatus.value = null;
  }
});

onMounted(() => {
  if (props.show) {
    fetchSettings();
  }
});
</script>