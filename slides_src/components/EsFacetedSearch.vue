<template>
    <div class="es-faceted-search">

        <!-- =========================================
             Error
        ========================================= -->

        <div v-if="error" class="error">
            Invalid JSON: {{ error }}
        </div>

        <template v-else-if="data">

            <!-- =========================================
                 Title
            ========================================= -->

            <div class="page-header">

                <h3>Faceted Search</h3>

                <div class="page-info">

                    <strong>Matched:</strong>
                    {{ totalMatched }}

                    &nbsp; | &nbsp;

                    <strong>Returned:</strong>
                    {{ returnedCount }}

                    <template v-if="data.took !== undefined">

                        &nbsp; | &nbsp;

                        <strong>Took:</strong>
                        {{ data.took }} ms

                    </template>

                </div>

            </div>


            <!-- =========================================
                 Horizontal Layout
            ========================================= -->

            <div class="faceted-layout">

                <!-- =====================================
                     LEFT: Facets
                ===================================== -->

                <aside class="facets" :style="{
                    maxHeight: props.height
                }">

                    <h4 class="sidebar-title">
                        Filters
                    </h4>


                    <!-- Each Aggregation -->

                    <section v-for="facet in facets" :key="facet.name" class="facet-group">

                        <h5 class="facet-title">

                            {{ facet.title }}

                        </h5>


                        <!-- Buckets -->

                        <div v-for="(bucket, index)
                            in facet.buckets" :key="index" class="facet-item">

                            <!-- Bucket Label -->

                            <span class="facet-label">

                                {{ formatBucketLabel(
                                    facet,
                                    bucket
                                ) }}

                            </span>


                            <!-- Document Count -->

                            <span class="facet-count">

                                {{ bucket.doc_count ?? 0 }}

                            </span>

                        </div>


                        <!-- Empty Aggregation -->

                        <div v-if="facet.buckets.length === 0" class="facet-empty">

                            No buckets

                        </div>

                    </section>


                    <!-- No Facets -->

                    <div v-if="facets.length === 0" class="facet-empty">

                        No bucket aggregations

                    </div>

                </aside>


                <!-- =====================================
                     RIGHT: Search Results
                ===================================== -->

                <main class="results">

                    <h4 class="results-title">
                        Search Results
                    </h4>


                    <!-- =================================
                         Reuse Existing ToTable.vue

                         IMPORTANT:

                         We remove aggregations from
                         the data passed to ToTable.

                         Otherwise ToTable would detect
                         aggregations first and display
                         buckets instead of documents.
                    ================================= -->

                    <ToTable v-if="hasSearchResponse" :height="props.height">{{ searchResponseJson }}</ToTable>


                    <!-- No hits.hits -->

                    <div v-else class="empty-results">

                        This response does not contain
                        search hits.

                    </div>

                </main>

            </div>

        </template>

    </div>
</template>


<script setup>

import {
    computed,
    useSlots
} from 'vue'

import ToTable from './EsTable.vue'


/* =========================================================
   1. Props
========================================================= */

const props = defineProps({

    height: {
        type: String,
        default: '350px'
    }

})


/* =========================================================
   2. Extract JSON from Slidev Slot

   Usage:

   <EsFacetedSearch>
   {
       "hits": { ... },
       "aggregations": { ... }
   }
   </EsFacetedSearch>

   Preserve <em> and <mark> tags when Slidev
   interprets them as HTML elements.
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

            content = extractText(
                node.children
            )

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

   Example:

   "description": """Long
   multiline description"""

   This is not valid standard JSON.

   Convert it into a JSON string.
========================================================= */

function normalizeKibanaJson(text) {

    let result = ''

    let i = 0

    let insideString = false

    let escaped = false


    while (i < text.length) {

        const char = text[i]


        /*
         * Inside normal JSON string.
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
         * Kibana triple quote.
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
         * Start normal JSON string.
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

   Standard JSON first.

   If parsing fails, attempt Kibana format.
========================================================= */

const parsed = computed(() => {

    try {

        return {

            data: JSON.parse(
                rawText.value
            ),

            error: null

        }

    }

    catch (originalError) {

        try {

            const normalized =
                normalizeKibanaJson(
                    rawText.value
                )


            return {

                data: JSON.parse(
                    normalized
                ),

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


const data = computed(() => {

    return parsed.value.data

})


const error = computed(() => {

    return parsed.value.error

})


/* =========================================================
   5. Search Statistics
========================================================= */

const hasSearchResponse = computed(() => {

    return Array.isArray(
        data.value?.hits?.hits
    )

})


const returnedCount = computed(() => {

    return (
        data.value?.hits?.hits?.length ?? 0
    )

})


const totalMatched = computed(() => {

    const total =
        data.value?.hits?.total


    if (typeof total === 'number') {

        return total

    }


    if (
        total &&
        typeof total.value === 'number'
    ) {

        /*
         * relation: gte means the value
         * is a lower bound.
         */

        if (total.relation === 'gte') {

            return `${total.value}+`

        }


        return total.value

    }


    return 'N/A'

})


/* =========================================================
   6. Extract Facets from Aggregations

   Input:

   aggregations: {

       by_productline: {
           buckets: [...]
       },

       price_ranges: {
           buckets: [...]
       }

   }

   Output:

   [
       {
           name: "by_productline",
           title: "Product Line",
           buckets: [...]
       },

       {
           name: "price_ranges",
           title: "Price Range",
           buckets: [...]
       }
   ]
========================================================= */

const facets = computed(() => {

    const aggregations =
        data.value?.aggregations ?? {}


    return Object.entries(
        aggregations
    )

        /*
         * Only bucket aggregations.
         */

        .filter(

            ([name, aggregation]) =>

                Array.isArray(
                    aggregation?.buckets
                )

        )

        /*
         * Convert to sidebar model.
         */

        .map(

            ([name, aggregation]) => ({

                name,

                title: formatFacetTitle(
                    name
                ),

                buckets:
                    aggregation.buckets

            })

        )

})


/* =========================================================
   7. Format Facet Titles

   by_productline -> Product Line

   price_ranges -> Price Range

   by_vendor -> Vendor

   by_country -> Country
========================================================= */

function formatFacetTitle(name) {

    /*
     * Friendly names for the
     * Classic Models example.
     */

    const titleMap = {

        by_productline:
            'Product Line',

        price_ranges:
            'Price Range',

        by_vendor:
            'Vendor',

        by_country:
            'Country',

        by_productvendor:
            'Product Vendor'

    }


    if (titleMap[name]) {

        return titleMap[name]

    }


    /*
     * Generic fallback:

     * by_customer_city

     * becomes:

     * Customer City
     */

    return name

        .replace(/^by_/, '')

        .replace(/_/g, ' ')

        .replace(/\b\w/g, char =>

            char.toUpperCase()

        )

}


/* =========================================================
   8. Format Numbers for Price Ranges
========================================================= */

function formatNumber(value) {

    if (typeof value !== 'number') {

        return String(value)

    }


    return new Intl.NumberFormat(
        'en-US',
        {
            maximumFractionDigits: 2
        }
    ).format(value)

}


/* =========================================================
   9. Detect Whether a Facet is Price-Related
========================================================= */

function isPriceFacet(facet) {

    return /price|msrp|cost/i.test(
        facet.name
    )

}


/* =========================================================
   10. Format Bucket Labels

   Terms aggregation:

   "Vintage Cars"
       -> Vintage Cars

   Range aggregation:

   {
       "key": "*-70.0",
       "to": 70
   }

       -> Below $70

   {
       "from": 70,
       "to": 120
   }

       -> $70 to below $120

   {
       "from": 120
   }

       -> $120 and above
========================================================= */

function formatBucketLabel(facet, bucket) {

    const from = bucket.from

    const to = bucket.to


    const hasFrom = (
        from !== undefined &&
        from !== null
    )


    const hasTo = (
        to !== undefined &&
        to !== null
    )


    /*
     * Terms bucket:
     *
     * No from/to range.
     */

    if (!hasFrom && !hasTo) {

        return String(
            bucket.key_as_string ??
            bucket.key ??
            ''
        )

    }


    /*
     * Use $ for price-related facets.
     */

    const prefix =
        isPriceFacet(facet) ? '$' : ''


    /*
     * Example:
     *
     * *-70.0
     *
     * Below $70
     */

    if (!hasFrom && hasTo) {

        return (
            `Below ${prefix}` +
            formatNumber(to)
        )

    }


    /*
     * Example:
     *
     * 120.0-*
     *
     * $120 and above
     */

    if (hasFrom && !hasTo) {

        return (
            `${prefix}` +
            formatNumber(from) +
            ' and above'
        )

    }


    /*
     * Example:
     *
     * 70.0-120.0
     *
     * $70 to below $120
     *
     * Elasticsearch range aggregation:
     *
     * from inclusive
     * to exclusive
     */

    return (

        `${prefix}` +

        formatNumber(from) +

        ` to below ${prefix}` +

        formatNumber(to)

    )

}


/* =========================================================
   11. Build Search-Only JSON for ToTable.vue

   Original response:

   {
       took: 3,

       hits: {
           hits: [...]
       },

       aggregations: {
           by_productline: {...},
           price_ranges: {...}
       }
   }

   ToTable receives:

   {
       took: 3,

       hits: {
           hits: [...]
       }
   }

   This is important because the existing
   ToTable detects aggregations BEFORE search.
========================================================= */

const searchResponseJson = computed(() => {

    if (
        !data.value ||
        !hasSearchResponse.value
    ) {

        return ''

    }


    /*
     * Separate aggregations from the
     * Elasticsearch response.
     *
     * Do not mutate the original data.
     */

    const {
        aggregations,
        ...searchResponse
    } = data.value


    return JSON.stringify(
        searchResponse
    )

})

</script>


<style scoped>
/* =========================================================
   Main Component
========================================================= */

.es-faceted-search {

    width: 100%;

    max-width: 100%;

    min-width: 0;

    box-sizing: border-box;

    font-family:
        Arial,
        sans-serif;

}


/* =========================================================
   Header
========================================================= */

.page-header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    flex-wrap: wrap;

    gap: 8px;

    margin-bottom: 12px;

}


.page-header h3 {

    margin: 0;

    font-size: 20px;

    font-weight: bold;

}


.page-info {

    font-size: 13px;

    color: #64748b;

}


/* =========================================================
   Horizontal Layout

   LEFT: 220px
   RIGHT: remaining width

   minmax(0, 1fr) is important because
   ToTable contains a very wide table.
========================================================= */

.faceted-layout {

    display: grid;

    grid-template-columns:
        220px minmax(0, 1fr);

    gap: 14px;

    width: 100%;

    min-width: 0;

    align-items: start;

}


/* =========================================================
   LEFT: Facets
========================================================= */

.facets {

    min-width: 0;

    box-sizing: border-box;

    overflow-y: auto;

    overflow-x: hidden;

    padding: 12px;

    border: 1px solid #ddd;

    border-radius: 6px;

    overscroll-behavior: contain;

}


/* =========================================================
   Sidebar Title
========================================================= */

.sidebar-title {

    margin: 0 0 12px 0;

    padding-bottom: 8px;

    font-size: 16px;

    font-weight: bold;

    border-bottom: 1px solid #ddd;

}


/* =========================================================
   Facet Group
========================================================= */

.facet-group {

    margin-bottom: 16px;

}


.facet-group:last-child {

    margin-bottom: 0;

}


/* =========================================================
   Facet Title
========================================================= */

.facet-title {

    margin: 0 0 8px 0;

    font-size: 14px;

    font-weight: bold;

}


/* =========================================================
   Facet Item
========================================================= */

.facet-item {

    display: flex;

    align-items: flex-start;

    justify-content: space-between;

    gap: 8px;

    padding: 5px 0;

    font-size: 13px;

}


/* =========================================================
   Bucket Label
========================================================= */

.facet-label {

    min-width: 0;

    flex: 1;

    line-height: 1.4;

    overflow-wrap: break-word;

}


/* =========================================================
   Bucket Count
========================================================= */

.facet-count {

    flex-shrink: 0;

    min-width: 24px;

    padding: 2px 7px;

    border-radius: 12px;

    background: #e5e7eb;

    color: #111827;

    font-size: 12px;

    font-weight: bold;

    text-align: center;

}


/* =========================================================
   RIGHT: Results
========================================================= */

.results {

    width: 100%;

    min-width: 0;

    max-width: 100%;

    overflow: hidden;

    box-sizing: border-box;

}


/* =========================================================
   Search Results Title
========================================================= */

.results-title {

    margin: 0 0 8px 0;

    font-size: 16px;

    font-weight: bold;

}


/* =========================================================
   Existing ToTable Component

   Prevent it from expanding the
   parent grid beyond the slide width.
========================================================= */

.results :deep(.to-table) {

    width: 100%;

    max-width: 100%;

    min-width: 0;

    margin: 0;

}


/* =========================================================
   Empty Facets
========================================================= */

.facet-empty {

    padding: 8px 0;

    font-size: 13px;

    color: #777;

}


/* =========================================================
   Empty Results
========================================================= */

.empty-results {

    padding: 15px;

    color: #777;

    border: 1px solid #ddd;

    border-radius: 6px;

}


/* =========================================================
   Error
========================================================= */

.error {

    padding: 12px;

    border: 1px solid #c00;

    border-radius: 6px;

    color: #c00;

}


/* =========================================================
   Responsive Layout

   On a narrow viewport, stack
   facets above results.
========================================================= */

@media (max-width: 650px) {

    .faceted-layout {

        grid-template-columns:
            minmax(0, 1fr);

    }


    .facets {

        max-height: 200px !important;

    }

}
</style>