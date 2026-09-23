<template>
    <div class="to-table">
        <div v-if="error" class="error">
            Invalid JSON: {{ error }}
        </div>

        <template v-else>
            <div class="summary" v-if="data">
                <strong>Matched:</strong>
                {{ data.hits?.total?.value ?? rows.length }}

                <span>
                    &nbsp; | &nbsp;
                    <strong>Returned:</strong> {{ rows.length }}
                </span>

                <span v-if="data.took !== undefined">
                    &nbsp; | &nbsp;
                    <strong>Took:</strong> {{ data.took }} ms
                </span>
            </div>

            <div v-if="rows.length" class="table-scroll">
                <table>
                    <thead>
                        <tr>
                            <th v-for="column in columns" :key="column">
                                {{ column }}
                            </th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="(row, index) in rows" :key="row._id ?? index">
                            <td v-for="column in columns" :key="column">
                                {{ formatValue(row[column]) }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div v-else>
                No results
            </div>
        </template>
    </div>
</template>

<script setup>
import { computed, useSlots } from 'vue'

const slots = useSlots()

/*
 * Extract text from default slot
 */
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

/*
 * Kibana Console may show multiline strings like:
 *
 * "description": """line 1
 * line 2"""
 *
 * Convert them to valid JSON strings.
 */
function normalizeKibanaJson(text) {
    let result = ''
    let i = 0

    while (i < text.length) {
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
                throw new Error('Unclosed triple-quoted string')
            }

            result += JSON.stringify(content)

            i += 3
        }
        else {
            result += text[i]
            i++
        }
    }

    return result
}

const rawText = computed(() => {
    const nodes = slots.default?.() ?? []

    return extractText(nodes).trim()
})

const parsed = computed(() => {
    try {
        const normalized = normalizeKibanaJson(rawText.value)

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
})

const data = computed(() => parsed.value.data)

const error = computed(() => parsed.value.error)

/*
 * Convert Elasticsearch hits to flat rows
 */
const rows = computed(() => {
    const hits = data.value?.hits?.hits ?? []

    return hits.map(hit => ({
        _score: hit._score,
        ...hit._source
    }))
})

/*
 * Detect all columns automatically
 */
const columns = computed(() => {
    const names = new Set()

    for (const row of rows.value) {
        for (const key of Object.keys(row)) {
            names.add(key)
        }
    }

    return [...names]
})

function formatValue(value) {
    if (value === null || value === undefined) {
        return ''
    }

    if (typeof value === 'object') {
        return JSON.stringify(value)
    }

    return value
}
</script>

<style scoped>
.to-table {
    width: 100%;
    margin: 1rem 0;
}

.summary {
    margin-bottom: 10px;
    font-family: Arial, sans-serif;
    font-size: 14px;
}

/*
 * Scrollable table container
 */
.table-scroll {
    width: 100%;

    height: 75vh;
    height: 75dvh;

    overflow-x: auto;
    overflow-y: auto;

    border: 1px solid #ddd;
}

/*
 * Make table wider than container when necessary
 */
table {
    width: max-content;
    min-width: 100%;

    border-collapse: collapse;

    font-family: Arial, sans-serif;
    font-size: 14px;
}

th,
td {
    border: 1px solid #ddd;

    padding: 8px 10px;

    text-align: left;
    vertical-align: top;
}

/*
 * Keep header visible while scrolling vertically
 */
th {
    position: sticky;
    top: 0;

    z-index: 2;

    background: #f5f5f5;

    white-space: nowrap;
}

/*
 * Prevent very long columns such as
 * productdescription from becoming too wide
 */
td {
    min-width: 100px;
    max-width: 350px;

    white-space: normal;
    overflow-wrap: break-word;
    word-break: break-word;
}

tbody tr:hover {
    background: #fafafa;
}

.error {
    padding: 10px;

    border: 1px solid #c00;

    color: #c00;

    font-family: Arial, sans-serif;
}
</style>