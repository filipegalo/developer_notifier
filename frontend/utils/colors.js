export const colorPalette = [
  'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100',
  'bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-100',
  'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100',
  'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100',
  'bg-indigo-100 text-indigo-800 dark:bg-indigo-800 dark:text-indigo-100',
  'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
  'bg-pink-100 text-pink-800 dark:bg-pink-800 dark:text-pink-100',
  'bg-teal-100 text-teal-800 dark:bg-teal-800 dark:text-teal-100',
  'bg-orange-100 text-orange-800 dark:bg-orange-800 dark:text-orange-100',
  'bg-cyan-100 text-cyan-800 dark:bg-cyan-800 dark:text-cyan-100',
];

const colorMap = new Map();
let colorIndex = 0;

export function getColor(key) {
  if (key === 'ALL') {
    return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100';
  }
  
  if (!colorMap.has(key)) {
    colorMap.set(key, colorPalette[colorIndex]);
    colorIndex = (colorIndex + 1) % colorPalette.length;
  }
  
  return colorMap.get(key);
}