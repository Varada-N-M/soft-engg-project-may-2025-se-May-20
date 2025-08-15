<script setup lang="ts" generic="T extends Record<string, any>">
import type { BaseChartProps } from "."
import { Donut } from "@unovis/ts"
import { VisDonut, VisSingleContainer, VisTooltip } from "@unovis/vue"
import { useMounted } from "@vueuse/core"
import { type Component, computed, ref, createApp } from "vue"
import { cn } from "@/lib/utils"
import { ChartLegend, ChartTooltip, defaultColors } from '@/components/ui/chart'

const props = withDefaults(defineProps<Pick<BaseChartProps<T>, "data" | "colors" | "index" | "margin" | "showLegend" | "showTooltip" | "filterOpacity"> & {
  /**
   * Sets the name of the key containing the quantitative chart values.
   */
  category: KeyOfT
  /**
   * Change the type of the chart
   * @default "donut"
   */
  type?: "donut" | "pie"
  /**
   * Function to sort the segment
   */
  sortFunction?: (a: any, b: any) => number | undefined
  /**
   * Controls the formatting for the label.
   */
  valueFormatter?: (tick: number, i?: number, ticks?: number[]) => string
  /**
   * Render custom tooltip component.
   */
  customTooltip?: Component
}>(), {
  margin: () => ({ top: 0, bottom: 0, left: 0, right: 0 }),
  sortFunction: () => undefined,
  type: "donut",
  filterOpacity: 0.2,
  showTooltip: true,
  showLegend: true,
})

type KeyOfT = Extract<keyof T, string>
type Data = typeof props.data[number]

const valueFormatter = props.valueFormatter ?? ((tick: number) => `${tick}`)
const category = computed(() => props.category as KeyOfT)
const index = computed(() => props.index as KeyOfT)

const isMounted = useMounted()
const activeSegmentKey = ref<string>()
const colors = computed(() => props.colors?.length ? props.colors : defaultColors(props.data.filter(d => d[props.category]).filter(Boolean).length))
const legendItems = ref(props.data.map((item, i) => ({
  name: item[props.index],
  color: colors.value[i],
  inactive: false,
  hidden: false,
})))

const totalValue = computed(() => props.data.reduce((prev, curr) => {
  return prev + curr[props.category]
}, 0))

// Use weakmap to store reference to each datapoint for Tooltip
const wm = new WeakMap()

// Styled tooltip template function
function createStyledTooltip(d: any, i: number, elements: (HTMLElement | SVGElement)[]) {
  if (!d?.data) return null
  
  const data = d.data
  if (wm.has(data)) {
    return wm.get(data)
  }
  
  const style = getComputedStyle(elements[i])
  const tooltipData = [{
    name: data[props.index],
    value: valueFormatter(data[props.category]),
    color: style.fill || colors.value[i] || '#000'
  }]
  
  const componentDiv = document.createElement('div')
  const TooltipComponent = props.customTooltip ?? ChartTooltip
  createApp(TooltipComponent, { 
    data: tooltipData 
  }).mount(componentDiv)
  
  wm.set(data, componentDiv.innerHTML)
  return componentDiv.innerHTML
}

// Tooltip triggers for proper @unovis implementation with styling
const tooltipTriggers = computed(() => ({
  [Donut.selectors.segment]: createStyledTooltip
}))

function handleLegendItemClick() {
  // Legend click handling - for future interactivity
}
</script>

<template>
  <div :class="cn('w-full h-48 flex flex-col', $attrs.class ?? '')">
    <VisSingleContainer :style="{ height: isMounted ? '100%' : 'auto' }" :margin="{ left: 20, right: 20 }" :data="data">
      <VisTooltip
          v-if="showTooltip"
          :horizontal-shift="20"
          :vertical-shift="20"
          :triggers="tooltipTriggers"
      />

      <VisDonut
          :value="(d: Data) => d[category]"
          :sort-function="sortFunction"
          :color="colors"
          :arc-width="type === 'donut' ? 20 : 0"
          :show-background="false"
          :central-label="type === 'donut' ? valueFormatter(totalValue) : ''"
          :events="{
          [Donut.selectors.segment]: {
            click: (d: Data, ev: PointerEvent, i: number, elements: HTMLElement[]) => {
              if (d?.data?.[index] === activeSegmentKey) {
                activeSegmentKey = undefined
                elements.forEach(el => el.style.opacity = '1')
              }
              else {
                activeSegmentKey = d?.data?.[index]
                elements.forEach(el => el.style.opacity = `${filterOpacity}`)
                elements[i].style.opacity = '1'
              }
            },
          },
        }"
      />

      <slot />
    </VisSingleContainer>

    <ChartLegend
        v-if="showLegend"
        v-model:items="legendItems"
        @legend-item-click.prevent="handleLegendItemClick"
        class="mt-3 justify-center"
    />
  </div>
</template>
