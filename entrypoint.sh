#!/bin/bash

# Create dirs for electrum and jsmodel if not created, create links for them in the volume
mkdir -p /root/.config/jumpscale/secureconfig/jumpscale/packages
mkdir -p /data/jsngmodel && ln -s /data/jsngmodel ~/.config/jumpscale/secureconfig/jumpscale/packages/gettft
mkdir -p /data/electrum && ln -s /data/electrum ~/.electrum

# Edit the default domain with the passed one
sed -i "s/domain = \"gettft.grid.tf\"/domain = \"$domain\"/g" /code/tftshop/jumpscale/packages/gettft/package.toml 

# Create a dummy identity to start jsng with Threefold Connect
# Moved to entrypoint to save all data in the mounted volumes and avoid to override
poetry run jsng 'ident=j.core.identity.new("default", "tftshopident5.3bot", "test5@email.com", network="testnet", words="ginger benefit design struggle match chaos erosion minor hen light awkward candy youth mirror cabbage upper three smoke boy animal science net poverty pond"); ident.register(); ident.save()'

# Create wallets not to crash the threebot on startup when checking the identity
poetry run jsng 'j.clients.stellar.new("main",network="STD"); j.clients.stellar.main.save()'
poetry run jsng 'j.clients.stellar.new("test",network="TEST"); j.clients.stellar.test.save()'

# Create the default threebot
poetry run jsng 'j.servers.threebot.new("default"); j.servers.threebot.default.save()'
poetry run jsng "j.servers.threebot.default.packages.add(path='/code/tftshop/jumpscale/packages/gettft')"

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

# Configure restic client for backup
echo "checking env variables for backup was set correctly "
disable_backup=0
for var in repo_url backup_password AWS_ACCESS_KEY_ID AWS_ACCESS_KEY_ID
    do
        if [ -z "${!var}" ]
        then
            echo "Backup won't be working because $var not set, Please set it in creating your container"
            disable_backup=1
        fi
    done

if [ $disable_backup == 0 ]; then
    poetry run jsng "j.tools.restic.get(\"systembackupclient\", repo=\"$repo_url\", password=\"$backup_password\", extra_env={\"AWS_ACCESS_KEY_ID\": \"$AWS_ACCESS_KEY_ID\", \"AWS_SECRET_ACCESS_KEY\": \"$AWS_ACCESS_KEY_ID\"})"
fi

# Set email server config
poetry run jsng "email_server_config = {\"host\": "$email_host", \"port\": "$email_port", \"username\": "$email_username", \"password\": "$email_password"}; j.core.config.set(\"EMAIL_SERVER_CONFIG\", email_server_config)"


# Start threebot server without certificate as kubernetes manages it
poetry run threebot start --no-cert
