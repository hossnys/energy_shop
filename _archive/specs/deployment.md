# Deployment of TFT webshop

Should be managed by zerorobot templates

## Setup
2 machines zero-os machines as specified in [Webshop](webshop.md) 

### Protected machine
Machine has the master private key 

### Webshop machine
Machine has master public key with to generate address with the readonly wallet

## Required templates
- ProtectedMachine template `protectedmachine`: 
    Responsible for provisioning machine with electrum and creating wallet.
- WebshopMachine template `webshopmachine`:
    - Responsible for provisioning machine
    - Lua requirements in case of no flist available.
    - Hosting the readonly wallet (using the master public key from the protected machine)
    - Setup SSL for the site
- AlertaMachine template `alertamachine`
    - Responsbile for installing/configuring alerta 

- Webshop umbrella template `webshop`:
    Responsible for
    - Deployinng `protectedmachine`, `webshopmachine`, `alertamachine`
    - Exporting master public key `mpk` from the protectedmachine to webshopmachine
    - Running the webserver
    - Healing strategy:
        - Bring system down if `protectedmachine is down`
        - One for one if `webshop` machine is down
