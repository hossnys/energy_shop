<template>
  <v-app class="main-app">
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import axios from "axios";
import { Component, Vue } from "vue-property-decorator";
import Logo from "./components/Logo.vue";

import VTooltip from "v-tooltip";
Vue.use(VTooltip);

@Component({
  name: "App",
  components: {
    Logo,
  },
})
export default class App extends Vue {
  private _readPrice(x: any): number {
    const z = Object.values(x["data"]["result"]) as any;
    return +z[0]["a"][0];
  }

  created() {
    const coins = ["BTCUSD", "XLMUSD"];
    const priceUrl = "https://threefoldfoundation.github.io/tft-price/tftprice.json"; // prettier-ignore
    axios
      .get<{ btc: number }>(priceUrl)
      .then(({ data }) => {
        this.$store.dispatch("SetTftRatio", data);
        return axios.get("/gettft/prices/date/");
      })
      .then(({ data }) => {
        this.$store.dispatch("SetDate", data.date);
        return Promise.all(
          coins.map((c) =>
            axios.get(`https://api.kraken.com/0/public/Ticker?pair=${c}`)
          )
        );
      })
      .then(([btc, xlm]: any) => {
        this.$store.dispatch("SetUsd", {
          btc: this._readPrice(btc),
          xlm: this._readPrice(xlm),
        });
      });
  }
}
</script>

<style lang="scss">
// .main-app {
//   background-color: #103073 !important;
//   color: white !important;
// }

.tooltip {
  display: block !important;
  z-index: 10000;
}

.tooltip .tooltip-inner {
  background: black;
  color: white;
  border-radius: 16px;
  padding: 5px 10px 4px;
}

.tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: black;
  z-index: 1;
}

.tooltip[x-placement^="top"] {
  margin-bottom: 5px;
}

.tooltip[x-placement^="top"] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="bottom"] {
  margin-top: 5px;
}

.tooltip[x-placement^="bottom"] .tooltip-arrow {
  border-width: 0 5px 5px 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
  top: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="right"] {
  margin-left: 5px;
}

.tooltip[x-placement^="right"] .tooltip-arrow {
  border-width: 5px 5px 5px 0;
  border-left-color: transparent !important;
  border-top-color: transparent !important;
  border-bottom-color: transparent !important;
  left: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip[x-placement^="left"] {
  margin-right: 5px;
}

.tooltip[x-placement^="left"] .tooltip-arrow {
  border-width: 5px 0 5px 5px;
  border-top-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  right: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip.popover .popover-inner {
  background: #f9f9f9;
  color: black;
  padding: 24px;
  border-radius: 5px;
  box-shadow: 0 5px 30px rgba(black, 0.1);
}

.tooltip.popover .popover-arrow {
  border-color: #f9f9f9;
}

.tooltip[aria-hidden="true"] {
  visibility: hidden;
  opacity: 0;
  transition: opacity 0.15s, visibility 0.15s;
}

.tooltip[aria-hidden="false"] {
  visibility: visible;
  opacity: 1;
  transition: opacity 0.15s;
}
</style>
