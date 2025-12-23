<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
const preEl = ref(null)
const rawText = ref('')

onMounted(async () => {
    await nextTick()
    if (preEl.value) {
        // ใช้ textContent แทน innerHTML เพื่อไม่เอา HTML tags
        rawText.value = preEl.value.textContent || ''
        console.log('Raw:', JSON.stringify(rawText.value))
    }
})

watch(preEl, async (newVal) => {
    await nextTick()
    if (newVal) {
        rawText.value = newVal.textContent || ''
    }
})

const parsedData = computed(() => {
    if (!rawText.value) return []

    // แยกบรรทัด
    const lines = rawText.value.split('\n')

    // // ลบบรรทัดว่างท้ายสุด
    while (lines.length > 2 && lines[lines.length - 1] === '') {
        lines.pop()
    }

    if (lines.length === 0) return []

    const sep = lines[0].includes('\t') ? '\t' : ','

    return lines.map(line => {
        if (line === '') {
            return ['NULL']
        }

        const cells = line.split(sep)
        return cells.map(cell => {
            const cleaned = cell.replace(/^"|"$/g, '')
            return cleaned === '' ? 'NULL' : cleaned
        })
    })
})

const headers = computed(() => parsedData.value[0] || [])
const rows = computed(() => parsedData.value.slice(1) || [])
const cols = computed(() => headers.value.length)
</script>
<template>
    <pre ref="preEl" style="display: none;"><slot /></pre>
    <div class="my-2">
        <div v-if="cols > 0" class="border border-gray-400 overflow-hidden text-[0.625rem]"
            style="display: grid; gap: 0;" :style="{ gridTemplateColumns: `repeat(${cols}, 1fr)` }">
            <!-- Headers -->
            <div v-for="(h, i) in headers" :key="'h' + i"
                class="bg-gray-300 text-gray-800 font-semibold border-r border-b border-gray-400 text-center px-2 py-1 truncate"
                :title="h">
                {{ h }}
            </div>
            <!-- Rows -->
            <template v-for="(row, i) in rows" :key="'r'+i">
                <div v-for="(cell, j) in row" :key="'c' + j"
                    class="border-r border-b border-gray-300 px-2 py-1 truncate"
                    :class="i % 2 === 0 ? 'bg-white' : 'bg-gray-100'" :title="cell">
                    {{ cell }}
                </div>
            </template>
        </div>
        <div v-else class="text-red-500 text-[0.625rem]">No data</div>
    </div>
</template>