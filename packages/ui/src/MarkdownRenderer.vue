<template>
  <div class="prose prose-sm max-w-none" v-html="rendered" />
</template>

<script setup lang="ts">
import { computed } from "vue";
import { marked } from "marked";

const props = defineProps<{
  content: string;
}>();

const rendered = computed(() => {
  return marked.parse(props.content, { breaks: true });
});
</script>
