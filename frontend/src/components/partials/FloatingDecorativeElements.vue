<script setup lang="ts">

</script>

<template>
  <div class="absolute z-0 inset-0 overflow-hidden pointer-events-none">
    <div class="absolute top-16 left-8 w-14 h-14 bg-yellow-300 rounded-full opacity-60 animate-bounce"></div>
    <div
        class="absolute top-32 right-16 w-18 h-18 bg-green-300 rounded-full opacity-60 animate-bounce"
        style="animation-delay: 0.3s"
    ></div>
    <div
        class="absolute bottom-40 left-16 w-16 h-16 bg-orange-300 rounded-full opacity-60 animate-bounce"
        style="animation-delay: 0.8s"
    ></div>
    <div
        class="absolute bottom-24 right-12 w-12 h-12 bg-cyan-300 rounded-full opacity-60 animate-bounce"
        style="animation-delay: 1.2s"
    ></div>
    <div
        class="absolute top-1/2 left-4 w-10 h-10 bg-red-300 rounded-full opacity-60 animate-bounce"
        style="animation-delay: 1.8s"
    ></div>
  </div>
</template>

<style scoped>

</style>