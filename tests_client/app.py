# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sys

if __name__ == '__main__':
    """
    Simple application for client/server development and testing.

    Example usage: python app.py debug

    Server TODO:
        - Test on all Platforms
            - Dependencies:
                [cryptography, cffi, six, pycparser]
                [service-identity, pyasn1, pyasn1-modules, pyopens, sl, characteristic]
        - Fix File Picker to be OS native (also needs to get proper focus)
            * win32api depends on python version (ie: 2.6 64-bit), so this will be complicated.
                - Also needs function pointers which I don't know how to pass (even possible?)
                - Should we instead compile our own c++ dll to be used with python for the file dialog? (unless we know how to pass hook)

                - When do we actually need both files/folder selection?
        - Make repo: tk-framework-toolkit-server --> see: editorial framework for blank framework
        - uft-8 unit testing internationalization
    """
    sys.path.append("../resources/python")
    sys.path.append("../")

    from twisted.internet import reactor, ssl
    from twisted.web.static import File
    from twisted.web.server import Site
    from twisted.python import log

    from python.tk_server import Server

    # Get debug info
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug = True
    else:
        debug = False

    if debug:
        log.startLogging(sys.stdout)

    server = Server()

    # Serve test pages
    local_server = debug
    keys_folder = "../resources/keys"
    if local_server:
        # Serve client folder
        keys_dir = File(keys_folder)
        web_dir = File("./client")
        web_dir.putChild("keys", keys_dir)
        web_dir.contentTypes[".crt"] = "application/x-x509-ca-cert"
        web = Site(web_dir)
        #reactor.listenSSL(8080, web, server.contextFactory)        # For serving https..
        reactor.listenTCP(8080, web)

    server.start(debug, keys_folder)
