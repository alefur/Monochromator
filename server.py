import logging
import socket
from datetime import datetime as dt
from mono import Monochromator


def runServer(args):
    host = args.host
    port = args.port
    logFolder = args.logFolder

    logger = logging.getLogger('monoserver')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('%s/%s-mono.log' % (logFolder, dt.utcnow().replace(microsecond=0).isoformat()))
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    try:
        while True:
            sock.listen(5)
            client, address = sock.accept()
            logger.debug("{} connected".format(address))

            mono = Monochromator(remote=True)

            while True:
                try:
                    command = client.recv(255)
                except ConnectionResetError:
                    command = False
                if not command:
                    break

                cmdStr = command.decode()
                logger.debug("received command : %s" % cmdStr)

                try:
                    cmdStr = cmdStr.split('\r\n')[0]
                    funcname = cmdStr.split(',')[0]
                    args = cmdStr.split(',')[1:]
                    func = getattr(mono, funcname)
                    ret = func(*args)
                    msg = '0,%s' % ret

                except Exception as e:
                    msg = '1,%s' % str(e)

                logger.debug("sending reply : %s" % msg)
                client.send(('%s\r\n' % msg).encode('utf-8'))

            client.close()

    except KeyboardInterrupt:
        print('interrupted!')

    sock.close()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='ait-server', type=str, nargs='?', help='database server ip address')
    parser.add_argument('--port', default='4003', type=int, nargs='?', help='database server port')
    parser.add_argument('--logFolder', default='/software/monochromator', type=str, nargs='?', help='log')

    args = parser.parse_args()

    runServer(args)


if __name__ == '__main__':
    main()
