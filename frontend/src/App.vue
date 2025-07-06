<script setup lang="ts">

import AuthNavbar from "@/components/app/AuthNavbar.vue";
import GuestNavbar from "@/components/app/GuestNavbar.vue";
</script>

<template>
  <!-- Navbar for authenticated user : todo : update v-if when login completed -->
  <!-- <auth-navbar v-if="true" :user-type="'student'"/> -->
  <!-- Navbar for for guest user -->
  <!-- <guest-navbar v-else /> -->
  <router-view></router-view>
</template>

<style scoped>

</style>
