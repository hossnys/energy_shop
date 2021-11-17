<template>
  <Layout :fluid="true">
    <v-container>
      <img src="../assets/tftvalue.png" alt="tftvalue" width="100%" />

      <v-alert type="info">
        1 TFT =
        {{
          (
            +$store.getters.usd[form.amount.coin.toLowerCase()] /
            +$store.getters.tftRatio[form.amount.coin.toLowerCase()]
          ).toFixed(9)
        }}
        USD =
        {{
          (
            1 / +$store.getters.tftRatio[form.amount.coin.toLowerCase()]
          ).toFixed(9)
        }}
        {{ form.amount.coin }} <br />
        These prices will be valid till {{ $store.getters.date }} 16:00 CET.
      </v-alert>

      <form @submit.prevent="onSubmitHandler">
        <InputBlock label="I would like to buy">
          <v-text-field
            label="Amount"
            solo
            type="number"
            suffix="TFT"
            persistent-hint
            v-model="tft"
          ></v-text-field>

          <v-alert
            type="error"
            v-if="isNaN(+tft) || +tft < 100 || tft.includes('.')"
          >
            Minimum value is 100 <b>TFT</b>, must not include decimals.
          </v-alert>
        </InputBlock>

        <InputBlock label="This costs">
          <AmountInput
            :value="form.amount.value"
            v-on:coin-changed="onCoinUpdated"
          />
        </InputBlock>

        <InputBlock label="Your TFT Wallet Address to receive TFTs at">
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-bind="attrs"
                v-on="on"
                label="Your TFT Wallet Address"
                solo
                type="text"
                v-model="form.address"
              ></v-text-field>
            </template>
            <span>
              Stellar wallet address, You can copy it from ThreeFold Connect
              Application.
            </span>
          </v-tooltip>
        </InputBlock>

        <v-alert v-if="error" type="error">
          {{ error }}
        </v-alert>

        <v-row class="ml-1" align="center">
          <v-checkbox v-model="agreed" color="primary"> </v-checkbox>
          <label>
            I agree to
            <a
              href="https://library.threefold.me/info/legal/#/legal__terms_conditions_gettft"
              target="_blank"
              class="text-decoration-none"
              >Terms of Service</a
            >.
          </label>
        </v-row>

        <v-btn
          x-large
          color="#00cd75"
          type="submit"
          :loading="loading"
          :disabled="
            !form.address ||
            isNaN(+tft) ||
            +tft < 100 ||
            (+tft).toFixed(0) !== tft ||
            !agreed
          "
        >
          GENERATE QR CODE
        </v-btn>
      </form>
    </v-container>
  </Layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import { Decimal } from "decimal.js";
import { api } from "@/plugins/axios";

// components
import Layout from "../components/Layout.vue";
import InputBlock from "../components/InputBlock.vue";
import AmountInput from "../components/SwapForm/AmountInput.vue";

@Component({
  name: "SwapFrom",
  components: {
    Layout,
    InputBlock,
    AmountInput,
  },
})
export default class SwapForm extends Vue {
  form = {
    amount: {
      value: 0.00001,
      coin: "BTC",
    },
    address: this.$store.getters.tft,
  };
  loading = false;
  error: string | null = null;
  tft = "100";
  agreed = false;

  private fixStringNumber(val: string): string {
    if (val.includes("e+")) {
      const [amount, times] = val.split("e+");
      return amount + "0".repeat(+times);
    }

    if (val.includes("e-")) {
      return parseFloat(val).toFixed(+val.split("e-")[1]);
    }

    return val;
  }

  async created() {
    const { data } = await api.get<{ tft_address: string }>("/address");
    this.form.address = data.tft_address;
  }

  onCoinUpdated(coin: string) {
    this.form.amount.coin = coin;
    this.tftWatcher(this.tft);
  }

  @Watch("tft", { immediate: true, deep: true })
  tftWatcher(val: string) {
    const coin = this.form.amount.coin.toLowerCase();
    const ratio = this.$store.getters.tftRatio[coin];
    if (val === "" || isNaN(+val)) {
      val = "0";
    }

    const amount = new Decimal(val).div(ratio).toFixed(8).toString();
    this.form.amount.value = this.fixStringNumber(amount) as any;
  }

  onSubmitHandler() {
    const { address } = this.form;
    this.error = null;
    this.loading = true;
    let amount = this.tft;
    api
      .post("/payment", { address, amount })
      .then(() => this._onSubmitHandler())
      .catch((error) => {
        this.error = error.response.data.message;
      })
      .finally(() => {
        this.loading = false;
      });
  }

  private _onSubmitHandler() {
    const { amount: { value: amount, coin }, address } = this.form; // prettier-ignore
    this.$store.dispatch("SwapData", {
      amount,
      coin,
      address,
    });

    this.$router.push("/payment");
  }
}
</script>

<style lang="scss" scoped>
/* Start TFT */
.tft-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.tft-container > div {
  width: 20%;
  padding: 0 15px;
  margin-top: 25px;
}

.tft-container > div > div {
  text-align: center;
}

.tft-container > div > div img {
  width: 100px;
  margin-bottom: 10px;
}

.tft-container > div > div h3 {
  font-size: 20px;
  font-weight: bold;
}

.tft-container > div > div > p {
  margin-bottom: 10px;
  font-weight: 500;
  font-size: 16px;
}

.tft-container > div > div hr {
  border-color: white;
  margin-bottom: 15px;
}

.tft-container > div > div > p:last-of-type span {
  font-weight: bold;
  display: block;
}

@media (max-width: 1300px) {
  .tft-container > div {
    width: 25%;
  }
}

@media (max-width: 1100px) {
  .tft-container > div {
    width: calc(100% / 3);
  }
}

@media (max-width: 850px) {
  .tft-container > div {
    width: 50%;
  }
}

@media (max-width: 570px) {
  .tft-container > div {
    width: 100%;
  }
}
</style>
