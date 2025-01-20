<script setup lang="ts">
import { ref, watch } from 'vue'
import { useGLTF } from '@tresjs/cientos'
import { useRenderLoop } from '@tresjs/core'
import { shallowRef } from 'vue'

const props = defineProps([
  'model_url',
])
const { scene: model } = await useGLTF(
  props.model_url
)

const pieceref = shallowRef();

</script>

<template>
  <primitive ref="pieceref" :object="model" :key="model" />
</template>