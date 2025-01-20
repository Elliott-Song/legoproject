<script setup>
import { ref } from 'vue'

const statusText = ref('Upload an image');
const file = ref(null);
const fileUrl = ref(null);
const prediction_primary = ref(null);
const prediction_secondary = ref(null);

function validFileCheck() {
  if (!file.value) {
    console.log('No file selected');
    statusText.value = 'No file selected';
    return false;
  }
  if (file.value.size > 21 * 1024 * 1024) {
    console.log('File is too large, must be less than 10MB');
    statusText.value = 'File is too large';
    return false;
  }
  if (!['image/png', 'image/jpeg', 'image/gif'].includes(file.value.type)) {
    console.log('File is not an image');
    statusText.value = 'File is not an image';
    return false;
  }
  return true;
}

function uploadFile(e) {
  e.preventDefault()
  // if the user drags a file into the dropzone, use that file
  if (e.dataTransfer) {
    file.value = e.dataTransfer.files[0];
  }
  // if the user clicks the dropzone, use the file they select
  else {
    file.value = e.target.files[0];
  }
  if (!validFileCheck()) return;
  console.log('File ' + file.value.name + ' is valid');
  statusText.value = 'File ' + file.value.name + ' is valid';
  fileUrl.value = URL.createObjectURL(file.value);
  submitFile();
}

function submitFile() {
  console.log('Submitting file ' + file.value.name);
  statusText.value = 'Submitting file ' + file.value.name;
  const formData = new FormData();
  formData.append('file', file.value);
  fetch('https://coral-app-58aam.ondigitalocean.app/predict', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      statusText.value = 'Success';
      light_color.value = '#00ff70';
      if (data.predictions) {
        prediction_primary.value = data.predictions[0];
        model_url.value = data.predictions[0].label + '.gltf';
        if (data.predictions[1].probability > 5.0) {
          prediction_secondary.value = data.predictions[1];
        }
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      statusText.value = 'Error: ' + error;
    });
}

function deleteFile() {
  file.value = null;
  fileUrl.value = null;
  statusText.value = 'Upload an image';
  light_color.value = '#000000';
  
  prediction_primary.value = null;
  prediction_secondary.value = null;
}

import { TresCanvas, useRenderLoop } from '@tresjs/core';
import { GLTFModel } from '@tresjs/cientos';
import { shallowRef } from 'vue';
import Piece from './components/Piece.vue';
import { onMounted } from 'vue';

const all_piece_urls = ['Plate1x1(3024)', 'Plate1x10(4477)', 'Plate1x12(60479)', 'Plate1x2(3023)', 'Plate1x3(3623)', 'Plate1x4(3710)', 'Plate1x5(78329)', 'Plate1x6(3666)', 'Plate1x8(3460)', 'Plate2x10(3832)', 'Plate2x12(2445)', 'Plate2x14(91988)', 'Plate2x16(4282)', 'Plate2x2(3022)', 'Plate2x2Corner(2420)', 'Plate2x3(3021)', 'Plate2x4(3020)', 'Plate2x6(3795)', 'Plate2x8(3034)', 'Plate3x3(11212)', 'Plate3x3Corner(77844)', 'Plate4x10(3030)', 'Plate4x12(3029)', 'Plate4x4(3031)', 'Plate4x4Corner(2639)', 'Plate4x6(3032)', 'Plate4x8(3035)', 'Plate6x10(3033)', 'Plate6x12(3028)', 'Plate6x14(3456)', 'Plate6x16(3027)', 'Plate6x24(3026)', 'Plate6x6(3958)', 'Plate6x8(3036)', 'Plate8x16(92438)', 'Plate8x8(42534)']
const model_url = ref('Plate1x1(3024).gltf')
const light_color = ref('#000000')

// every 1 second change the piece
onMounted(() => {
  setInterval(() => {
    if (prediction_primary.value) return;
    model_url.value = all_piece_urls[Math.floor(Math.random() * all_piece_urls.length)] + '.gltf';
  }, 1000)
})

const groupRef = shallowRef();
const { onLoop } = useRenderLoop();
onLoop(({ delta }) => {
  groupRef.value.rotation.y += delta;
});

</script>

<template>
  <div class="h-screen flex flex-col items-center justify-center">
    <div class="w-full h-48">
      <TresCanvas>
        <TresPerspectiveCamera :position="[3, 1, 3]" :look-at="[0, 0, 0]" />
        <TresGroup ref="groupRef">
          <Suspense>
            <Piece ref="pieceref" scale="0.05" :model_url="model_url" :key="model_url" />
          </Suspense>
        </TresGroup>

        <TresDirectionalLight cast-shadow :position="[0, 2, 1]" :intensity="5" :color="light_color" :key="light_color"/>
      </TresCanvas>
    </div>
    <h1 class="text-5xl font-bold">
      LEGO Piece Identifier
    </h1>
    <div class="text-lg mt-2">
      {{ statusText }}
    </div>
    <div v-if="!file" class="mt-2 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
      <div class="flex flex-col justify-center space-y-1 text-center">
        <label for="file-upload"
          class="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
          <span>browse files</span>
          <input id="file-upload" name="file-upload" type="file" class="sr-only" @change="uploadFile" />
        </label>
        <p class="">or</p>
        <p class="">drag and drop</p>
        <p class="text-xs text-gray-500">
          PNG, JPG, GIF up to 20MB
        </p>
      </div>
    </div>
    <div v-else="file" class="mt-2 w-64 h-64 bg-cover rounded text-right"
      :style="{ backgroundImage: 'url(' + fileUrl + ')' }">
      <button @click="deleteFile" class="mt-2 ml-2 text-white bg-black rounded-full flex items-center justify-center">
        Remove
      </button>
    </div>
    <div v-if="prediction_primary" class="mt-4 text-center">
      <div v-if="prediction_primary.probability < 45.0" class="mt-2">
        Are you sure this is a LEGO piece?
      </div>
      <h2 class="text-xl">Your piece is:</h2>
      <h1 class="text-2xl font-bold text-green-500">{{ prediction_primary.label }}</h1>
      <div v-if="prediction_secondary" class="mt-2">
        <h2 class="text-xl">Or it could be:</h2>
        <h1 class="text-2xl font-bold">{{ prediction_secondary.label }}</h1>
      </div>
      
    </div>
  </div>

</template>
