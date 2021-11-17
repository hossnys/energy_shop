from jumpscale.loader import j


class gettft:
    def install(self, **kwargs):
        # create xlms wallet
        if "gettft_xlm" not in j.clients.stellar.list_all():
            secret = kwargs.get("secret", None)
            wallet = j.clients.stellar.new("gettft_xlm", secret=secret)
            if not secret:
                wallet.activate_through_threefold_service()
            wallet.save()
