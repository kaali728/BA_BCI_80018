import socket
import cortex
from cortex import Cortex

def server():
    host = socket.gethostname()  # get local machine name
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()
    print("Connection from: " + str(addr))
    while True:
        brainConfig(c)
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
        print('From online user: ' + data)
        data = data.upper()
        c.send(data.encode('utf-8'))
    c.close()




class BrainConnection():
    def __init__(self, app_client_id, app_client_secret, socketClient, **kwargs):
        self.c = Cortex(app_client_id, app_client_secret, debug_mode=True, **kwargs)
        self.c.bind(create_session_done=self.on_create_session_done)
        self.c.bind(query_profile_done=self.on_query_profile_done)
        self.c.bind(load_unload_profile_done=self.on_load_unload_profile_done)
        self.c.bind(save_profile_done=self.on_save_profile_done)
        self.c.bind(new_fe_data=self.on_new_fe_data)
        self.c.bind(get_mc_active_action_done=self.on_get_mc_active_action_done)
        self.c.bind(mc_action_sensitivity_done=self.on_mc_action_sensitivity_done)
        self.c.bind(inform_error=self.on_inform_error)
        self.socketClient = socketClient

    def start(self, profile_name, headsetId=''):
        if profile_name == '':
            raise ValueError('Empty profile_name. The profile_name cannot be empty.')

        self.profile_name = profile_name
        self.c.set_wanted_profile(profile_name)

        if headsetId != '':
            self.c.set_wanted_headset(headsetId)

        self.c.open()

    def load_profile(self, profile_name):
        self.c.setup_profile(profile_name, 'load')

    def unload_profile(self, profile_name):
        self.c.setup_profile(profile_name, 'unload')

    def save_profile(self, profile_name):
        self.c.setup_profile(profile_name, 'save')

    def subscribe_data(self, streams):
        self.c.sub_request(streams)

    def get_active_action(self, profile_name):
        self.c.get_mental_command_active_action(profile_name)

    def get_sensitivity(self, profile_name):
        self.c.get_mental_command_action_sensitivity(profile_name)

    def set_sensitivity(self, profile_name, values):
        self.c.set_mental_command_action_sensitivity(profile_name, values)

    # callbacks functions
    def on_create_session_done(self, *args, **kwargs):
        print('on_create_session_done')
        self.c.query_profile()

    def on_query_profile_done(self, *args, **kwargs):
        print('on_query_profile_done')
        self.profile_lists = kwargs.get('data')
        if self.profile_name in self.profile_lists:
            # the profile is existed
            self.c.get_current_profile()
        else:
            # create profile
            self.c.setup_profile(self.profile_name, 'create')

    def on_load_unload_profile_done(self, *args, **kwargs):
        is_loaded = kwargs.get('isLoaded')
        print("on_load_unload_profile_done: " + str(is_loaded))

        if is_loaded == True:
            # get active action
            self.get_active_action(self.profile_name)
        else:
            print('The profile ' + self.profile_name + ' is unloaded')
            self.profile_name = ''

    def on_save_profile_done(self, *args, **kwargs):
        print('Save profile ' + self.profile_name + " successfully")
        # subscribe mental command data
        stream = ['fac']
        self.c.sub_request(stream)

    def on_new_fe_data(self, *args, **kwargs):
        global action
        data = kwargs.get('data')
        print('mc data: {}'.format(data))
        eyeAction = data.get('eyeAct')
        lowAction = data.get('lAct')
        action = "neutral"
        if eyeAction != "neutral":
            action = eyeAction
        elif lowAction == "smile":
            print(lowAction)
            action = lowAction
        print(action)
        self.socketClient.send(action.encode('utf-8'))

    def on_get_mc_active_action_done(self, *args, **kwargs):
        data = kwargs.get('data')
        print('on_get_mc_active_action_done: {}'.format(data))
        self.get_sensitivity(self.profile_name)

    def on_mc_action_sensitivity_done(self, *args, **kwargs):
        data = kwargs.get('data')
        print('on_mc_action_sensitivity_done: {}'.format(data))
        if isinstance(data, list):
            # get sensivity
            new_values = [7, 7, 5, 5]
            self.set_sensitivity(self.profile_name, new_values)
        else:
            # set sensitivity done -> save profile
            self.save_profile(self.profile_name)

    def on_inform_error(self, *args, **kwargs):
        error_data = kwargs.get('error_data')
        error_code = error_data['code']
        error_message = error_data['message']

        print(error_data)

        if error_code == cortex.ERR_PROFILE_ACCESS_DENIED:
            # disconnect headset for next use
            print('Get error ' + error_message + ". Disconnect headset to fix this issue for next use.")
            self.c.disconnect_headset()

def brainConfig(socketClient):
    # Please fill your application clientId and clientSecret before running script
    your_app_client_id = 'SIexmTFqD5NGpYPTppg5ZgFS0V9i7Kdex0OaxzVC'
    your_app_client_secret = 'nHh8G5FGtcENZDreMifykEWIHRDXEdj8qmkLJQVxfX0ODwc65v5qRcgL7VcaXajWIYkDop4zy67DuX4Brl7mfQSV8nvKudNdaibrmNZzwc5orRzNBrEbHvVe5HbnK79p'

    # Init live advance
    l = BrainConnection(your_app_client_id, your_app_client_secret, socketClient)

    trained_profile_name = 'Ali'  # Please set a trained profile name here
    l.start(trained_profile_name)

if __name__ == '__main__':
    server()