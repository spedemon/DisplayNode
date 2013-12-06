
# Display Node - Python and Javascript plotting and data visualisation. 
# Stefano Pedemonte
# Aalto University, School of Science, Helsinki
# 20 Oct 2013, Helsinki 



import BaseHTTPServer
from SimpleXMLRPCServer import SimpleXMLRPCServer 
import urllib2

import os, time, shutil, random
from thread import start_new_thread 
from math import floor

NO_KEY = "<html><head><title>NodeDisplay</title></head><body><p>NodeDisplay: no key</p></body></html>"

WEB_ADDRESS   = '127.0.0.1'
WEB_PORT      = 8001 
PROXY_ADDRESS = '127.0.0.1'
PROXY_PORT    = 8002

LOCAL_STORAGE_PATH = '.'+os.sep+'._DisplayNode'+os.sep

RESOURCES = {                        
                'three.js':         {'url':  'http://threejs.org/build/three.js',     
                                     'local': False, 
                                     'location':'.'+os.sep+'static'+os.sep},
                                     
                'three.min.js':     {'url':  'http://threejs.org/build/three.min.js',     
                                     'local': False, 
                                     'location':'.'+os.sep+'static'+os.sep},    
                                     
                'TrackballControls.js': {'url':  'http://threejs.org/examples/js/controls/TrackballControls.js',     
                                     'local': False, 
                                     'location':'.'+os.sep+'static'+os.sep},  
                                     
                                     
                'stats.min.js':     {'url':  'http://threejs.org/examples/js/libs/stats.min.js',     
                                     'local': False, 
                                     'location':'.'+os.sep+'static'+os.sep},  
                                
                                
                                          
                'd3.v3.js':         {'url':  'http://d3js.org/d3.v3.js',           
                                     'local':False, 
                                     'location':'.'+os.sep+'static'+os.sep},    
                                     
                'd3.v3.min.js':     {'url':  'http://d3js.org/d3.v3.min.js',       
                                     'local':False, 
                                     'location':'.'+os.sep+'static'+os.sep},   
                                     


                'openseadragon.js': {'url':  'openseadragon/openseadragon.js',
                                     'local':True , 
                                     'location':'.'+os.sep+'static'+os.sep},
                                     
                                     
                                     
                'plot.html':        {'url':  'plot.html',                     
                                     'local':True , 
                                     'location':'.'+os.sep+'static'+os.sep},
                                     
                'three_cubes.html': {'url':  'three_cubes.html',                    
                                     'local':True , 
                                     'location':'.'+os.sep+'static'+os.sep},
                                     
                'graph.html':       {'url':  'graph.html',                    
                                     'local':True , 
                                     'location':'.'+os.sep+'static'+os.sep},  
                                            
                'index.html':       {'url':  'index.html',                    
                                     'local':True , 
                                     'location':'.'+os.sep+'static'+os.sep},          } 






class FrontendServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self,address,handler): 
        self.address = address 
        self.httpd   = BaseHTTPServer.HTTPServer(self.address, self) 
        self.handler = handler

    def serve_forever(self): 
        #print time.asctime(), "FrontendServer Starts - %s:%s" % self.address
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt: 
            print "Frontend interrupted (Control-C)"
        self.httpd.server_close()
        #print time.asctime(), "FrontendServer Stops  - %s:%s" % self.address 

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        key = self.path
        html = self.handler(key)
        self.wfile.write(html) 

    def __call__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def log_message(self,*arg): 
        pass 

        

class BackendServer(): 
    def __init__(self,address,functions_to_register): 
        self.server = SimpleXMLRPCServer(address,logRequests=False) 
        self.register_functions(functions_to_register)  
        self.address = address 

    def register_functions(self,functions):
        for f in functions:  
            self.server.register_function(f)
        self.server.register_function(self.is_alive)
        self.server.register_introspection_functions() 

    def is_alive(self,value): 
        return value

    def serve_forever(self,blocking):
        #print time.asctime(), "BackebdServer Starts - %s:%s" % self.address 
        if blocking: 
            self.server.serve_forever()
        else: 
            start_new_thread(self.server.serve_forever,()) 
            
    def stop(self):
        pass 
        #print time.asctime(), "BackendServer Stops  - %s:%s" % self.address






 
 

class Content(): 
    def __init__(self): 
        self.name = ''
        self.html = "<html><head><title>NodeDisplay</title></head><body><p> </p></body></html>"
        self.resources = []
        self.data = {} 
        self.resource_manager = ResourceManager() 
        
    def get_html(self): 
        return self.html 

    def make_content(self):
        self.html = ''

    def _decorate_with_resources(self,html,resources): 
        needed_html = ''
        for r in resources: 
            if r.endswith('.js'): 
                l = "<script type='text/javascript' src='%s'></script>"%(RESOURCES[r]['location'].replace(os.sep,"/")+r)
            elif r.endswith('.css'): 
                pass
            else: 
                pass
            needed_html = needed_html + l +'\n'
        return html.replace('<head>', '<head>%s' % needed_html, 1)


class Plot(Content): 
    def __init__(self,data): 
        Content.__init__(self)
        self.data = data
        self.name = 'plot' 
        self.template = 'plot.html'
        self.resources = ['d3.v3.min.js',]
        self.make_content()
    
    def make_content(self): 
        self.html = "<html><head><title>NodeDisplay</title></head><body><p>Plot</p></body></html>"
        self.html = self._decorate_with_resources(self.html,self.resources) 

class Image(Content): 
    def __init__(self,data): 
        Content.__init__(self)
        self.data = data
        self.name = 'image'
        self.template = 'image.html'
        self.resources = ['openseadragon.js',]
        self.make_content()

    def make_content(self): 
        self.html = self.read_remplate()
        self.html = self._decorate_with_resources(self.html,self.resources) 
       
class Graph(Content): 
    def __init__(self,data): 
        Content.__init__(self)
        self.data = data
        self.name = 'graph'
        self.template = 'graph.html'
        self.resources = ['d3.v3.min.js',]
        self.make_content()

    def make_content(self): 
        self.html = self.resource_manager.get_resource_data(self.template)
        self.html = self._decorate_with_resources(self.html,self.resources) 
        # FIXME: data
    
class ThreeCubes(Content): 
    def __init__(self,data): 
        Content.__init__(self)
        self.data = data
        self.name = 'three_cubes'
        self.template = 'three_cubes.html'
        self.resources = ['three.min.js','TrackballControls.js','stats.min.js'] 
        self.make_content()
        
    def make_content(self): 
        self.html = self.resource_manager.get_resource_data(self.template)
        self.html = self._decorate_with_resources(self.html,self.resources) 
        # FIXME: data




class ResourceManager(): 
    def __init__(self,local_storage_path=LOCAL_STORAGE_PATH): 
        self.local_storage_path = local_storage_path
        self.initialize_local_storage()
        
    def initialize_local_storage(self): 
        if not os.path.exists(self.local_storage_path): 
            os.mkdir(self.local_storage_path) 
        # copy all the resources defined as local 
        for rname in RESOURCES.keys(): 
            r = RESOURCES[rname] 
            if r['local']: 
                rlocation = r['location']
                if rlocation.startswith('.'): 
                    rlocation=rlocation[1:]
                source = os.path.split(__file__)[0]+rlocation+rname
                destination = self.local_storage_path+rlocation+rname
                if not os.path.exists(os.path.split(destination)[0]): 
                    os.mkdir(os.path.split(destination)[0]) 
                shutil.copy(source,destination) 
                    
    def is_resource(self,resource_name): 
        return (resource_name in RESOURCES.keys()) 
         
    def is_valid_local_resource(self,resource_path): 
        if not self.is_resource(os.path.basename(resource_path)): 
            return False 
        resource = RESOURCES[os.path.basename(resource_path)] 
        location = resource['location']
        return (location.replace('.'+os.sep,'').replace(os.sep,'') == os.path.dirname(resource_path).replace('.'+os.sep,'').replace(os.sep,''))
        
    def is_available_locally(self,resource,full_path=False): 
        if not full_path:
            if not self.is_resource(resource): 
                return False 
            location = RESOURCES[resource]['location']  
            resource = location + resource 
        resource = self.local_storage_path + resource
        return os.path.exists(resource)

    def fetch_resource(self,resource_name): 
        url = RESOURCES[resource_name]['url']
        location = RESOURCES[resource_name]['location']
        print "Fetching %s  [%s -> %s] ..."%(resource_name,url,location + resource_name)
        t = time.time()
        response = urllib2.urlopen(url)
        content = response.read()
        resource = location + resource_name
        resource = self.local_storage_path + resource
        fid = open(resource,'w')
        fid.write(content)
        fid.close() 
        print "Fetched %d bytes in %2.3f sec."%(len(content),time.time()-t)

    def get_resource_data(self,resource,full_path=False): 
        if not self.is_available_locally(resource,full_path=full_path): 
            return None
        else: 
            if not full_path:
                location = RESOURCES[resource]['location']
                resource = location + resource
            resource = self.local_storage_path + resource
            fid = open(resource,'r') 
            d = fid.read() 
            fid.close()
            return d 



class ContentProvider():
    def __init__(self): 
        self.dict = {}
        self.resource_manager = ResourceManager() 
        self.start_maintainance() 

    def _generate_key(self): 
        return str(int(floor(random.random()*10000000+1))) #make sure it's unique FIXME

    def make_content(self,content_descriptor): 
        key = self._generate_key()  
        if not isinstance(content_descriptor,type({})): 
            return 'invalid' 
        if not (content_descriptor.has_key('type') and content_descriptor.has_key('data')): 
            return 'invalid' 
        if content_descriptor['type'] == 'plot': 
            content = Plot(content_descriptor['data']) 
        elif content_descriptor['type'] == 'image': 
            content = Image(content_descriptor['data']) 
        elif content_descriptor['type'] == 'graph': 
            content = Graph(content_descriptor['data']) 
        elif content_descriptor['type'] == 'three_cubes': 
            content = ThreeCubes(content_descriptor['data']) 
        else: 
            return 'nokey'           
        self.dict[key] = content
        return key

    def get_content(self,key): 
        key = key[1:]
        if self.dict.has_key(key): 
            content = self.dict[key] 
            # make sure that the static files are available locally 
            for resource in content.resources: 
                if not self.resource_manager.is_available_locally(resource): 
                    self.resource_manager.fetch_resource(resource) 
            # return the html content  
            content = content.get_html()
            return content
        else: 
            # if it is a valid static file, serve it 
            if not self.resource_manager.is_valid_local_resource(resource_path=key): 
                return NO_KEY
            else: 
                content = self.resource_manager.get_resource_data(resource=key,full_path=True)
                return content
    def start_maintainance(self):
        pass 






class DisplayNodeServer(): 
    def __init__(self,backend_address=(PROXY_ADDRESS,PROXY_PORT),frontend_address=(WEB_ADDRESS,WEB_PORT)): 
        self.frontend_address = frontend_address
        self.backend_address = backend_address
        self.frontend_server = FrontendServer(frontend_address,self.get_content) 
        self.backend_server = BackendServer(backend_address,[self.display])
        self.content_provider = ContentProvider() 

    def get_content(self,key):
        return self.content_provider.get_content(key)

    def make_content(self,content_descriptor): 
        key = self.content_provider.make_content(content_descriptor)
        #print "New content at %s"%key
        address = 'http://'+self.frontend_address[0]+":"+str(self.frontend_address[1])+"/"+key
        return address
     
    def display(self,*args): 
        return self.make_content(*args)
   
    def serve_forever(self): 
        self.backend_server.serve_forever(blocking=False)
        self.frontend_server.serve_forever() 
        self.frontend_server.stop() 
        self.backend_server.stop() 

    def stop(self): 
        self.backend.stop()
        self.frontend.stop() 




    
if __name__=="__main__": 
    F = DisplayNodeServer()
    F.serve_forever()
    
