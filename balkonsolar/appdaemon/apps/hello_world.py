import appdaemon.plugins.hass.hassapi as hass

class HelloWorld(hass.Hass):
    def initialize(self):
        self.log("Hello from AppDaemon!")
        self.log("This is version 1.0 of the HelloWorld app")
