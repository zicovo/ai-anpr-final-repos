import os
import websockets
import asyncio

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from model import predict

async def send_result(result):
  uri = "ws://localhost:5000"
  async with websockets.connect(uri) as websocket:
    print(result)
    await websocket.send(result)



class MyHandler(FTPHandler):

    def on_file_received(self, file):
        prediction = predict(file)
        if prediction[0] == 0 or prediction[0] == 1:
            print("phone use")
            asyncio.get_event_loop().run_until_complete(send_result("phone-use"))
            return "phone use"
        else:
            print("not using phone")
            asyncio.get_event_loop().run_until_complete(send_result("no-phone-use"))
            return "not using phone"


def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = MyHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    # handler.masquerade_address = '151.25.42.11'
    # handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    # Use 0.0.0.0 if you want to make it accessible, so that everyone in the network can access the ftp server
    address = ('0.0.0.0', 21)
    
    # Use 127.0.0.1 to test it locally
    # address = ('127.0.0.1', 21)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()


if __name__ == '__main__':
    main()

