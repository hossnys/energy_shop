<template>
  <Layout>
    <p class="text-h4" style="margin-top: 200px;">
      <span class="font-weight-bold">404 </span>
      <span class="font-weight-thin">- Page Not Found</span>
    </p>
    <p class="text-h6">
      We are working hard to get this page in as soon as possible.
    </p>
  </Layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

// components
import Layout from "../components/Layout.vue";

@Component({
  name: "PageNotFound",
  components: { Layout },
})
export default class PageNotFound extends Vue {}
</script>
