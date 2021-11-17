<template>
  <div>
    <v-container v-if="!canceled">
      <div v-if="md" v-html="md"></div>
      <v-row v-if="md" justify="end" class="mt-8 mb-16">
        <v-btn
          color="primary"
          class="mr-4"
          @click="onAccept"
          :disabled="loading"
          :loading="loading"
          >Accept</v-btn
        >
        <v-btn color="error" @click="canceled = true">Cancel</v-btn>
      </v-row>
      <v-row v-if="!md" justify="center">
        <v-progress-circular indeterminate class="mt-16"></v-progress-circular>
      </v-row>
    </v-container>

    <v-container v-if="canceled">
      <p class="text-h3 mt-16" style="text-align: center">
        Sorry can't process without accepting our terms and conditions.
      </p>
      <v-row justify="center" class="mt-16">
        <v-btn @click="canceled = false" color="primary" x-large>Back</v-btn>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import axios from "axios";
import marked from "marked";
import { api } from "@/plugins/axios";

@Component({
  name: "Terms",
})
export default class Terms extends Vue {
  public md = "";
  public canceled = false;
  loading = false;

  async created() {
    try {
      const md = await axios.get(
        "https://raw.githubusercontent.com/threefoldfoundation/info_legal/development/wiki/terms_conditions_gettft.md"
      );

      marked.use({
        renderer: {
          heading(txt) {
            return `<h1 class="text-h2 mb-10 mt-16">${txt}</h1>`;
          },
          link(href, _, txt) {
            return `<a
                        href="${href}"
                        target="_blank"
                        class="text-decoration-none">
                          ${txt}
                        </a>`;
          },
          list(body) {
            return `<ul style="list-style: square;">${body}</ul>`;
          },
        },
      });
      this.md = marked.parse(md.data);
    } catch (err) {
      console.log("Error", err);
    }
  }

  onAccept() {
    this.loading = true;

    /* call /api/accept */
    api
      .get("/accept")
      .then(() => {
        this.$router.push("/buy");
      })
      .catch((err) => {
        console.log("Error", err);
      })
      .finally(() => {
        this.loading = false;
      });
  }
}
</script>
