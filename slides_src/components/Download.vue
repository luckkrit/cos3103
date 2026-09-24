<template>
    <a :href="fileUrl" :download="downloadName">
        <slot>Download {{ downloadName }}</slot>
    </a>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    file: {
        type: String,
        required: true
    },
    filename: {
        type: String,
        default: ''
    }
})

const fileUrl = computed(() =>
    `${import.meta.env.BASE_URL}${props.file.replace(/^\/+/, '')}`
)

const downloadName = computed(() =>
    props.filename || props.file.split('/').pop()
)
</script>