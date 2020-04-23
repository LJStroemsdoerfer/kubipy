# import libs
import subprocess
import os
from requests import get
from sys import platform

# setup class
class minipy:

    # describe class
    def __init__(self):
        
        # define the slots
        self.description = 'local kubernetes cluster'
        self.url_mac = 'https://download.virtualbox.org/virtualbox/6.1.6/VirtualBox-6.1.6-137129-OSX.dmg'
        self.OS = platform
        self.wd = os.getcwd()
        self.status = None

    # define private method to download file
    def __download_driver(self, url, file_name):

        # try to download driver
        try:

            # download a binary file
            with open(file_name, 'wb') as file:

                # get the content
                response = get(url)

                # write the file to a temporary directory
                file.write(response.content)

            # return
            return True
        
        # return false if it doesn't work
        except:

            # return
            return False

    # define private method to create a temporary directory
    def __create_temp_dir(self):

        # try to create tmp dirctory in cwd
        try:

            # create tmp
            os.mkdir('tmp_dir')

            # save dir_name
            dir_name = 'tmp_dir'

            # return dir_name
            return dir_name

        # handle exception
        except:

            # return
            return None

    # function to install driver
    def __install_driver(self, file_name):

        # try to install driver
        try: 

            # mount the dmg
            command = str('hdiutil attach ' + file_name)
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # change to mounted volume
            os.chdir('/Volumes/VirtualBox')

            # install the .pkg file
            command = str('sudo installer -pkg VirtualBox.pkg -target /')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # unmount and eject the dmg
            command = str('hdiutil detach -force /Volumes/VirtualBox/')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # change to previous wd
            os.chdir(self.wd)

            # remove tmp dir
            tmp_dir_name = file_name.split('/')[0]
            command = str('rm -rf ' + tmp_dir_name)
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # return
            return True

        # return if it doesn't work
        except:

            # return
            return False

    # function to install kubectl
    def __install_kubectl(self):

        # try to install kubectl
        try:

            # install kubectl
            command = 'brew install kubectl 2>&1'
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # return
            return True

        # return false if it didn't work
        except:

            # return
            return False

    # function to install minikube
    def __install_minikube(self):

        # try to install minikube
        try:

            # install minikube
            command = 'brew install minikube'
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # return 
            return True
        
        # return false if it didn't work
        except:

            # return 
            return False

    # function to install minikube
    def install(self):

        # check if platform is macOS
        if platform == 'darwin':

            # set the binary download to the macOS file
            url = self.url_mac

            # define file ending
            ending = '.dmg'

        # else
        else:

            # exit function
            raise Exception('Currently only MacOS is supported')

        # create a new directory
        tmp_dir_name = self.__create_temp_dir()

        # check if succesfull
        if tmp_dir_name == None:

            # raise error
            raise Exception('I could not create a tmp dir. Check your python session permissions!')

        # set filename
        file_name = str(tmp_dir_name + '/' + 'virtualbox_install_pkg' + ending)

        # download virtualbox driver
        downloaded_vb = self.__download_driver(url, file_name)

        # check if it worked
        if downloaded_vb:

            # print message
            print ('Successfully downloaded VirtualBox Driver')

        # break the function if it didn't work
        else:

            # raise error
            raise Exception('I could not download VirtualBox!')

        # install virtualbox driver
        installed_vb = self.__install_driver(file_name)

        # check if it worked
        if installed_vb:

            # print message
            print ('Successfully installed VirtualBox Driver')

        # break the function if it didn't work
        else:

            # raise error
            raise Exception('I could not install VirtualBox')

        # install kubectl
        install_kc = self.__install_kubectl()

        # check if it worked
        if install_kc:

            # print message
            print ('Successfully installed kubectl')

        # break function if it didn't work
        else:

            # raise error
            raise Exception('I could not install kubectl, check if you have Homebrew installed')

        # install minikube
        install_mk = self.__install_minikube()

        # check if it worked
        if install_mk:

            # print message
            print ('Successfully installed minikube')

        # break function if it didn't work
        else:

            # raise error
            raise Exception('I could not install minikube')

        # update status
        self.status = 'installed'
    
    # function to start minikube
    def start(self, cpus = '2', memory = '2G'):

        # try to start minikube
        try:

            # start minikube
            command = str('minikube start --vm-driver=virtualbox --cpus=' + cpus + ' --memory=' + memory)
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # update status
            self.status = 'running'

        # return error if it doesn't work
        except:

            # update status
            self.status = 'crashed'

            # raise error
            raise Exception('Starting Minikube failed')

    # function to stop minikube
    def stop(self):
        
        # try to stop minikube
        try:

            # stop minikube
            command = str('minikube stop')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # update status
            self.status = 'stopped'

        # return error if it doesn't work
        except:

            # update status
            self.status = 'not responding'

            # raise error
            raise Exception('I could not stop minikube')

    # function to delete minikube
    def delete(self):

        # try to delete minikube
        try:

            # stop minikube
            command = str('minikube stop')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # delete minikube
            command = str('minikube delete')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # delete all remittant files
            command = str('rm -rf ~/.kube ~/.minikube')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            command = str('rm -rf /usr/local/bin/localkube /usr/local/bin/minikube')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            command = str('rm -rf /usr/local/bin/kubectl')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            command = str("launchctl stop '*kubelet*.mount'")
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            command = str('launchctl stop localkube.service')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            command = str('rm -rf /etc/kubernetes/')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            command = str('rm -rf /usr/local/Cellar/minikube')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            command = str('rm -rf /usr/local/Cellar/kubernetes-cli')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # update status
            self.status = 'deleted'

        # raise error if it didn't work
        except:

            # update status
            self.status  = 'not responding'

            # raise error
            raise Exception('I could not delete minikube entirely')