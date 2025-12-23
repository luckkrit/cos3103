<script setup lang="ts">
const props = defineProps({
    steps: {
        default: ['FROM', 'JOIN', 'WHERE', 'GROUP BY', 'HAVING', 'SELECT', 'ORDER BY'],
    },
})
</script>

<template>
    <div class="w-screen flex gap-1">
        <div :key="i" v-for="s, i of props.steps"
            class="arrow-step w-[150px] h-[50px] flex items-center justify-start pl-6 text-white font-semibold text-xs text-center px-2">
            {{ (i + 1) + ". " + s }}
        </div>
    </div>

</template>
<style>
.arrow-step {
    background-image: url('/images/sql_select/arrow_shape_svg.svg');
    background-size: 150px 50px;
    background-position: left center;
    background-repeat: no-repeat;
}
</style>