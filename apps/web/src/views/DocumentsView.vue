<template>
  <div class="p-6">
    <div class="mx-auto max-w-5xl">
      <DocumentUpload class="mb-8" />
      <DocumentList />
    </div>
  </div>
</template>

<script setup lang="ts">
import DocumentUpload from "@/components/documents/DocumentUpload.vue";
import DocumentList from "@/components/documents/DocumentList.vue";
</script>
