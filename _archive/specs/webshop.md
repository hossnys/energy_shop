# webshop for rivine based tokens  using bitcoin

 Payment process using the [BIP-70](https://github.com/bitcoin/bips/blob/master/bip-0070.mediawiki) standard.

## Bitcoin wallets

We do not want to have a private keys on the webshop  server. The server can generate addresses and see the transactions but the bitcoins received should not be spendable.
As such, we have a wallet on a protected machine, export the master public key  and use that one on the webshop server to create a read-only wallet that can generate addresses but does not have the private keys.

If anybody compromise your merchant server, s/he will be able to access read-only version of your wallet only and won’t be able to spent currency.

Please notice that the potential intruder still will be able to see your addresses, transactions and balance, though. It’s also recommended to use a separate wallet for your merchant purposes (and not your main wallet).

Create a wallet on your protected machine, as you want to keep your cryptocurrency safe.

Using the electrum commandline this can be done as follows:

```sh
electrum create
```

Still being on a protected machine, export your Master Public Key (xpub):

Using the electrum commandline this can be done as follows:

```sh
electrum getmpk -w .electrum/wallets/your-wallet
```

Now you are able to set up your electrum merchant daemon.

On the server machine restore your wallet from previously exported Master Public Key (xpub):

Using the electrum commandline this can be done as follows:

```sh
electrum restore xpub...............................................
```

> Make sure we don't use the same address twice at any point

Task: Make this available in the jumpscale btc_electrum client 

## Services

### 1. Webshop frontend webservice 
Serves the webpage, generates unique bitcoin adresses for proposed transactions and stores them together with the amount and the  tft target address  in a.  

### 2. TFT payment service
Uses the stored proposed transactions, monitors the bitcoin chain for payments and transfers the tft to the target adresses. 


 ## references 
 - [BIP-70](https://github.com/bitcoin/bips/blob/master/bip-0070.mediawiki)
 - [Electrum](https://electrum.org/)