
import time
import os
import subprocess
import datetime
import json

'''

*** Daemon restart Nginx and PHP-fmp

'''

class Restarter:


    def __init__(self) -> None:
        self.conf = 'config.json'
        self.time_sleep = 60
    

    def write_log(self, t, e):

        try:

            path = self.path_log_restarter_error if t else self.path_log_restarter

            with open(path, "a") as f: f.write(f'{str(e)}\n')

        except Exception as e:
            print("[+] Error in write log")
            print(e)

    
    def readFile(self, file):

        try:

            if os.path.exists(file):

                print(f'[+] File {file} is exists')

                with open(file, 'r') as logs: return logs.read()
            

            print(f'[+] File {file} is not exists')
            return False

        except Exception as e:
            print('[+] Error in read fpm logs')
            print(e)
            self.write_log(True, e)
            return False


    def start(self):

        try: 

            while True:

                config = self.readFile(self.conf)

                if config != False:

                    config = json.loads(config)

                    print('[+] Upadate time_sleep')

                    self.time_sleep = config['time_sleep']

                    self.path_log_restarter = config['path_log_restarter']

                    self.path_log_restarter_error = config['path_log_restarter_error']

                    self.path_to_log_fpm = config['path_to_log_fpm']

                    self.varsion_fmp = config['varsion_fmp']
                    
                    self.save_log_fpm = config['save_log_fpm']

                    try:
                        logs = self.readFile(self.path_to_log_fpm)
                       
                        if logs != False:

                           if 'server reached pm.max_children setting' in str(logs):

                                print('[+] Restart nginx | fpm | rewrite file')
                                
                                with open(self.save_log_fpm, "a") as f: f.write(f'{str(logs)}\n')

                                try:
                                    
                                    print('[+] Restart nginx')
                                    self.write_log(False, f'\nRestart NGINX Time: {datetime.datetime.now()}\n')
                                    subprocess.call('systemctl restart nginx', shell=True)

                                except Exception as e:
                                    self.write_log(True, f'ERROR IN RESTART NGINX Time: {datetime.datetime.now()}')

                                
                                try:
                                    
                                    print('[+] Reatart fpm')
                                    self.write_log(False, f'\nRestart FPM Time: {datetime.datetime.now()}\n')
                                    subprocess.call(f'systemctl restart {self.varsion_fmp}', shell=True)

                                except Exception as e:
                                    self.write_log(True, f'ERROR IN RESTART FPM Time: {datetime.datetime.now()}')
                                

                                try:
                                    
                                    print('[+] Rewrite logs')
                                    self.write_log(False, f'\nRewrite LOGS Time: {datetime.datetime.now()}\n')
                                    subprocess.call(f'echo "" > {self.path_to_log_fpm}', shell=True)

                                except Exception as e:
                                    self.write_log(True, f'ERROR IN RESET LOG_FPM Time: {datetime.datetime.now()}')

                                self.write_log(False, f'Restart server and fpm\n Time: {datetime.datetime.now()}')

                        else: self.write_log(True, f'FPM_LOG is False Time: {datetime.datetime.now()}')

                    except Exception as e:
                       print('[+] Error in start method')
                       print(e)
                       self.write_log(True, e)
                
                else: self.write_log(True, f'Config is False Time: {datetime.datetime.now()}')

                self.write_log(False, f'Next step Time: {datetime.datetime.now()}')

                config = None

                print(f'[+] Sleep {self.time_sleep}')
                time.sleep(self.time_sleep)
        
        except Exception as e:
            print('[+] Error in start method!\n program STOP')
            print(e)
            self.write_log(True, e)
            self.write_log(True, "Error in start method! Program STOP")


if __name__ == '__main__':

    try:

        Restarter().start()
        print('[+] Sleep 60 sec')
    
    except Exception as e:
        print('[+] Error in ')