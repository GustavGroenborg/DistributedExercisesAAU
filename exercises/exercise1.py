from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub


class GossipMessage(MessageStub):
    """ The message that is distributed. """
    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip(Device):
    """ Scenario 1: The device that distributes messages. """
    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new
        # routing-table (for instance) or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        count = self.index()
        while True:
            dest = count % self.number_of_devices()
            count = (count + 1) % self.number_of_devices()
            if dest != self.index():
                self.medium().send(GossipMessage(self.index(), dest, self._secrets))

            # Exiting if all secrets are already known
            if len(self._secrets) == self.number_of_devices() and count == self.index():
                return

            for msg in self.medium().receive_all():
                self._secrets = self._secrets.union(msg.secrets)

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')

class BiDirectionalGossip(Device):
    """ Scenario 2: The device that distributes messages bi-directionally. """
    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        self._secrets = set([index])

    def run(self):
        while True:
            left = (self.index() - 1) % self.number_of_devices()
            right = (self.index() + 1) % self.number_of_devices()

            # Sending the messages left and right
            self.medium().send(GossipMessage(self.index(), left, self._secrets))
            self.medium().send(GossipMessage(self.index(), right, self._secrets))

            # Exiting if all secrets are already known
            if len(self._secrets) == self.number_of_devices():
                return

            for msg in self.medium().receive_all():
                self._secrets = self._secrets.union(msg.secrets)

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')
