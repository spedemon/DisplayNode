
# Display Node - Python and Javascript plotting and data visualisation. 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# 20 Oct 2013, Helsinki 



from DisplayNodeServer import DisplayNodeServer
from DisplayNodeServer import PROXY_ADDRESS,PROXY_PORT,WEB_ADDRESS,WEB_PORT
from xmlrpclib import Server 
import webbrowser
from multiprocessing import Process
import signal, sys
import socket

socket.setdefaulttimeout(2)


class Display(): 
    def __init__(self,proxy_address=(PROXY_ADDRESS,PROXY_PORT), web_address=(WEB_ADDRESS,WEB_PORT)): 
        self._proxy = Server('http://%s:%s'%proxy_address) 
        self.start_server(proxy_address,web_address) 
        # FIXME: use introspection to define the methods (for autocompletion) 

    def start_server(self,proxy_address,web_address): 
        if not self.is_server_responding(): 
            self._server = DisplayNodeServer(proxy_address,web_address)
            self._server_process = Process( target=self.__run_server_forever, args=() )
            self._server_process.start()
    
    def __run_server_forever(self): 
        signal.signal(signal.SIGINT, self.__signal_handler_interrupt)
        self._server.serve_forever() 

    def __signal_handler_interrupt(self, signal, frame):
        print 'Shutting down DisplayNode server. '
        sys.exit(0)
    
    def is_server_responding(self): 
        try:
            alive = self._proxy.is_alive(1) 
        except: 
            alive = False
        return alive 

    def display(self,content_type,data,open_browser=True,new_tab=False,autoraise=False): 
        url = self._proxy.display({'type':content_type,'data':data}) 
        if open_browser:
            if new_tab:  
                webbrowser.open_new_tab(url) 
            else:
                webbrowser.open(url,autoraise=autoraise) 
                



if __name__ == "__main__": 
    D = DisplayNodeServer()
    D.display('graph','') 

