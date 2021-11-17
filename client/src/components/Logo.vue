<template>
  <v-row align="center" justify="center" class="mt-16 mb-6">
    <img src="../assets/logo.png" height="100" alt="logo" />
    <p class="text-h1 mb-0" style="line-height: initial">
      <span class="font-weight-bold">&nbsp;GET</span>
      TFT
    </p>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "Logo",
})
export default class Logo extends Vue {}
</script>
