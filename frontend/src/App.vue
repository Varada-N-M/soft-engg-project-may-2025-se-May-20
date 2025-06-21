<script setup lang="ts">

import AuthNavbar from "@/components/app/auth-navbar.vue";
import GuestNavbar from "@/components/app/guest-navbar.vue";
</script>

<template>
  <!-- Navbar for authenticated user : todo : update v-if when login completed -->
  <auth-navbar v-if="false" :user-type="'student'"/>
  <!-- Navbar for for guest user -->
  <guest-navbar v-else />
  <router-view></router-view>
</template>

<style scoped>

</style>
