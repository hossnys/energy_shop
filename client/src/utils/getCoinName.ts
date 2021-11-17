const COINS: any = {
  BTC: "bitcoin",
  XLM: "xlm",
};

export function getCoinName(symbol: string): string {
  return COINS[symbol];
}
