# -*- coding: utf-8 -*-

"""

kaautils.py

This module contains useful methods to operate with Kaa

"""

import requests

class KaaNodeError(Exception):
    pass

class KaaSDKLanguage(object):
    """List of supported SDK languages"""
    C = 'C'
    CPP = 'CPP'
    JAVA = 'JAVA'
    OBJECTIVE_C = 'OBJC'

class KaaUser(object):
    """Represents Kaa user"""

    def __init__(self, name, password):
        """
        :param name: Kaa use name
        :type name: string
        :param password: Kaa user port
        :type password: string
        """

        self.name = name
        self.password = password

class KaaNode(object):
    """Allows to communicate with Kaa node via REST API"""

    def __init__(self, host, port):
        """
        :param host: Kaa node IP address
        :type host: string
        :param port: Kaa node port
        :type port: string or integer
        """

        self.host = str(host)
        self.port = str(port)

    def download_sdk(self, profile_id, language, kaauser, ofile):
        """Downloads specific SDK from Kaa server and writes it to a file.

        :param profile_id: Kaa SDK profile ID.
        :type profile_id: integer
        :param language: Represents SKD language.
        :type language: KaaSDKLanguage
        :param kaauser: The Kaa User.
        :type kaauser: KaaUser
        :param ofile: Output filename. NOTE: If the file is already exists, it will be overwritten.
        :type ofile: string
        """

        url = 'http://%s:%s/kaaAdmin/rest/api/sdk?sdkProfileId=%s&targetPlatform=%s'%(self.host, self.port, str(profile_id), language)

        req = requests.post(url, auth=(kaauser.name, kaauser.password))
        if req.status_code != requests.codes.ok:
            raise KaaNodeError('Unable to download SDK. Return code: %d'%req.status_code)

        with open(ofile, 'w') as output_file:
            output_file.write(req.content)

    def get_applications(self, kaauser):
        """Gets the list for Kaa application. Returns result in JSON format.

        :param kaauser:  The Kaa user.
        :type kaauser: KaaUser
        """

        url = 'http://%s:%s/kaaAdmin/rest/api/applications'%(self.host, self.port)

        req = requests.get(url, auth=(kaauser.name, kaauser.password))
        if req.status_code != requests.codes.ok:
            raise KaaNodeError('Unable to get list of applications. Return code: %d'%req.status_code)

        return req.json()

    def get_sdk_profiles(self, appname, kaauser):
        """Gets the SDK profiles for application. Returns result in JSON format.

        :param appname: The name of the application.
        :type appname: string
        :param kaauser: The Kaa server IP address.
        :type kaauser: KaaUser
        """

        apps = self.get_applications(kaauser)
        token = None
        for app in apps:
            if app['name'] == appname:
                token = app['applicationToken']
                break

        if not token:
            raise KaaNodeError('Application: "%s" was not found'%appname)

        url = 'http://%s:%s/kaaAdmin/rest/api/sdkProfiles/%s'%(self.host, self.port, str(token))

        req = requests.get(url, auth=(kaauser.name, kaauser.password))
        if req.status_code != requests.codes.ok:
            raise KaaNodeError('Unable to get SDK profiles. Return code: %d'%req.status_code)

        return req.json()