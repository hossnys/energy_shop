#!/bin/bash

# Edit the default domain with the passed one
sed -i "s/domain = \"gettft.grid.tf\"/domain = \"$domain\"/g" ~/code/tftshop/jumpscale/packages/gettft/package.toml 

# Create a dummy identity to start jsng with Threefold Connect
# Moved to entrypoint to save all data in the mounted volumes and avoid to override
poetry run jsng 'ident=j.core.identity.new("default", "tftshopident5.3bot", "test5@email.com", network="testnet", words="ginger benefit design struggle match chaos erosion minor hen light awkward candy youth mirror cabbage upper three smoke boy animal science net poverty pond"); ident.register(); ident.save()'

# Create wallets not to crash the threebot on startup when checking the identity
poetry run jsng 'j.clients.stellar.new("main",network="STD"); j.clients.stellar.main.save()'
poetry run jsng 'j.clients.stellar.new("test",network="TEST"); j.clients.stellar.test.save()'

# Create the default threebot
poetry run jsng 'j.servers.threebot.new("default"); j.servers.threebot.default.save()'
poetry run jsng "j.servers.threebot.default.packages.add(path='/home/gitpod/code/tftshop/jumpscale/packages/gettft')"

# Start electrum daemon
if [ $network == "testnet" ]; then
    electrum daemon -d --testnet
    stellar_network="TEST"
else
    electrum daemon -d
    stellar_network="STD"
fi

# Configure tftshop mpk and wallet
poetry run jsng 'j.core.config.set("tftshop_mpk", os.environ.get("mpk"))'
poetry run jsng "wallet=j.clients.stellar.get(\"tftshop_wallet\"); wallet.secret=\"$tftshop_wallet_secret\"; wallet.network=\"$stellar_network\"; wallet.save()"
