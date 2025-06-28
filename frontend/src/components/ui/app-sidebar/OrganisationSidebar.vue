<script setup lang="ts">

import {Calendar, Home, Inbox, PersonStanding, Search, Settings} from "lucide-vue-next"
import {
  Sidebar,
  SidebarContent, SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel, SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

// Menu items.
const items = [
  {
    title: "Home",
    url: "/org/home",
    icon: Home,
  },
  {
    title: "Teachers",
    url: "/org/teachers",
    icon: PersonStanding,
  },
];
</script>

<template>
  <Sidebar collapsible="icon">
    <SidebarHeader/>
    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel>Application</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem v-for="item in items" :key="item.title">
              <SidebarMenuButton asChild>
                <router-link :to="item.url">
                  <component :is="item.icon"/>
                  <span>{{ item.title }}</span>
                </router-link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>
    <SidebarFooter/>
  </Sidebar>
</template>