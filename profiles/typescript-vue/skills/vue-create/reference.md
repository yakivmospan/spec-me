# Vue — reference

Examples for `SKILL.md`. Names are placeholders for the project's own; the layout is Feature-Sliced
Design — elsewhere, the same files go where the project keeps its own.

## Template — a new page

A page, the composable it calls, one component below it, and their tests.

```
entities/item/
├── model/types.ts           Item
├── model/useItems.ts        loads items; state, loading, error
├── ui/ItemRow.vue           one row: props in, event out
└── index.ts                 the slice's public API
pages/items/
├── ui/ItemsPage.vue         wires the composable to the components
└── index.ts
```

`entities/item/model/useItems.ts`

```ts
import { onScopeDispose, ref, shallowRef } from 'vue'
import type { Item } from './types'

export function useItems(load: (signal: AbortSignal) => Promise<Item[]>) {
  const items = shallowRef<Item[]>([])
  const loading = ref(false)
  const failed = ref(false)
  let controller: AbortController | undefined

  async function refresh() {
    controller?.abort()
    const current = new AbortController()
    controller = current
    loading.value = true
    failed.value = false
    try {
      items.value = await load(current.signal)
    } catch {
      failed.value = !current.signal.aborted
    } finally {
      if (controller === current) loading.value = false
    }
  }

  onScopeDispose(() => controller?.abort())
  return { items, loading, failed, refresh }
}
```

`entities/item/ui/ItemRow.vue`

```vue
<script setup lang="ts">
import type { Item } from '../model/types'

const { item, selected = false } = defineProps<{ item: Item; selected?: boolean }>()
const emit = defineEmits<{ select: [id: string] }>()
</script>

<template>
  <li class="row">
    <button type="button" :aria-pressed="selected" @click="emit('select', item.id)">
      {{ item.title }}
    </button>
  </li>
</template>

<style scoped>
.row button {
  min-block-size: 2.75rem;
}
</style>
```

`entities/item/index.ts`

```ts
export type { Item } from './model/types'
export { useItems } from './model/useItems'
export { default as ItemRow } from './ui/ItemRow.vue'
```

`pages/items/ui/ItemsPage.vue`

```vue
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ItemRow, useItems } from '@/entities/item'
import { fetchItems } from '@/shared/api' // the project's own client

const { items, loading, failed, refresh } = useItems(fetchItems)
const selectedId = ref<string>()
const isEmpty = computed(() => !loading.value && !failed.value && items.value.length === 0)

function select(id: string) {
  selectedId.value = id
}

onMounted(refresh)
</script>

<template>
  <main>
    <h1 tabindex="-1">Items</h1>
    <p role="status">
      <template v-if="loading">Loading…</template>
      <template v-else-if="isEmpty">Nothing here yet.</template>
    </p>
    <p v-if="failed">
      Couldn't load the items.
      <button type="button" @click="refresh">Try again</button>
    </p>
    <ul v-else>
      <ItemRow
        v-for="item in items"
        :key="item.id"
        :item="item"
        :selected="item.id === selectedId"
        @select="select"
      />
    </ul>
  </main>
</template>
```

`pages/items/index.ts`, and the route — lazy:

```ts
export { default as ItemsPage } from './ui/ItemsPage.vue'

// router: { path: '/items', component: () => import('@/pages/items').then((page) => page.ItemsPage) }
```

`entities/item/ui/__tests__/ItemRow.spec.ts` — in the project's test location:

```ts
import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import ItemRow from '../ItemRow.vue'

describe('ItemRow', () => {
  it('emits select with the item id when pressed', async () => {
    const wrapper = mount(ItemRow, { props: { item: { id: '7', title: 'Seven' } } })

    await wrapper.get('button').trigger('click')

    expect(wrapper.emitted('select')).toEqual([['7']])
  })
})
```

`entities/item/model/__tests__/useItems.spec.ts` — a composable using a lifecycle hook runs inside an
effect scope:

```ts
import { effectScope } from 'vue'
import { describe, expect, it } from 'vitest'
import { useItems } from '../useItems'

describe('useItems', () => {
  it('flags a failed load', async () => {
    const scope = effectScope()
    const state = scope.run(() => useItems(() => Promise.reject(new Error('offline'))))!

    await state.refresh()

    expect(state.failed.value).toBe(true)
    scope.stop()
  })
})
```

## Non-obvious accessibility

```ts
// Move focus to the new page's heading after each navigation (in the router setup).
router.afterEach(async () => {
  await nextTick()
  document.querySelector<HTMLElement>('main h1')?.focus()
})
```

```vue
<!-- A modal dialog: showModal() traps focus; closing returns it to the opener. -->
<script setup lang="ts">
import { useTemplateRef, watch } from 'vue'

const open = defineModel<boolean>('open', { required: true })
const dialog = useTemplateRef('dialog')
let opener: HTMLElement | null = null

watch(open, (isOpen) => {
  if (isOpen) {
    opener = document.activeElement as HTMLElement | null
    dialog.value?.showModal()
  } else {
    dialog.value?.close()
    opener?.focus()
  }
})
</script>

<template>
  <dialog ref="dialog" aria-labelledby="dialog-title" @close="open = false">
    <h2 id="dialog-title"><slot name="title" /></h2>
    <slot />
  </dialog>
</template>
```

```vue
<!-- A field error: in text, tied to the field, announced. -->
<label for="email">Email</label>
<input
  id="email"
  v-model="email"
  type="email"
  :aria-invalid="emailError ? 'true' : undefined"
  aria-describedby="email-error"
/>
<p id="email-error" role="alert">{{ emailError }}</p>
```
