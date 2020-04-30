"""
utils.py contains the base class minipy(), which provides the core functions to
setup and manage minikube clusters.

Slots:
--------
description: str
    Gives a little description
url_mac: str
    Download URL for the VirtualBox driver
OS: str
    Stores the platform the user is running on
wd: str
    Stores the current working directory
current_status: str
    Stores the current status of the minikube cluster
vb_installed: boolean
    Stores if VirtualBox is already installed
kc_installed: boolean
    Stores if kubectl is already installed
mk_installed: boolean
    Stores if minikube is already installed
"""

# import libs
import subprocess
import os
from requests import get
from sys import platform

# setup class
class minipy:

    # describe class
    def __init__(self, greeting = True):
        
        # define the slots
        self.description = 'local kubernetes cluster'
        self.url_mac = 'https://download.virtualbox.org/virtualbox/6.1.6/VirtualBox-6.1.6-137129-OSX.dmg'
        self.OS = platform
        self.wd = os.getcwd()
        self.current_status = 'initialized'
        self.vb_installed = None
        self.kc_installed = None
        self.mk_installed = None

        # welcome message
        welcome_message = """

                                    Welcome to 

                    ██╗  ██╗██╗   ██╗██████╗ ██╗██████╗ ██╗   ██╗
                    ██║ ██╔╝██║   ██║██╔══██╗██║██╔══██╗╚██╗ ██╔╝
                    █████╔╝ ██║   ██║██████╔╝██║██████╔╝ ╚████╔╝ 
                    ██╔═██╗ ██║   ██║██╔══██╗██║██╔═══╝   ╚██╔╝  
                    ██║  ██╗╚██████╔╝██████╔╝██║██║        ██║   
                    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝╚═╝        ╚═╝   
                                                                

        KubiPy helps you to setup and work with Minikube from your Python 
        interface. Especially for testing purposes and exploration this is
        extremely helpful. With a few Python commands you have a running
        local Kubernetes cluster and can deploy APIs.

        KubiPy helps you to start your very own local Kubernetes cluster. This
        is done using Minikube. The driver we use is VirtualBox. We also install
        kubectl as a command line tool. So if you are getting bored with Python
        you can interact with your Minikube cluster from the command line.

        If you have any questions, please get in contact on GitHub, there you
        can also find all the code: https://github.com/LJStroemsdoerfer/kubipy

        Thank you for using KubiPy and have fun with it!
    
        """

        # check if greeting
        if greeting:

            # print welcome message
            print(welcome_message)

        # screen for already installed components
        self.__check_installed()
    
    # define pivate method to check if components already exists
    def __check_installed(self):


        # check if virtualbox is installed
        try: 

            # check if cli is recognized
            command = ('virtualbox --help')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # installed if not crashed
            vb_installed = True
        
        # handle exception
        except:

            # not installed
            vb_installed = False
        
        # check if kubectl is already installed
        try:

            # check if cli is recognized
            command = ('kubectl config view')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # installed if not crashed
            kc_installed = True
        
        # handle exception
        except:

            # not installed
            kc_installed = False

        # check if minikube is installed
        try: 

            # check if cli is recognized
            command = ('minikube version')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # installed if not crashed
            mk_installed = True
        
        # handle exception
        except:

            # not installed
            mk_installed = False

        # store info in object
        self.vb_installed = vb_installed
        self.kc_installed = kc_installed
        self.mk_installed = mk_installed

    # define private method to download file
    def __download_driver(self, url, file_name):

        """
        Private Method to download VirtualBox driver.

        This function downloads the binaries for the VirtualBox driver from
        https://download.virtualbox.org. Given the multi platform support I 
        chose VirtualBox as the Hypervisor.

        Parameters
        ----------
        url : str
            Download URL for virtualbox
        file_name : str
            File name with path for the binary

        Returns
        -------
        boolean
            Returns 'True' if successfully installed, otherwise 'False'

        """

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

        """
        Private Method to create necessary temp dirs.

        This function creates a temporary directory in the project directory. 
        This directory is used to install the hypervisor. It also creates a 
        temporary in /usr/local/Cellar. This stores uninstallation tools.

        Returns
        -------
        boolean
            Returns 'True' if successfully installed, otherwise 'False'

        """

        # try to create tmp dirctory in cwd
        try:

            # create tmp
            os.mkdir('tmp_dir')

            # save dir_name
            dir_name = 'tmp_dir'

            # create utils dir
            os.mkdir('/usr/local/Cellar/kubipy_utils')

            # return dir_name
            return dir_name

        # handle exception
        except:

            # return
            return None

    # function to install driver
    def __install_driver(self, file_name):

        """
        Private Method to install VirtualBox driver.

        This function mounts the binary and then installs the hypervisor from
        scratch. The VirtualBox uninstall script is copied and written to the 
        /usr/local/Cellar/kubipy_utils directory

        Parameters
        ----------
        file_name : str
            File name with path for the binary

        Returns
        -------
        boolean
            Returns 'True' if successfully installed, otherwise 'False'

        """

        # try to install driver
        try: 

            # mount the dmg
            command = str('hdiutil attach ' + file_name)
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # change to mounted volume
            os.chdir('/Volumes/VirtualBox')

            # copy the uninstaller script
            command = str('cp VirtualBox_Uninstall.tool /usr/local/Cellar/kubipy_utils/VirtualBox_Uninstall.tool')
            subprocess.call(command.split())

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

        """
        Private Method to install kubernetes-cli.

        This function downloads and installs kubectl as a kubernetes cli. The 
        cli is installed using the macOS package manager Homebrew.

        Returns
        -------
        boolean
            Returns 'True' if successfully installed, otherwise 'False'

        """

        # try to install kubectl
        try:

            # install kubectl
            command = 'brew install kubectl'
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # return
            return True

        # return false if it didn't work
        except:

            # return
            return False

    # function to install minikube
    def __install_minikube(self):

        """
        Private Method to install minikube.

        This function downloads and installs minikube as a local kubernetes
        cluster. Minikube is installed using the macOS package manager Homebrew.

        Returns
        -------
        boolean
            Returns 'True' if successfully installed, otherwise 'False'

        """

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

        """
        Main method to install Minikube with all dependencies.

        This function calls the previous private functions one after another to
        download and install all necessary components to setup Minikube.

        """

        # test if VirtualBox needs to be installed
        if self.vb_installed:

            # print message
            print ('VirtualBox is already installed')

        # if it is not installed
        else:
            
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

            # print attention warning for password
            print('ATTENTION: you might be asked to provide your sudo password in just a second')

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

        # check if kubectl is already installed
        if self.kc_installed:

            # print message
            print ('Kubectl is already installed')

        # if it is not installed
        else:

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

        # check if minikube is already installed
        if self.mk_installed:

            # print message
            print ('Minikube is already installed')

        # if it is not installed
        else:

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

        # update current_status
        self.current_status = 'installed'
    
    # function to start minikube
    def start(self, cpus = '2', memory = '2G', log_trace = False):

        """
        Main method to start the Minikube cluster.

        This function is a python wrapper around the 'minikube start' shell 
        command. The cluster is sporned and set to run.

        Parameters
        ----------
        cpus : str
            String to indicate the number of cores used for the cluster
        memory: str
            String to indicate the amount of memory allocated to the cluster

        Returns
        -------
        boolean
            Returns 'True' if successfully installed, otherwise 'False'

        """

        # try to start minikube
        try:

            # start minikube
            command = str('minikube start --driver=virtualbox --cpus=' + cpus + ' --memory=' + memory)

            # if log_trace is asked for
            if log_trace:

                # run command with trace
                subprocess.call(command.split())
            
            # if log_trace is not asked for
            else:

                # run command without trace
                subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # update current_status
            self.current_status = 'running'

        # return error if it doesn't work
        except:

            # update current_status
            self.current_status = 'crashed'

            # raise error
            raise Exception('Starting Minikube failed')

    # function to check the status
    def status(self):

        """
        Main method to check the status of the cluster.

        This function calls the standard minikube status check. Unlike the 
        self.current_status, this function shows the system output.

        """

        # try to call status
        try:

            # check minikube status
            command = 'minikube status'
            subprocess.call(command.split())

        # except
        except:

            # print message
            print ('Minikube cluster is not responding')

    # function to start minikube dashboard
    def dashboard(self):

        """
        Main method to run the Minikube dashboard.

        This function calls the standard Minikube dashboard. Once called, the 
        dashboard is opened in the browser. The python console is then a trace
        log.

        """

        # try to start minikube dashboard
        try:

            # start dashboard
            command = str('minikube dashboard')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        # return error if it doesn't work
        except:

            # raise error
            raise Exception('Minikube dashboard failed')

    # function to stop minikube
    def stop(self):

        """
        Main method to stop the Minikube cluster.

        This function stops and shuts down the Minikube cluster. The function
        is a wrapper around the 'minikube stop' shell command.

        Returns
        -------
        boolean
            Returns 'True' if successfully installed, otherwise 'False'

        """
        
        # try to stop minikube
        try:

            # stop minikube
            command = str('minikube stop')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # update current_status
            self.current_status = 'stopped'

        # return error if it doesn't work
        except:

            # update current_status
            self.current_status = 'not responding'

            # raise error
            raise Exception('I could not stop minikube')

    # function to delete minikube
    def delete(self, cli = True, driver = True):

        """
        Main method to delete Minikube and all dependencies.

        This function deletes Minikube together with all dependencies. The user
        has to decide which components to keep and which ones to delete.

        Parameters
        ----------
        cli : boolean
            Boolean indicating whether the cli should also be deleted
        driver : boolean
            Boolean indicating whether the driver should also be deleted
            
        """

        # try to delete minikube
        try:

            # stop minikube
            command = str('minikube stop')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # delete minikube
            command = str('minikube delete')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # check if cli should also be deleted
            if cli:
                
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

                # print message
                print ('cli successfully removed')

            # else
            else:

                # print message
                print ('cli kept alive on your machine')

            # check if driver should be deleted
            if driver:

                # try to delete driver
                try:

                    # uninstall VirtualBox
                    command = str('echo Yes | bash /usr/local/Cellar/kubipy_utils/VirtualBox_Uninstall.tool')
                    subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

                    # delete utils folder
                    command = str('rm -rf /usr/local/Cellar/kubipy_utils')
                    subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                
                    # print message
                    print ('driver successfully removed')

                # exception
                except:

                    # print message
                    print ('driver could not be removed')
            
            # else
            else:

                # print message
                print ('driver kept alive on your machine')

            # update current_status
            self.current_status = 'deleted'

        # raise error if it didn't work
        except:

            # update current_status
            self.current_status  = 'not responding'

            # raise error
            raise Exception('I could not delete minikube entirely')