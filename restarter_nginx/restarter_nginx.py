
import json
import os
import time
import datetime
import subprocess

'''

*** Daemon restart only nginx

'''

class Restarter_nginx:
    
    
    def __init__(self) -> None:
        self.time_sleep = 60
        
    
    def write_log(self, t, e):

        try:

            path = self.path_log_restarter_error if t else self.path_log_restarter

            with open(path, "a") as f: f.write(f'{str(e)}\n')

        except Exception as e:
            print("[+] Error in write log")
            print(e)
    
    
    def readConf(self):

        try:
            
            file = 'config.json'

            if os.path.exists(file):

                with open(file, 'r') as conf: return json.loads(conf.read())
            
            return False

        except Exception as e:
            self.write_log(True, e)
            return False
    
    
    def restart(self):
        try:
            result = subprocess.run(['systemctl', 'restart', 'nginx'])
            
            if len(result.stderr) == 0:
                
                result = subprocess.run(['systemctl', 'status', 'nginx'], capture_output=True, text=True)
                
                if len(result.stderr) == 0:
                    
                    if 'Active: active (running)' not in result.stdout: self.write_log(True, f'ERROR IN REPEAT RESTART NGINX Time: {datetime.datetime.now()}')
                            
                    else: self.write_log(False, f'Check Time: {datetime.datetime.now()}')
                        
                else: self.write_log(True, f'\nSome error in get repeat status NGINX Time: {datetime.datetime.now()}\n')
            
            else: self.write_log(True, f'ERROR IN RESTART NGINX Time: {datetime.datetime.now()}')
        
        except Exception as e:
            self.write_log(True, e)
            
    
    def run(self):
        
        try:
            
            while True:
                
                print("[+] Step")
                
                try:
    
                    config = self.readConf()
                    
                    if config:
                        
                        self.time_sleep = config['time_sleep']
                        
                        self.path_log_restarter = config['path_log_restarter']
                        
                        self.path_log_restarter_error = config['path_log_restarter_error']
                        
                        result = subprocess.run(['systemctl', 'status', 'nginx'], capture_output=True, text=True)
                        
                        if len(result.stderr) == 0:
                            
                            self.restart() if 'Active: active (running)' not in result.stdout else self.write_log(False, f'Check Time: {datetime.datetime.now()}')
                        
                        else: self.write_log(True, f'\nSome error in get status NGINX Time: {datetime.datetime.now()}\n')
                            
                    else: self.write_log(True, f'Can not read CONFIG Time: {datetime.datetime.now()}')
                        
                except Exception as e:
                    self.write_log(True, e)
                    
                time.sleep(self.time_sleep)
            
        except Exception as e:
            print("[+] Error")
            print(e)


if __name__ == "__main__":
    
    try:
        print('[+] Start Restarter_nginx')
        
        Restarter_nginx().run()

    except Exception as e: print(e)
    
