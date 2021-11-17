<template>
  <Layout v-if="swapdata">
    <InputBlock label="Please send amount of:">
      <v-text-field
        solo
        :value="swapdata.amount"
        disabled
        :suffix="swapdata.coin"
      ></v-text-field>
    </InputBlock>

    <InputBlock label="To this address:">
      <div class="address">
        <v-text-field solo :value="address" disabled></v-text-field>
        <span class="address__icon">
          <v-btn icon color="#103073" @click="copy(address)">
            <v-icon>
              mdi-content-copy
            </v-icon>
          </v-btn>
        </span>
      </div>
      <v-snackbar v-model="snackbar">
        Copied!
      </v-snackbar>
    </InputBlock>

    <InputBlock label="With Memo Text:" v-if="swapdata.coin === 'XLM'">
      <div class="address">
        <v-text-field solo :value="memoText" disabled></v-text-field>
        <span class="address__icon">
          <v-btn icon color="#103073" @click="copy(memoText)">
            <v-icon>
              mdi-content-copy
            </v-icon>
          </v-btn>
        </span>
      </div>
      <v-alert type="warning">
        * Make sure to add this field in your transaction or your coins will be
        lost.
      </v-alert>

      <v-snackbar v-model="snackbar">
        Copied!
      </v-snackbar>
    </InputBlock>

    <InputBlock
      label="Or scan the QR Code with your mobile wallet"
      v-if="!error"
    >
      <v-row justify="center">
        <img :src="qrcode" alt="qrcode" v-if="qrcode" />
      </v-row>

      <v-alert type="info" class="mt-8">
        It will take at most 15 mins to process your request. Feel free to reach
        out using the live chat.
      </v-alert>
    </InputBlock>

    <v-alert v-if="error" type="error">
      Failed to generate QRCODE !
    </v-alert>
  </Layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import QRCode from "qrcode";

// components
import Layout from "../components/Layout.vue";
import InputBlock from "../components/InputBlock.vue";
import { ISwapData } from "@/store";
import { getCoinName } from "@/utils/getCoinName";
import { api } from "@/plugins/axios";

interface IAddresses {
  btc_address: string;
  xlm_address: string;
  memo_text: string;
}

@Component({
  name: "PayForm",
  components: {
    Layout,
    InputBlock,
  },
})
export default class PayForm extends Vue {
  swapdata: ISwapData = this.$store.getters.swapdata;
  address = "";
  snackbar = false;
  qrcode: string | null = null;
  error = false;
  memoText = "";

  copy(text: string) {
    const inp = document.createElement("input");
    inp.value = text;
    document.body.append(inp);
    inp.select();
    document.execCommand("copy");
    inp.remove();

    this.snackbar = true;
  }

  async created() {
    try {
      const { data } = await api.get<IAddresses>("/address");
      const { amount, coin } = this.swapdata;
      const { btc_address, xlm_address, memo_text } = data;

      this.address = coin === "BTC" ? btc_address : xlm_address;
      this.memoText = memo_text;

      let code = `${getCoinName(coin)}:${this.address}?amount=${amount}`;
      if (coin === "XLM") {
        code += `&memo_text=${memo_text}`;
      }
      this.qrcode = await QRCode.toDataURL(code);
    } catch (err) {
      console.log("Error", err);
      return this.$router.push("/");
    }
  }
}
</script>

<style lang="scss" scoped>
.address {
  position: relative;

  &__icon {
    position: absolute;
    top: 6px;
    right: 15px;
  }
}
</style>
