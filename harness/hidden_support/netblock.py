"""pytest plugin: block all network access so tests must mock it."""
import socket


def pytest_configure(config):
    def refuse(*args, **kwargs):
        raise OSError("network disabled by the benchmark checker")
    socket.socket.connect = refuse
    socket.create_connection = refuse
