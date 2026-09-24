<template>
    <div class="to-table">

        <!-- Error -->
        <div v-if="error" class="error">
            Invalid JSON: {{ error }}
        </div>

        <template v-else>

            <!-- Summary -->
            <div v-if="data" class="summary">

                <!-- Elasticsearch Search -->
                <template v-if="isSearchResponse">

                    <strong>Matched:</strong>
                    {{ data.hits?.total?.value ?? rows.length }}

                    &nbsp; | &nbsp;

                    <strong>Returned:</strong>
                    {{ rows.length }}

                </template>


                <!-- Elasticsearch Single Document -->
                <template v-else-if="isSingleDocumentResponse">

                    <strong>Index:</strong>
                    {{ data._index }}

                    &nbsp; | &nbsp;

                    <strong>Document ID:</strong>
                    {{ data._id }}

                </template>


                <!-- Elasticsearch Mapping -->
                <template v-else-if="isMappingResponse">

                    <strong>Fields:</strong>
                    {{ rows.length }}

                </template>


                <!-- Normal JSON Array -->
                <template v-else>

                    <strong>Rows:</strong>
                    {{ rows.length }}

                </template>


                <!-- Took -->
                <span v-if="data?.took !== undefined">

                    &nbsp; | &nbsp;

                    <strong>Took:</strong>
                    {{ data.took }} ms

                </span>

            </div>


            <!-- =================================================
                 Horizontal scrollbar at TOP
            ================================================== -->

            <div v-if="rows.length" ref="topScroll" class="top-scroll" @scroll="syncFromTop" @wheel.stop>

                <div class="top-scroll-content" :style="{ width: `${tableWidth}px` }"></div>

            </div>


            <!-- =================================================
                 Main Table Viewport
            ================================================== -->

            <div v-if="rows.length" ref="tableScroll" class="table-scroll" :style="{ height: props.height }"
                @scroll="syncFromTable" @wheel.stop @touchmove.stop>

                <table ref="tableElement">

                    <thead>

                        <tr>

                            <th v-for="column in columns" :key="column" :class="{
                                description: isDescriptionColumn(column)
                            }">
                                {{ column }}
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        <tr v-for="(row, index) in rows" :key="index">

                            <td v-for="column in columns" :key="column" :class="{
                                description: isDescriptionColumn(column)
                            }">
                                {{ formatValue(row[column]) }}
                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>


            <!-- Empty -->
            <div v-else class="empty">
                No results
            </div>

        </template>

    </div>
</template>


<script setup>

import {
    computed,
    useSlots,
    ref,
    nextTick,
    onMounted,
    onBeforeUnmount,
    watch
} from 'vue'


/* =========================================================
   1. Props
========================================================= */

const props = defineProps({

    height: {
        type: String,
        default: '320px'
    }

})


/* =========================================================
   2. Slot -> Text
========================================================= */

const slots = useSlots()


function extractText(nodes) {

    let text = ''

    for (const node of nodes ?? []) {

        if (typeof node.children === 'string') {

            text += node.children

        }

        else if (Array.isArray(node.children)) {

            text += extractText(node.children)

        }

    }

    return text

}


const rawText = computed(() => {

    const nodes = slots.default?.() ?? []

    return extractText(nodes).trim()

})


/* =========================================================
   3. Kibana Triple Quote Support

   Kibana may show:

   "description": """hello
   world"""

   This is not standard JSON.

   Convert it to:

   "description": "hello\nworld"
========================================================= */

function normalizeKibanaJson(text) {

    let result = ''

    let i = 0

    let insideString = false

    let escaped = false


    while (i < text.length) {

        const char = text[i]


        /*
         * Inside normal JSON string
         */

        if (insideString) {

            result += char


            if (escaped) {

                escaped = false

            }

            else if (char === '\\') {

                escaped = true

            }

            else if (char === '"') {

                insideString = false

            }


            i++

            continue

        }


        /*
         * Kibana triple quote
         */

        if (
            text[i] === '"' &&
            text[i + 1] === '"' &&
            text[i + 2] === '"'
        ) {

            i += 3


            let content = ''


            while (

                i < text.length &&

                !(
                    text[i] === '"' &&
                    text[i + 1] === '"' &&
                    text[i + 2] === '"'
                )

            ) {

                content += text[i]

                i++

            }


            if (i >= text.length) {

                throw new Error(
                    'Unclosed triple-quoted string'
                )

            }


            result += JSON.stringify(content)


            i += 3

            continue

        }


        /*
         * Start normal JSON string
         */

        if (char === '"') {

            insideString = true

        }


        result += char

        i++

    }


    return result

}


/* =========================================================
   4. Parse JSON
========================================================= */

const parsed = computed(() => {

    /*
     * Try normal JSON first
     */

    try {

        return {

            data: JSON.parse(rawText.value),

            error: null

        }

    }

    catch (originalError) {

        /*
         * Try Kibana format
         */

        try {

            const normalized =
                normalizeKibanaJson(rawText.value)


            return {

                data: JSON.parse(normalized),

                error: null

            }

        }

        catch (e) {

            return {

                data: null,

                error: e.message

            }

        }

    }

})


const data = computed(() => parsed.value.data)

const error = computed(() => parsed.value.error)


/* =========================================================
   5. Detect Elasticsearch _search
========================================================= */

const isSearchResponse = computed(() => {

    return Array.isArray(
        data.value?.hits?.hits
    )

})


/* =========================================================
   6. Detect Elasticsearch Single Document

   GET products/_doc/S10_1678
========================================================= */

const isSingleDocumentResponse = computed(() => {

    return (

        data.value !== null &&

        typeof data.value === 'object' &&

        !Array.isArray(data.value) &&

        data.value.found === true &&

        data.value._source !== null &&

        typeof data.value._source === 'object' &&

        !Array.isArray(data.value._source)

    )

})


/* =========================================================
   7. Detect Elasticsearch Mapping

   GET products
========================================================= */

const isMappingResponse = computed(() => {

    if (

        !data.value ||

        Array.isArray(data.value) ||

        typeof data.value !== 'object'

    ) {

        return false

    }


    return Object.values(data.value).some(

        index =>

            index?.mappings?.properties &&

            typeof index.mappings.properties === 'object'

    )

})


/* =========================================================
   8. Build Rows
========================================================= */

const rows = computed(() => {

    if (!data.value) {

        return []

    }


    /*
     * JSON Array
     *
     * Example:
     * _cat/indices?format=json
     */

    if (Array.isArray(data.value)) {

        return data.value

    }


    /*
     * Elasticsearch _search
     */

    if (isSearchResponse.value) {

        return data.value.hits.hits.map(hit => ({

            _score: hit._score,

            ...hit._source

        }))

    }


    /*
     * Elasticsearch Single Document
     */

    if (isSingleDocumentResponse.value) {

        return [

            {
                ...data.value._source
            }

        ]

    }


    /*
     * Elasticsearch Mapping
     *
     * Show only:
     *
     * Field | Type
     */

    if (isMappingResponse.value) {

        const result = []


        for (
            const index of Object.values(data.value)
        ) {

            const properties =
                index?.mappings?.properties ?? {}


            for (
                const [fieldName, mapping]
                of Object.entries(properties)
            ) {

                result.push({

                    Field: fieldName,

                    Type: mapping?.type ?? ''

                })

            }

        }


        return result

    }


    return []

})


/* =========================================================
   9. Detect Columns
========================================================= */

const columns = computed(() => {

    const names = new Set()


    for (const row of rows.value) {

        if (

            row === null ||

            typeof row !== 'object' ||

            Array.isArray(row)

        ) {

            continue

        }


        for (const key of Object.keys(row)) {

            names.add(key)

        }

    }


    return [...names]

})


/* =========================================================
   10. Description Fields
========================================================= */

function isDescriptionColumn(column) {

    return column
        .toLowerCase()
        .includes('description')

}


/* =========================================================
   11. Format Values
========================================================= */

function formatValue(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return ''

    }


    if (typeof value === 'object') {

        return JSON.stringify(value)

    }


    return value

}


/* =========================================================
   12. Scroll Synchronization
========================================================= */

const topScroll = ref(null)

const tableScroll = ref(null)

const tableElement = ref(null)

const tableWidth = ref(0)


let syncing = false

let resizeObserver = null


/*
 * Measure real table width.
 */

async function updateTableWidth() {

    await nextTick()


    if (!tableElement.value) {

        tableWidth.value = 0

        return

    }


    tableWidth.value =
        tableElement.value.scrollWidth

}


/*
 * Top scrollbar -> table
 */

function syncFromTop() {

    if (syncing) {

        return

    }


    if (
        !topScroll.value ||
        !tableScroll.value
    ) {

        return

    }


    syncing = true


    tableScroll.value.scrollLeft =
        topScroll.value.scrollLeft


    requestAnimationFrame(() => {

        syncing = false

    })

}


/*
 * Table -> top scrollbar
 */

function syncFromTable() {

    if (syncing) {

        return

    }


    if (
        !topScroll.value ||
        !tableScroll.value
    ) {

        return

    }


    syncing = true


    topScroll.value.scrollLeft =
        tableScroll.value.scrollLeft


    requestAnimationFrame(() => {

        syncing = false

    })

}


/* =========================================================
   13. Watch Data Changes
========================================================= */

watch(

    rows,

    () => {

        updateTableWidth()

    },

    {
        deep: true
    }

)


/* =========================================================
   14. Resize Observer

   Important for Slidev:
   preview -> fullscreen -> presenter view
========================================================= */

onMounted(async () => {

    await updateTableWidth()


    if (
        typeof ResizeObserver !== 'undefined'
    ) {

        resizeObserver =
            new ResizeObserver(() => {

                updateTableWidth()

            })


        if (tableElement.value) {

            resizeObserver.observe(
                tableElement.value
            )

        }


        if (tableScroll.value) {

            resizeObserver.observe(
                tableScroll.value
            )

        }

    }

})


onBeforeUnmount(() => {

    if (resizeObserver) {

        resizeObserver.disconnect()

        resizeObserver = null

    }

})

</script>


<style scoped>
/* =========================================================
   Main Component
========================================================= */

.to-table {

    width: 100%;

    max-width: 100%;

    min-width: 0;

    box-sizing: border-box;

    margin: 1rem 0;

}


/* =========================================================
   Summary
========================================================= */

.summary {

    margin-bottom: 8px;

    font-family:
        Arial,
        sans-serif;

    font-size: 14px;

}


/* =========================================================
   TOP Horizontal Scrollbar
========================================================= */

.top-scroll {

    display: block;

    width: 100%;

    height: 18px;

    overflow-x: scroll;

    overflow-y: hidden;

    box-sizing: border-box;

    margin-bottom: 4px;

    scrollbar-gutter: stable;

}


/*
 * Invisible element that creates
 * the scrollbar width.
 */

.top-scroll-content {

    height: 1px;

}


/* =========================================================
   Main Table Scroll Area
========================================================= */

.table-scroll {

    display: block;

    width: 100%;

    max-width: 100%;

    min-width: 0;

    box-sizing: border-box;

    /*
     * Both directions
     */

    overflow-x: auto;

    overflow-y: auto;

    /*
     * Prevent scroll escaping to Slidev
     */

    overscroll-behavior: contain;

    touch-action: pan-x pan-y;

    border: 1px solid #ddd;

    border-radius: 6px;

}


/* =========================================================
   Table

   width:max-content is very important.

   It forces the table to retain its
   real column width instead of shrinking
   into the Slidev viewport.
========================================================= */

table {

    width: max-content !important;

    min-width: 100%;

    table-layout: auto;

    border-collapse: separate;

    border-spacing: 0;

    font-family:
        Arial,
        sans-serif;

    font-size: 14px;

}


/* =========================================================
   Table Cells
========================================================= */

th,
td {

    box-sizing: border-box;

    border-right: 1px solid #ddd;

    border-bottom: 1px solid #ddd;

    padding: 8px 10px;

    text-align: left;

    vertical-align: top;

}


/* =========================================================
   Sticky Header
========================================================= */

th {

    position: sticky;

    top: 0;

    z-index: 10;

    min-width: 140px;

    background: #f5f5f5;

    white-space: nowrap;

    font-weight: bold;

}


/* =========================================================
   Normal Cells

   nowrap ensures columns create horizontal
   width instead of shrinking aggressively.
========================================================= */

td {

    min-width: 140px;

    white-space: nowrap;

}


/* =========================================================
   Description Columns

   Long descriptions wrap inside a fixed width.
========================================================= */

th.description,
td.description {

    width: 300px;

    min-width: 300px;

    max-width: 300px;

}


td.description {

    white-space: normal;

    overflow-wrap: break-word;

    word-break: normal;

}


/* =========================================================
   Hover
========================================================= */

tbody tr:hover {

    background:
        rgba(128, 128, 128, 0.08);

}


/* =========================================================
   Empty
========================================================= */

.empty {

    padding: 15px;

    color: #777;

    font-family:
        Arial,
        sans-serif;

}


/* =========================================================
   Error
========================================================= */

.error {

    padding: 12px;

    border: 1px solid #c00;

    border-radius: 6px;

    color: #c00;

    font-family:
        Arial,
        sans-serif;

}
</style>