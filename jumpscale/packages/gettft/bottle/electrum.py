from jumpscale.loader import j
from jumpscale.packages.gettft.models.user_model import users


class Electrum:
    def __init__(self, public_key: str, test_net: bool) -> None:
        self.NAME = "shop_wallet"
        self.public_key = public_key
        self.test_net = test_net

        """Check daemon and get path"""
        daemon_info = self.check_daemon()
        self.path = self.get_wallet_path(daemon_info)  # TODO: FIXME

        """Load wallet or restore it"""
        self.load_wallet()

    def exec(self, *cmds):
        cmd = self.create_command(*cmds)
        """ rc, op, error """
        rc, out, __ = j.sals.process.execute(cmd)
        return rc, out

    def create_command(self, *cmds: list) -> str:
        command = ["electrum", *cmds]
        if self.test_net:
            command.append("--testnet")
        return str.join(" ", command)

    def get_wallet_path(self, output: str):
        return f"{j.data.serializers.json.loads(output)['path']}/wallets/{self.NAME}"

    def check_daemon(self):
        rc, out = self.exec("getinfo")
        if rc != 0 or "daemon not running" in out.lower():
            raise Exception("Daemon is not running")
        return out

    def restore_wallet(self):
        self.exec("restore", self.public_key, "-w", self.path)

    def generate_used_addresses(self):
        for _ in range(users.count):
            self.create_address()

    def load_wallet(self, first_time=True):
        rc, out = self.exec("load_wallet", "-w", self.path)

        # Try to restore wallet if it's not loaded (only once!)
        if rc != 0 or "false" in out.lower():
            if first_time:
                self.restore_wallet()
                self.load_wallet(False)
                return self.generate_used_addresses()
            raise Exception("Couldn't load wallet.")

    def create_address(self):
        rc, out = self.exec("createnewaddress", "-w", self.path)
        out = out.strip()
        if rc == 0:
            return out
        raise Exception("Couldn't create new address.")
