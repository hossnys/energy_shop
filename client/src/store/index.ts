import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export interface ISwapData {
  amount: number;
  coin: "BTC" | "XLM";
  address: string;
  email: string;
}

export interface IState {
  swapdata: ISwapData | null;
  btcAddress: string;
  tftRatio: {
    btc: number;
    xlm: number;
  };
  usd: {
    btc: number;
    xlm: number;
  };
  date: string;
}

export default new Vuex.Store<IState>({
  state: {
    swapdata: null,
    btcAddress: "",
    tftRatio: {
      btc: 0,
      xlm: 0,
    },
    usd: {
      btc: 0,
      xlm: 0,
    },
    date: "",
  },
  getters: {
    tftRatio: (start) => start.tftRatio,
    swapdata: (state) => state.swapdata,
    usd: (start) => start.usd,
    date: (start) => start.date,
  },
  mutations: {},
  actions: {
    SwapData({ state }, payload: ISwapData) {
      payload.amount = +payload.amount;
      state.swapdata = payload;
    },
    SetTftRatio({ state }, payload: IState["tftRatio"]) {
      state.tftRatio = payload;
    },
    SetUsd({ state }, payload: any) {
      state.usd = payload;
    },
    SetDate({ state }, payload: string) {
      state.date = payload;
    },
  },
  modules: {},
});
