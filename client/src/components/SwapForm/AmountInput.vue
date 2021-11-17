<template>
  <v-container>
    <v-row>
      <v-text-field
        label="Amount"
        solo
        type="float"
        class="coin-amount"
        :value="value"
        disabled
      ></v-text-field>
      <div style="width: 110px">
        <v-select
          solo
          class="coin-select"
          v-model="coin"
          :items="coins"
          label="Coin"
          @change="$emit('coin-changed', coin)"
        >
          <template v-slot:selection="{ item }">
            <img
              :src="require('@/assets/coins/' + item.icon)"
              alt="coin logo"
              width="30"
            />
          </template>
          <template v-slot:item="{ item }">
            <img
              :src="require('@/assets/coins/' + item.icon)"
              alt="coin logo"
              width="30"
            />
            <v-spacer /> {{ item.value }}
          </template>
        </v-select>
      </div>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component({
  name: "AmountInput",
})
export default class AmountInput extends Vue {
  @Prop({ required: true }) value!: string;
  coin = "BTC";

  coins = [
    {
      value: "BTC",
      icon: "btc.svg",
    },
    // {
    //   value: "XLM",
    //   icon: "xlm.svg",
    // },
  ];
}
</script>

<style lang="scss">
.coin-amount .v-input__control {
  .v-input__slot {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }
}

.coin-select .v-input__control {
  .v-input__slot {
    background-color: #eef0f5 !important;
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
  }
}
</style>
