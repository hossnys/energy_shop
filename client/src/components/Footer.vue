<template>
  <div class="text-center" style="margin-top: 200px">
    <p class="mb-0 text-h5">
      <a
        class="text-decoration-none"
        target="_blank"
        href="https://library.threefold.me/info/legal/#/legal__terms_conditions_gettft"
        >Terms of Service</a
      >
    </p>
    <p class="mb-0 font-weight-thin text-h6">&copy; ThreeFold 2021</p>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  name: "Footer",
})
export default class Footer extends Vue {}
</script>
