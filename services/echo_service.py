
class EchoService:

    def build_echo_text(self, args):
        if not args:
            return None
        return " ".join(args)