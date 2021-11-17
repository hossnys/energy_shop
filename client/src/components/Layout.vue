<template>
  <v-container :fluid="fluid">
    <Logo />
    <slot />
    <Footer />
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

// components
import Logo from "../components/Logo.vue";
import Footer from "../components/Footer.vue";

@Component({
  name: "Layout",
  components: {
    Logo,
    Footer,
  },
})
export default class Layout extends Vue {
  @Prop({ default: false }) fluid!: boolean;
}
</script>
