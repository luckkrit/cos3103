<script setup lang="ts">
interface Props {
    githubUser: string
    repo: string
    branch?: string
    path: string // e.g. "public/เขียนโปรแกรมด้วย pictoblox.pptx"
}

const props = withDefaults(defineProps<Props>(), {
    branch: 'main',
})

const rawUrl = `https://raw.githubusercontent.com/${props.githubUser}/${props.repo}/${props.branch}/${props.path}`
const embedUrl = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(rawUrl)}`
</script>

<template>
    <Teleport to="body">
        <iframe :src="embedUrl" style="position:fixed; inset:0; width:100vw; height:100vh; border:none; z-index:100;" />
    </Teleport>
</template>