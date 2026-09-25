<template>
    <div class="to-table">

        <!-- =========================================
             Error
        ========================================= -->

        <div v-if="error" class="error">
            Invalid JSON: {{ error }}
        </div>

        <template v-else>

            <!-- =========================================
                 Summary
            ========================================= -->

            <div v-if="data" class="summary">

                <!-- Aggregation: check BEFORE search -->
                <template v-if="isAggregationResponse">

                    <strong>Aggregation:</strong>
                    {{ aggregationNames.join(', ') }}

                    &nbsp; | &nbsp;

                    <strong>Matched:</strong>
                    {{ data.hits?.total?.value ?? 'N/A' }}

                    &nbsp; | &nbsp;

                    <strong>Buckets:</strong>
                    {{ rows.length }}

                </template>

                <!-- Elasticsearch _search -->
                <template v-else-if="isSearchResponse">

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

                <!-- Normal JSON -->
                <template v-else>

                    <strong>Rows:</strong>
                    {{ rows.length }}

                </template>

                <!-- Query execution time -->
                <span v-if="data?.took !== undefined">

                    &nbsp; | &nbsp;

                    <strong>Took:</strong>
                    {{ data.took }} ms

                </span>

            </div>


            <!-- =========================================
                 TOP Horizontal Scrollbar
            ========================================= -->

            <div v-if="rows.length" ref="topScroll" class="top-scroll" @scroll="syncFromTop" @wheel.stop>

                <div class="top-scroll-content" :style="{
                    width: `${tableWidth}px`
                }"></div>

            </div>


            <!-- =========================================
                 Main Table Viewport
            ========================================= -->

            <div v-if="rows.length" ref="tableScroll" class="table-scroll" :style="{
                height: props.height
            }" @scroll="syncFromTable" @wheel.stop @touchmove.stop>

                <table ref="tableElement">

                    <!-- Header -->
                    <thead>

                        <tr>

                            <th v-for="column in columns" :key="column" :class="{
                                description:
                                    isDescriptionColumn(column)
                            }">
                                {{ column }}
                            </th>

                        </tr>

                    </thead>


                    <!-- Data -->
                    <tbody>

                        <tr v-for="(row, rowIndex) in rows" :key="rowIndex">

                            <td v-for="column in columns" :key="column" :class="{
                                description:
                                    isDescriptionColumn(column)
                            }">

                                <!-- =========================
                                     Elasticsearch Highlight

                                     Highlight appears inside
                                     original field column.
                                ========================= -->

                                <template v-if="hasHighlight(row, column)">

                                    <div v-for="fragment in getHighlightFragments(
                                        row.__highlights[column]
                                    )" :key="fragment.index" class="highlight-fragment">

                                        <span v-for="part in highlightParts(
                                            fragment.text
                                        )" :key="part.start">

                                            <mark v-if="part.highlight">{{ part.text }}</mark>

                                            <span v-else>{{ part.text }}</span>

                                        </span>

                                    </div>

                                </template>


                                <!-- =========================
                                     Normal Value

                                     Works for:
                                     - document fields
                                     - aggregation buckets
                                     - mappings
                                     - JSON arrays
                                ========================= -->

                                <template v-else>

                                    {{ formatValue(row[column]) }}

                                </template>

                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>


            <!-- =========================================
                 Empty Table
            ========================================= -->

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

   Important for Slidev:

   The slot may contain Elasticsearch markup:

   <em>chrome dashboard</em>

   Preserve highlight tags while extracting JSON text.
========================================================= */

const slots = useSlots()


function extractText(nodes) {

    let text = ''


    for (const node of nodes ?? []) {

        let content = ''


        if (typeof node.children === 'string') {

            content = node.children

        }

        else if (Array.isArray(node.children)) {

            content = extractText(node.children)

        }


        /*
         * Preserve Elasticsearch highlight tags.
         */

        if (
            node.type === 'em' ||
            node.type === 'mark'
        ) {

            text +=
                `<${node.type}>${content}</${node.type}>`

        }

        else {

            text += content

        }

    }


    return text

}


const rawText = computed(() => {

    const nodes =
        slots.default?.() ?? []

    return extractText(nodes).trim()

})


/* =========================================================
   3. Kibana Triple Quote Support

   Kibana Console may display:

   "description": """hello
   world"""

   Convert it into valid JSON.
========================================================= */

function normalizeKibanaJson(text) {

    let result = ''

    let i = 0

    let insideString = false

    let escaped = false


    while (i < text.length) {

        const char = text[i]


        /*
         * Inside a normal JSON string.
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
         * Kibana triple-quoted string.
         */

        if (
            text.slice(i, i + 3) === '"""'
        ) {

            i += 3

            let content = ''


            while (

                i < text.length &&

                text.slice(i, i + 3) !== '"""'

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
         * Start a normal JSON string.
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
     * Try standard JSON first.
     */

    try {

        return {

            data: JSON.parse(rawText.value),

            error: null

        }

    }

    catch (originalError) {

        /*
         * Try Kibana triple-quote format.
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


const data = computed(
    () => parsed.value.data
)

const error = computed(
    () => parsed.value.error
)


/* =========================================================
   5. Detect Elasticsearch Aggregations

   Example:

   aggregations: {
       by_productline: {
           buckets: [...]
       }
   }

   Detect aggregation names dynamically.
========================================================= */

const aggregationEntries = computed(() => {

    const aggregations =
        data.value?.aggregations


    if (

        !aggregations ||

        typeof aggregations !== 'object' ||

        Array.isArray(aggregations)

    ) {

        return []

    }


    /*
     * Only bucket aggregations are converted
     * to tables in this version.
     */

    return Object.entries(
        aggregations
    ).filter(

        ([name, aggregation]) =>

            Array.isArray(
                aggregation?.buckets
            )

    )

})


const isAggregationResponse = computed(() => {

    return aggregationEntries.value.length > 0

})


const aggregationNames = computed(() => {

    return aggregationEntries.value.map(

        ([name]) => name

    )

})


/* =========================================================
   6. Detect Elasticsearch _search
========================================================= */

const isSearchResponse = computed(() => {

    return Array.isArray(
        data.value?.hits?.hits
    )

})


/* =========================================================
   7. Detect Elasticsearch Single Document

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
   8. Detect Elasticsearch Mapping

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
   9. Flatten Aggregation Metrics

   Elasticsearch:

   avg_msrp: {
       value: 118.02
   }

   Table:

   avg_msrp = 118.02

   Also supports:
   - sum
   - min
   - max
   - value_count

   Other nested values remain unchanged.
========================================================= */

function flattenAggregationBucket(bucket) {

    const row = {}


    for (
        const [field, value]
        of Object.entries(bucket)
    ) {

        /*
         * Single-value numeric metric.
         */

        if (

            value !== null &&

            typeof value === 'object' &&

            !Array.isArray(value) &&

            Object.prototype.hasOwnProperty.call(
                value,
                'value'
            )

        ) {

            row[field] = value.value

        }

        else {

            row[field] = value

        }

    }


    return row

}


/* =========================================================
   10. Build Rows

   IMPORTANT:

   Aggregations are checked BEFORE search.

   A response can contain:

   hits.hits = []

   AND

   aggregations.by_productline.buckets = [...]

   We want to display aggregation buckets.
========================================================= */

const rows = computed(() => {

    if (!data.value) {

        return []

    }


    /* -------------------------------------
       Case 1: Normal JSON Array

       Example:

       GET _cat/indices?format=json
    ------------------------------------- */

    if (Array.isArray(data.value)) {

        return data.value

    }


    /* -------------------------------------
       Case 2: Elasticsearch Aggregations

       Check BEFORE _search.
    ------------------------------------- */

    if (isAggregationResponse.value) {

        const result = []


        const multipleAggregations =
            aggregationEntries.value.length > 1


        for (
            const [aggregationName, aggregation]
            of aggregationEntries.value
        ) {

            for (
                const bucket of aggregation.buckets
            ) {

                const row =
                    flattenAggregationBucket(bucket)


                /*
                 * Multiple aggregations:

                 * Add a column identifying
                 * the aggregation source.
                 */

                if (multipleAggregations) {

                    result.push({

                        _aggregation:
                            aggregationName,

                        ...row

                    })

                }

                else {

                    result.push(row)

                }

            }

        }


        return result

    }


    /* -------------------------------------
       Case 3: Elasticsearch _search

       Preserve highlight data internally.

       Do NOT create extra highlight columns.
    ------------------------------------- */

    if (isSearchResponse.value) {

        return data.value.hits.hits.map(

            hit => ({

                _score: hit._score,

                ...hit._source,

                /*
                 * Internal highlight metadata.
                 */

                __highlights:
                    hit.highlight ?? {}

            })

        )

    }


    /* -------------------------------------
       Case 4: Single Document
    ------------------------------------- */

    if (isSingleDocumentResponse.value) {

        return [

            {
                ...data.value._source
            }

        ]

    }


    /* -------------------------------------
       Case 5: Elasticsearch Mapping

       Field | Type
    ------------------------------------- */

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
   11. Detect Columns

   Collect all field names across rows.

   Hide __highlights metadata.
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

            /*
             * Internal highlight metadata
             * is not a visible column.
             */

            if (key === '__highlights') {

                continue

            }


            names.add(key)

        }

    }


    return [...names]

})


/* =========================================================
   12. Description Fields
========================================================= */

function isDescriptionColumn(column) {

    return column
        .toLowerCase()
        .includes('description')

}


/* =========================================================
   13. Detect Highlight for Current Cell

   If Elasticsearch returns:

   highlight: {
       productdescription: [...]
   }

   Render highlighted text in the existing
   productdescription column.
========================================================= */

function hasHighlight(row, column) {

    const fragments =
        row?.__highlights?.[column]


    if (Array.isArray(fragments)) {

        return fragments.length > 0

    }


    return (

        typeof fragments === 'string' &&

        fragments.length > 0

    )

}


/* =========================================================
   14. Get Highlight Fragments

   Returns:

   [
       {
           index: 0,
           text: "Text with <em>highlight</em>"
       }
   ]

   An index is used as the Vue key.
========================================================= */

function getHighlightFragments(value) {

    if (Array.isArray(value)) {

        return value.map(

            (fragment, index) => ({

                index,

                text: String(fragment)

            })

        )

    }


    if (typeof value === 'string') {

        return [

            {
                index: 0,
                text: value
            }

        ]

    }


    return []

}


/* =========================================================
   15. Parse Elasticsearch Highlight Markup

   Input:

   "This has <em>chrome dashboard</em>."

   Output:

   [
       {
           start: 0,
           text: "This has ",
           highlight: false
       },
       {
           start: 9,
           text: "chrome dashboard",
           highlight: true
       },
       {
           start: 34,
           text: ".",
           highlight: false
       }
   ]

   Supports:
   <em>...</em>
   <mark>...</mark>

   No v-html is needed.
========================================================= */

function highlightParts(fragment) {

    const result = []

    const regex =
        /<(em|mark)>([\s\S]*?)<\/\1>/gi

    let lastIndex = 0

    let match


    while (
        (match = regex.exec(fragment)) !== null
    ) {

        /*
         * Text before highlighted section.
         */

        if (match.index > lastIndex) {

            result.push({

                start: lastIndex,

                text: fragment.slice(
                    lastIndex,
                    match.index
                ),

                highlight: false

            })

        }


        /*
         * Highlighted text.
         */

        result.push({

            start: match.index,

            text: match[2],

            highlight: true

        })


        lastIndex = regex.lastIndex

    }


    /*
     * Text after the last highlight.
     */

    if (lastIndex < fragment.length) {

        result.push({

            start: lastIndex,

            text: fragment.slice(lastIndex),

            highlight: false

        })

    }


    /*
     * Fallback for empty strings.
     */

    if (result.length === 0) {

        result.push({

            start: 0,

            text: fragment,

            highlight: false

        })

    }


    return result

}


/* =========================================================
   16. Format Normal Values

   Numbers remain numbers.

   Objects and arrays are converted to
   readable JSON text.
========================================================= */

function formatValue(value) {

    if (
        value === null
    ) {

        return 'null'

    }

    if (
        value === undefined
    ) {

        return 'undefined'

    }


    if (typeof value === 'object') {

        return JSON.stringify(value)

    }


    return value

}


/* =========================================================
   17. Scroll References
========================================================= */

const topScroll = ref(null)

const tableScroll = ref(null)

const tableElement = ref(null)

const tableWidth = ref(0)


let syncing = false

let resizeObserver = null


/* =========================================================
   18. Measure Table Width
========================================================= */

async function updateTableWidth() {

    await nextTick()


    if (!tableElement.value) {

        tableWidth.value = 0

        return

    }


    const width =
        tableElement.value.scrollWidth


    if (tableWidth.value !== width) {

        tableWidth.value = width

    }

}


/* =========================================================
   19. TOP Scrollbar -> Table
========================================================= */

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


/* =========================================================
   20. Table -> TOP Scrollbar
========================================================= */

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
   21. Resize Observer Setup
========================================================= */

function observeTable() {

    if (!resizeObserver) {

        return

    }


    resizeObserver.disconnect()


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


/* =========================================================
   22. Watch Table Data Changes

   Supports changing JSON between:

   - _search
   - aggregation
   - mapping
   - normal array
========================================================= */

watch(

    rows,

    async () => {

        await updateTableWidth()

        observeTable()

    },

    {
        deep: true,
        flush: 'post'
    }

)


/* =========================================================
   23. Mounted

   Important for Slidev:

   - Preview
   - Fullscreen
   - Presenter view
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


        observeTable()

    }

})


/* =========================================================
   24. Cleanup
========================================================= */

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

    overflow-x: auto;

    overflow-y: auto;

    overscroll-behavior: contain;

    touch-action: pan-x pan-y;

    border: 1px solid #ddd;

    border-radius: 6px;

}


/* =========================================================
   Table
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
========================================================= */

td {

    min-width: 140px;

    white-space: nowrap;

}


/* =========================================================
   Description Columns
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
   Highlight Fragments
========================================================= */

.highlight-fragment {

    margin-bottom: 6px;

    white-space: pre-wrap;

    line-height: 1.5;

}


.highlight-fragment:last-child {

    margin-bottom: 0;

}


/* =========================================================
   Highlight Text

   Only matching text is highlighted.

   Table headers remain unchanged.
========================================================= */

mark {

    background: #fde047;

    color: #111827;

    font-weight: bold;

    padding: 1px 2px;

    border-radius: 2px;

}


/* =========================================================
   Row Hover
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