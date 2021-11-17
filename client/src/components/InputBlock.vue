<template>
  <div>
    <label class="mb-2 font-weight-bold" style="display: block;" v-if="label">
      {{ label }}
    </label>
    <slot />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({
  name: "InputBlock",
})
export default class InputBlock extends Vue {
  @Prop() label?: string;
}
</script>
