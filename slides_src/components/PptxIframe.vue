<script setup lang="ts">
interface Props {
    githubUser: string
    repo: string
    branch?: string
    path: string // e.g. "public/เขียนโปรแกรมด้วย pictoblox.pptx"
    width?: string
    height?: string
}

const props = withDefaults(defineProps<Props>(), {
    branch: 'main',
    width: '100%',
    height: '500px',
})

const rawUrl = `https://raw.githubusercontent.com/${props.githubUser}/${props.repo}/${props.branch}/${props.path}`

const embedUrl = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(rawUrl)}`
</script>

<template>
    <iframe :src="embedUrl" :width="width" :height="height" frameborder="0" class="pptx-preview" />
</template>

<style scoped>
.pptx-preview {
    border: 1px solid #ddd;
    border-radius: 8px;
}
</style>