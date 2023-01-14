# -*- coding: utf-8 -*-

import flask
import signal
import threading
import traceback
import uuid

from flask import request
from flask import jsonify, Response
from flask_cors import CORS
from waitress import serve

from classes.Profile import Profile
from classes.Research import Research, make_research
from utils.config.Config import Config
from utils.exceptions import ApiToMutchInstantiationException
from utils.signals import previous
from utils.stdout import print_log, print_debug, print_sucess
from utils.utils import to_dict
from utils.Task import Task


class Api(Task):
    """
    Class that represents the OPSE API.
    """

    is_instantiated: bool = False
    __api: threading.Thread = None
    __is_running: bool = False

    def __init__(self):
        """
        Constructor of the API.
        The API should be instancied only one time, otherwise, it can
        produce many issues due to port binding, etc.
        """
        super().__init__()
        signal.signal(signal.SIGINT, previous)

        if Api.is_instantiated:
            raise ApiToMutchInstantiationException()

        self.__client_research_initiate = {}
        self.__is_in_debug = Config.get()["config"]["api"]["is_in_dev_mode"]
        self.__is_unsafe = Config.get()["config"]["api"]["unsafe"]
        self.__host = Config.get()["config"]["api"]["host"]
        self.__port = Config.get()["config"]["api"]["port"]

        print("Host: "+str(self.__host) + "\nPort: " + str(self.__port))
        print_debug("dev mode:" + str(self.__is_in_debug) +
                    ", unsafe mode: " + str(self.__is_unsafe) +
                    ", host: " + str(self.__host) +
                    ", port: " + str(self.__port))

        Api.is_instantiated = True

    def execute(self):
        """Starts the API."""

        app = flask.Flask(__name__)
        cors = CORS(app, resources={r"/*": {"origins": "*"}})

        @app.route('/register', methods=['GET'])
        def register_client():
            """
            Function to register someone in the API
            """
            try:
                client_id = str(uuid.uuid4().hex)
                self.__client_research_initiate[client_id] = []
                return jsonify({"uuid": client_id}), 200
            except Exception as e:
                print_log(str(e) + "\n" + str(traceback.format_exc()))
                return self.send_error_message("Erreur interne. Impossible de traiter la demande", 500)

        @app.route('/make_research', methods=['POST'])
        def make_research_from_client():
            """Function which allow web client to launch research using OPSE"""

            try:
                data = request.get_json()
                nbData_get = 0
                user_input = "USER INPUT"

                if "uuid" not in data:
                    print(request, request.form)
                    return self.send_error_message("Enregistrement nécessaire...", 401)

                elif data["uuid"] not in self.__client_research_initiate.keys() and not self.__is_unsafe:
                    return self.send_error_message("UUID non connu. Accès refusé.", 403)

                # Resolve error of empty key
                for key in data.keys():
                    if data[key] == "":
                        data[key] = None

                    # Remove empty value from list
                    if isinstance(data[key], list):
                        try:
                            while True:
                                data[key].remove("")
                        except ValueError:
                            pass

                if "firstname" in data:
                    firstname = data["firstname"]
                else:
                    firstname = None

                if "middlename" in data:
                    middlename = data["middlename"]
                    if not isinstance(middlename, type(None)):
                        middlename = middlename.split(",")
                else:
                    middlename = None

                if "lastname" in data:
                    lastname = data["lastname"]
                else:
                    lastname = None

                if "gender" in data:
                    gender = data["gender"]
                else:
                    gender = None

                if "birthdate" in data:
                    birthdate = data["birthdate"]
                else:
                    birthdate = None

                if "age" in data:
                    age = data["age"]
                else:
                    age = None

                if "address" in data:
                    address = data["address"]
                else:
                    address = None

                if "phone" in data:
                    phone = data["phone"]
                    if not isinstance(phone, type(None)):
                        phone = phone.split(",")
                else:
                    phone = None

                if "email" in data:
                    email = data["email"]
                    if not isinstance(email, type(None)):
                        email = email.split(",")
                else:
                    email = None

                if "username" in data:
                    username = data["username"]
                    if not isinstance(username, type(None)):
                        username = username.split(",")
                else:
                    username = None

                if not any([
                    firstname,
                    middlename,
                    lastname,
                    gender,
                    birthdate,
                    age,
                    address,
                    phone,
                    email,
                    username,
                ]):
                    return self.send_error_message("Impossible de lancer une recherche sans information", 400)

                research = make_research(
                    firstname,
                    middlename,
                    lastname,
                    gender,
                    birthdate,
                    age,
                    address,
                    phone,
                    email,
                    username,
                    False,
                )
                # We run the function enrich_profiles in parallel, because we want to answer quickly to the client
                threading.Thread(target=research.enrich_profiles()).start()
                self.__client_research_initiate[data["uuid"]].append(research.get_id())
                return jsonify({"research_id": str(research.get_id())}), 200

            except Exception as e:
                print_log(str(e) + "\n" + str(traceback.format_exc()))
                return self.send_error_message("Erreur interne. Impossible de traiter la demande", 500)

        @app.route('/profile', methods=['POST'])
        def get_profile():
            """
            Function which return from web request one profile in json format
            """
            try:
                data = request.get_json()
                # Check client uuid
                if "uuid" not in data:
                    return self.send_error_message("Bad request", 400)
                elif data["uuid"] not in self.__client_research_initiate.keys() and not self.__is_unsafe:
                    return self.send_error_message("UUID non connu. Accès refusé.", 403)

                YES = ["TRUE", "YES", "Y", "true", "yes", "y", True]
                display_none_value = False
                if "display_none_value" in data.keys():
                    if str(data["display_none_value"]).upper() in YES:
                        display_none_value = True

                # Check for permission
                if "research_id" not in data:
                    return self.send_error_message("Bad request", 400)
                elif not self.has_permission(data["uuid"], data["research_id"]):
                    return self.send_error_message("Permission insufisante pour accéder à la ressource demandée", 403)

                if "profile_id" not in data:
                    return self.send_error_message("Bad request", 400)
                elif not self.has_permission(data["uuid"], data["profile_id"]):
                    return self.send_error_message("Permission insufisante pour accéder à la ressource demandée", 403)

                profile: Profile = Profile.get_profile(data["profile_id"])
                research = Research.get_research(data["research_id"])

                return jsonify(to_dict(profile, display_none_value)), 200
            except Exception as e:
                print_log(str(e) + "\n" + str(traceback.format_exc()))
                return self.send_error_message("Erreur interne. Impossible de traiter la demande", 500)

        @app.route('/profiles', methods=['POST'])
        def get_profiles():
            """
            Function which return from web request the list of all profiles in json format
            Profiles are returned as sumarized format.
            """
            try:
                data = request.get_json()
                # Check client uuid

                if "uuid" not in data:
                    return self.send_error_message("Bad request", 400)
                elif data["uuid"] not in self.__client_research_initiate.keys():
                    return self.send_error_message("UUID non connu. Accès refusé.", 403)

                YES = ["TRUE", "YES", "Y", "true", "yes", "y", True]
                display_none_value = False
                if "display_none_value" in data.keys():
                    if str(data["display_none_value"]).upper() in YES:
                        display_none_value = True

                # Check for permission
                if "research_id" not in data:
                    return self.send_error_message("Bad request", 400)
                elif not self.has_permission(data["uuid"], data["research_id"]):
                    return self.send_error_message("Permission insufisante pour accéder à la ressource demandée", 403)

                research = Research.get_research(data["research_id"])
                dict = {'uuid': data["uuid"],
                        'research_id': data["research_id"],
                        'lst_profile': []
                        }
                for profile in research.get_lst_profile():

                    picture = "./img/anon.png"

                    # We will try to get picture from
                    # for pict in profile.get_lst_pictures():
                    #     picture = pict

                    for account in profile.get_lst_accounts():
                        for key in account.__dict__:

                            if account.__dict__[key] is None:
                                continue
                            value = str(account.__dict__[key])

                            # Check extension.
                            # if value.split("://")[0] == "https" or value.split("://")[0] == "http":

                            #     value = html.unescape(value)
                            #     if is_url_image(value):
                            #         picture = value

                    dict['lst_profile'].append({"summary": profile.get_summary(),
                                                "picture": picture,
                                                "profile_id": profile.get_id()})
                return jsonify(dict), 200
            except Exception as e:
                print_log(str(e) + "\n" + str(traceback.format_exc()))
                return self.send_error_message("Erreur interne. Impossible de traiter la demande", 500)

        @app.route('/merge', methods=['POST'])
        def merge():
            """
            Function which take a list of profile to merge.
            This function will try to merge profile depending on same key value.
            """
            
            try:
                data = request.get_json()
                
                # Check client uuid
                if "uuid" not in data:
                    return self.send_error_message("Bad request", 400)
                elif data["uuid"] not in self.__client_research_initiate.keys() and not self.__is_unsafe:
                    return self.send_error_message("UUID non connu. Accès refusé.", 403)

                # Check for permission
                if "research_id" not in data:
                    return self.send_error_message("Bad request", 400)
                elif not self.has_permission(data["uuid"], data["research_id"]):
                    return self.send_error_message("Permission insufisante pour accéder à la ressource demandée", 403)

                # check if their are 2 profiles minimum for the merge
                profiles = data["profile_id"]
                if len(profiles) < 2:
                    return self.send_error_message("Bad request, please provide more than 1 profile", 400)

                # preparing merge
                research = Research.get_research(data["research_id"])
                base_profile: Profile = Profile.get_profile(profiles[0])
                profiles.pop(0)

                for profile in profiles:
                    profile: Profile = Profile.get_profile(profile)

                    try:
                        # try merge
                        new_profile: Profile = research.merge_profile(base_profile, profile)
                        # try add new profile to the research
                        if new_profile is not None:
                            research.get_lst_profile().append(new_profile)
                            # remove old profile
                            research.remove_profile(base_profile)
                            research.remove_profile(profile)
                            base_profile = new_profile
                    except Exception as e:
                        break
                    
                return jsonify({data["research_id"]: "successfully merge some profiles"}), 200
            
            except Exception as e:
                print_log(str(e) + "\n" + str(traceback.format_exc()))
                return self.send_error_message("Erreur interne. Impossible de traiter la demande", 500)

        @app.route('/enrich_profiles', methods=['PUT'])
        def enrich_profiles():
            """Function to update which data can be display for special research"""
            try:
                data = request.get_json()
                # Check client uuid
                if "uuid" not in data:
                    return self.send_error_message("Bad request", 400)
                elif data["uuid"] not in self.__client_research_initiate.keys() and not self.__is_unsafe:
                    return self.send_error_message("UUID non connu. Accès refusé.", 403)

                # Check for permission
                if "research_id" not in data:
                    return self.send_error_message("Bad request", 400)

                elif not self.has_permission(data["uuid"], data["research_id"]):
                    return self.send_error_message("Permission insufisante pour accéder à la ressource demandée", 403)

                research = Research.get_research(data["research_id"])
                research.enrich_profiles()

                return jsonify({"research_id": str(research.get_id())}), 200

            except Exception as e:
                print_log(str(e) + "\n" + str(traceback.format_exc()))
                return self.send_error_message("Erreur interne. Impossible de traiter la demande", 500)

        @app.route('/remove_profile', methods=['DELETE'])
        def remove_profiles():
            """Function to remove special profile from one research"""
            try:
                data = request.get_json()
                # Check client uuid
                if "uuid" not in data:
                    return self.send_error_message("Bad request", 400)
                elif data["uuid"] not in self.__client_research_initiate.keys() and not self.__is_unsafe:
                    return self.send_error_message("UUID non connu. Accès refusé.", 403)

                # Check for permission
                if "research_id" not in data:
                    return self.send_error_message("Bad request", 400)
                elif not self.has_permission(data["uuid"], data["research_id"]):
                    return self.send_error_message("Permission insufisante pour accéder à la ressource demandée", 403)

                research = Research.get_research(data["research_id"])

                if "lst_profile" not in data:
                    return self.send_error_message("Bad request", 400)
                elif not isinstance(data["lst_profile"], list):
                    return self.send_error_message("Bad request", 400)
                else:

                    if len(data["lst_profile"]) <= 0 or len(data["lst_profile"]) > len(research.get_lst_profile()):
                        return self.send_error_message("Bad request", 400)

                    for profile_id in data["lst_profile"]:
                        if not self.has_permission(data["uuid"], profile_id):
                            return self.send_error_message("Permission insufisante pour accéder à la ressource demandée", 403)

                for profile_id in data["lst_profile"]:
                    profile: Profile = Profile.get_profile(profile_id)
                    research.remove_profile(profile)

                return jsonify(data), 200

            except Exception as e:
                print_log(str(e) + "\n" + str(traceback.format_exc()))
                return self.send_error_message("Erreur interne. Impossible de traiter la demande", 500)

        self.__is_running = True
        print_sucess(" API Launched")

        if self.__is_in_debug:
            app.run(debug=False, host=self.__host, port=self.__port)
        else:
            serve(app, host=self.__host, port=self.__port)
        return True

    def has_permission(self, client_id: str, ressource_id: str) -> bool:
        """Function that returns True if the client has permission on
        a specific ressource. Else returns False.

        :param client_id: Client's identifier.
        :type client_id: str
        :param ressource_id: Ressource's identifier.
        :type ressource_id: str
        :return: True if the client has permission over the ressource,
         else False.
        :rtype: bool
        """

        # If unsafe mode is activate. Then every access is made easier.
        # This is to help developper to dev API.
        # /!\ Unsafe mode should nether be use in production.
        if self.__is_unsafe:
            return True

        # If the client is not register, then return False
        if client_id not in self.__client_research_initiate.keys():
            return False

        # Check if the ressource was produce by user research
        for research_id in self.__client_research_initiate[client_id]:

            find_research = Research.get_research(research_id)

            if find_research is None:
                continue

            linked_id = find_research.get_linked_id()
            if ressource_id == linked_id["research"]:
                return True
            elif ressource_id in linked_id["profile"]:
                return True
        return False

    @staticmethod
    def send_error_message(error_message: str, code: int) -> tuple[Response, int]:
        """Normalizes error message to send to a web user.`

        :param error_message: The error message.
        :type error_message: str
        :param code: The HTTP return status code.
        :type code: int
        :return: A tuple containing the Response with the error message
         and the status code associated.
        :rtype: tuple[:class:`~flask.wrappers.Response`, int]
        """
        return jsonify({"error_message": error_message}), code

    @staticmethod
    def is_running() -> bool:
        """Returns the state of the API: running or not.

        :return: True if the API is running, else False.
        :rtype: bool
        """
        return Api.__is_running

    @staticmethod
    def get() -> threading.Thread:
        """Returns the API.
        Instanciates the API if it's not.

        :return: A thread.
        :rtype: threading.Thread
        """
        # We instanciate the API
        if not Api.is_instantiated:
            Api.__api = Api()

        return Api.__api
