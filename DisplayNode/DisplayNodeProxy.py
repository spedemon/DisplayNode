
# Display Node - Python and Javascript plotting and data visualisation. 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# 20 Oct 2013, Helsinki 



from DisplayNode import *
from xmlrpclib import Server 
import webbrowser
from multiprocessing import Process



class DisplayNode(): 
    def __init__(self,proxy_address=(PROXY_ADDRESS,PROXY_PORT), web_address=(WEB_ADDRESS,WEB_PORT)): 
        self._proxy = Server('http://%s:%s'%proxy_address) 
        self.start_server(proxy_address,web_address) 
        # FIXME: use introspection to define the methods (for autocompletion) 

    def start_server(self,proxy_address,web_address): 
        if not self.is_server_responding(): 
            self._server = DisplayNode(proxy_address,web_address)
            self._server_process = Process(target=self._server.serve_forever, args=() )
            self._server_process.start()
            #self._server_process.join()
        
    def is_server_responding(self): 
        try:
            alive = self._proxy.is_alive(1)
        except: 
            alive = False
        return alive 

    def display(self,content_type,data,open_browser=True,new_tab=True): 
        url = self._proxy.display({'type':content_type,'data':data}) 
        if open_browser:
            if new_tab:  
                webbrowser.open_new_tab(url) 
            else:
                webbrowser.open(url) 
                



if __name__ == "__main__": 
    D = DisplayNode()
    D.display('graph','') 

