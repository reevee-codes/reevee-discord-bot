from errors.command_error import CommandError

class EchoService:

    def build_echo_text(self, args):
        if not args:
             raise CommandError("You must specify a message")
        return " ".join(args)