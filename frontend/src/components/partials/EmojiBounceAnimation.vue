<template>
  <div :class="`mt-6 flex justify-${align} space-x-4`">
    <div class="text-2xl animate-bounce" :style="'animation-delay: '+(i*0.2)+'s'" v-for="(emoji,i) in emojis">
      {{ emoji }}
    </div>
  </div>
</template>
<script setup>
import {defineProps} from 'vue';

const props = defineProps({
  emojis: {
    type: Array,
    required: true,
    default: () => [
      '🎮',
      '📚',
      '🏆',
      '⭐',
    ]
  },
  align:{
    default: 'center',
  }

})

</script>