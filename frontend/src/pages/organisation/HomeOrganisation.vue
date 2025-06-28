<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <OrgDashboardLayout>
      <template v-slot:breadcrumb>
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem class="hidden md:block">
              <BreadcrumbLink href="#">
                Organisation
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator class="hidden md:block"/>
            <BreadcrumbItem>
              <BreadcrumbPage>Dashboard</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </template>
      <header class="bg-white shadow-sm border-b">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between items-center py-4">
            <div class="flex items-center space-x-4">
              <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <Users class="w-6 h-6 text-white"/>
              </div>
              <div>
                <h1 class="text-2xl font-bold text-gray-900">Child Welfare Dashboard</h1>
                <p class="text-sm text-gray-600">Life Skills Development Monitoring</p>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <Select v-model="selectedTimeRange">
                <SelectTrigger class="w-40">
                  <SelectValue placeholder="Time Range"/>
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7d">Last 7 days</SelectItem>
                  <SelectItem value="30d">Last 30 days</SelectItem>
                  <SelectItem value="90d">Last 3 months</SelectItem>
                  <SelectItem value="1y">Last year</SelectItem>
                </SelectContent>
              </Select>
              <Button @click="exportReports" class="bg-blue-600 hover:bg-blue-700">
                <Download class="w-4 h-4 mr-2"/>
                Export Reports
              </Button>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Overview Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent class="p-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">Total Active Children</p>
                  <p class="text-3xl font-bold text-gray-900">{{ stats.totalChildren }}</p>
                </div>
                <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Users class="w-6 h-6 text-blue-600"/>
                </div>
              </div>
              <div class="mt-4 flex items-center">
                <TrendingUp class="w-4 h-4 text-green-500 mr-1"/>
                <span class="text-sm text-green-600">+12% from last month</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent class="p-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">Average Engagement</p>
                  <p class="text-3xl font-bold text-gray-900">{{ stats.avgEngagement }}%</p>
                </div>
                <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <Activity class="w-6 h-6 text-green-600"/>
                </div>
              </div>
              <div class="mt-4 flex items-center">
                <TrendingUp class="w-4 h-4 text-green-500 mr-1"/>
                <span class="text-sm text-green-600">+5% from last month</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent class="p-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">Skills Completed</p>
                  <p class="text-3xl font-bold text-gray-900">{{ stats.skillsCompleted }}</p>
                </div>
                <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Award class="w-6 h-6 text-purple-600"/>
                </div>
              </div>
              <div class="mt-4 flex items-center">
                <TrendingUp class="w-4 h-4 text-green-500 mr-1"/>
                <span class="text-sm text-green-600">+18% from last month</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent class="p-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">Well-being Score</p>
                  <p class="text-3xl font-bold text-gray-900">{{ stats.wellbeingScore }}</p>
                </div>
                <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                  <Heart class="w-6 h-6 text-orange-600"/>
                </div>
              </div>
              <div class="mt-4 flex items-center">
                <TrendingUp class="w-4 h-4 text-green-500 mr-1"/>
                <span class="text-sm text-green-600">+3% from last month</span>
              </div>
            </CardContent>
          </Card>
        </div>

        <!-- Report Sections -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <!-- Development Progress Chart -->
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center">
                <BarChart3 class="w-5 h-5 mr-2"/>
                Life Skills Development Progress
              </CardTitle>
              <CardDescription>
                Progress across different life skill categories
              </CardDescription>
            </CardHeader>
            <CardContent>
              <DevelopmentChart :data="developmentData"/>
            </CardContent>
          </Card>

          <!-- Engagement Trends -->
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center">
                <TrendingUp class="w-5 h-5 mr-2"/>
                Daily Engagement Trends
              </CardTitle>
              <CardDescription>
                User activity and completion rates over time
              </CardDescription>
            </CardHeader>
            <CardContent>
              <EngagementChart :data="engagementData"/>
            </CardContent>
          </Card>
        </div>

        <!-- Detailed Reports Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Safety & Emergency Preparedness -->
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center">
                <Shield class="w-5 h-5 mr-2"/>
                Safety Preparedness
              </CardTitle>
            </CardHeader>
            <CardContent>
              <SafetyReport :data="safetyData"/>
            </CardContent>
          </Card>

          <!-- Age Group Distribution -->
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center">
                <Users class="w-5 h-5 mr-2"/>
                Age Group Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <AgeDistribution :data="ageData"/>
            </CardContent>
          </Card>

          <!-- Risk Assessment -->
          <Card>
            <CardHeader>
              <CardTitle class="flex items-center">
                <AlertTriangle class="w-5 h-5 mr-2"/>
                Risk Assessment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <RiskAssessment :data="riskData"/>
            </CardContent>
          </Card>
        </div>

        <!-- Detailed Reports Table -->
        <Card class="mt-8">
          <CardHeader>
            <CardTitle class="flex items-center">
              <FileText class="w-5 h-5 mr-2"/>
              Detailed Child Reports
            </CardTitle>
            <CardDescription>
              Individual child progress and well-being indicators
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ChildReportsTable :reports="childReports"/>
          </CardContent>
        </Card>
      </main>
    </OrgDashboardLayout>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue'
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from '@/components/ui/card'
import {Button} from '@/components/ui/button'
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from '@/components/ui/select'
import {
  Users, Download, TrendingUp, Activity, Award, Heart,
  BarChart3, Shield, AlertTriangle, FileText
} from 'lucide-vue-next'

import DevelopmentChart from '@/components/org-dashboard/DevelopmentChart.vue'
import EngagementChart from '@/components/org-dashboard/EngagementChart.vue'
import SafetyReport from '@/components/org-dashboard/SafetyReport.vue'
import AgeDistribution from '@/components/org-dashboard/AgeDistribution.vue'
import RiskAssessment from '@/components/org-dashboard/RiskAssessment.vue'
import ChildReportsTable from '@/components/org-dashboard/ChildReportsTable.vue'
import OrgDashboardLayout from "@/components/partials/OrgDashboardLayout.vue";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList, BreadcrumbPage,
  BreadcrumbSeparator
} from "@/components/ui/breadcrumb";

const selectedTimeRange = ref('30d')

const stats = ref({
  totalChildren: 1247,
  avgEngagement: 78,
  skillsCompleted: 3456,
  wellbeingScore: 8.4
})

const developmentData = ref([
  {skill: 'Time Management', progress: 85, target: 90},
  {skill: 'Emotional Regulation', progress: 72, target: 80},
  {skill: 'Communication', progress: 88, target: 85},
  {skill: 'Financial Literacy', progress: 65, target: 75},
  {skill: 'Health & Hygiene', progress: 92, target: 90},
  {skill: 'Problem Solving', progress: 78, target: 85}
])

const engagementData = ref([
  {date: '2024-01-01', engagement: 65, completions: 45},
  {date: '2024-01-02', engagement: 72, completions: 52},
  {date: '2024-01-03', engagement: 68, completions: 48},
  {date: '2024-01-04', engagement: 78, completions: 58},
  {date: '2024-01-05', engagement: 82, completions: 62},
  {date: '2024-01-06', engagement: 75, completions: 55},
  {date: '2024-01-07', engagement: 80, completions: 60}
])

const safetyData = ref({
  emergencyKnowledge: 78,
  firstAidBasics: 65,
  contactInformation: 92,
  safetyProtocols: 71
})

const ageData = ref([
  {age: '8-9', count: 245, percentage: 19.6},
  {age: '10-11', count: 387, percentage: 31.0},
  {age: '12-13', count: 421, percentage: 33.8},
  {age: '14', count: 194, percentage: 15.6}
])

const riskData = ref({
  lowRisk: 892,
  mediumRisk: 287,
  highRisk: 68,
  criticalRisk: 12
})

const childReports = ref([
  {
    id: 'C001',
    name: 'Emma Johnson',
    age: 10,
    engagement: 85,
    skillsCompleted: 12,
    wellbeingScore: 8.2,
    lastActive: '2024-01-07',
    riskLevel: 'Low'
  },
  {
    id: 'C002',
    name: 'Michael Chen',
    age: 12,
    engagement: 92,
    skillsCompleted: 18,
    wellbeingScore: 9.1,
    lastActive: '2024-01-07',
    riskLevel: 'Low'
  },
  {
    id: 'C003',
    name: 'Sofia Rodriguez',
    age: 9,
    engagement: 67,
    skillsCompleted: 8,
    wellbeingScore: 7.5,
    lastActive: '2024-01-06',
    riskLevel: 'Medium'
  },
  {
    id: 'C004',
    name: 'James Wilson',
    age: 13,
    engagement: 45,
    skillsCompleted: 4,
    wellbeingScore: 6.2,
    lastActive: '2024-01-05',
    riskLevel: 'High'
  }
])

const exportReports = () => {
  // Implementation for exporting reports
  console.log('Exporting reports for time range:', selectedTimeRange.value)
}

onMounted(() => {
  // Load dashboard data
  console.log('Dashboard mounted')
})
</script>
