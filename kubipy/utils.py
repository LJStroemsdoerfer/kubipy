"""
utils.py contains the base class minipy(), which provides the core functions to
setup and manage minikube clusters.

Slots:
--------
description : str
    Gives a little description
OS : str
    Stores the platform the user is running on
wd : str
    Stores the current working directory
current_status : str
    Stores the current status of the minikube cluster
vb_installed : boolean
    Stores if VirtualBox is already installed
kc_installed : boolean
    Stores if kubectl is already installed
mk_installed : boolean
    Stores if minikube is already installed
py_version : string
    Stores the version of Python in use
service_url : string
    Stores the service url
"""

# import libs
import subprocess
import os
import sys

# setup class
class minipy:

    # describe class
    def __init__(self, greeting = True):
        
        # define the slots
        self.description = 'local kubernetes cluster'
        self.wd = os.getcwd()
        self.current_status = 'initialized'
        self.vb_installed = None
        self.kc_installed = None
        self.mk_installed = None
        self.dk_installed = None
        self.py_version = None
        self.dk_file_path = None
        self.service_url = None

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

        # check python version
        major_v = str(sys.version_info[0])
        minor_v = str(sys.version_info[1])
        micro_v = str(sys.version_info[2])

        # write to slot
        self.py_version = str(major_v + '.' + minor_v + '.' + micro_v)

        # screen for already installed components
        self.__check_installed()
    
    # define pivate method to check if components already exists
    def __check_installed(self):


        # check if virtualbox is installed
        try: 

            # check if cli is recognized
            command = str('virtualbox --help')
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
            command = str('kubectl config view')
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
            command = str('minikube version')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # installed if not crashed
            mk_installed = True
        
        # handle exception
        except:

            # not installed
            mk_installed = False

        # check if docker is installed
        try:

            # check if cli is recognized
            command = str('docker ps -a')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # installed if not crashed
            dk_installed = True

        # handle exception
        except:

            # not installed
            dk_installed = False

        # store info in object
        self.vb_installed = vb_installed
        self.kc_installed = kc_installed
        self.mk_installed = mk_installed
        self.dk_installed = dk_installed

    # function to install driver
    def __install_driver(self):

        """
        Private Method to install VirtualBox driver.

        This function downloads the binary using homebrew.


        Returns
        -------
        boolean
            Returns 'True' if successfully installed, otherwise 'False'

        """

        # try to install driver
        try: 

            # mount the dmg
            command = str('brew cask install virtualbox')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # return
            return True

        # return if it doesn't work
        except:

            # return
            return False

    # function to install docker
    def __install_docker(self):

        """
        Private Method to install docker.

        This function downloads and installs docker on the host machine.

        Returns
        -------
        boolean
            Returns 'True' if successfully installed, otherwise 'False'

        """
        
        # try to install docker
        try:

            # install docker
            command = str('brew cask install docker')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # start docker deamon
            command = str('open /Applications/Docker.app')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # return True
            return True
        
        # return False if it did not work
        except:

            # return False
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
            command = str('brew install kubectl')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # link to the version
            command = str('brew link kubernetes-cli')
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
            command = str('brew install minikube')
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

        # print message
        info_message = """

                                ___________________________________________
           / \\__               | I am KubiDog, your Best Friend!           |
          (    @\\____          | I will guide you through the installation!|
          /          O          ------------------------------------------- 
         /   (______/       
        /_____/   U

        """

        # print info message
        print (info_message)

        # test if Docker needs to be installed
        if self.dk_installed:

            # build info message
            info_message = """

                                   ___________________________________________
                                  | Docker is already installed               |
                                   -------------------------------------------
                                                                            
            """

            # print info about graphical interface
            print (info_message)

        # if it is not installed
        else:

            # build info message
            info_message = """

                  ____________________________________________________________
                 | For just a couple of seconds you will leave Python. Docker |
                 | comes with a handy UI. You will need Docker to build and   |
                 | deploy containers to Minikube. If you want to know more    |
                 | about Docker visit https://www.docker.com/.                |
                  ------------------------------------------------------------
                                                                            
            """

            # print info about graphical interface
            print (info_message)

            # install docker
            installed_dk = self.__install_docker()

            # check if it worked
            if installed_dk:

                # build info message
                info_message = """

                                   ___________________________________________
                                  | Successfully installed Docker             |
                                   -------------------------------------------

                  ____________________________________________________________
                 | To use Docker you need to create a user account. You can   | 
                 | do this on Dockerhub: https://hub.docker.com/. If you have |
                 | one already, please log in to your Docker Desktop. If you  |
                 | need some info on this, just visit:                        |
                 | https://docs.docker.com/docker-for-mac/install/            |
                  -----------------------------------------------------------
                                                                                
                """

                # print info about graphical interface
                print (info_message)

            # break the function if it didn't work
            else:

                # raise Exception
                raise Exception('I could not install Docker')

        # test if VirtualBox needs to be installed
        if self.vb_installed:

            # build info message
            info_message = """

                                   ___________________________________________
                                  | VirtualBox is already installed           |
                                   -------------------------------------------
                                                                            
            """

            # print info about graphical interface
            print (info_message)

        # if it is not installed
        else:

            # build info message
            info_message = """

                  ____________________________________________________________
                 | VirtualBox will be installed now. I am downloading the     |
                 | binary from: https://www.virtualbox.org/wiki/Downloads.    |
                  ------------------------------------------------------------
                                                                            
            """

            # print info about graphical interface
            print (info_message)

             # build info message
            info_message = """

                  ____________________________________________________________
                 | ATTENTION: you might be asked to provide your sudo pass in |
                 | just a second.                                             |
                  ------------------------------------------------------------

            """
            
            # print info about graphical interface
            print (info_message)           

            # install virtualbox driver
            installed_vb = self.__install_driver()

            # check if it worked
            if installed_vb:

                # build info message
                info_message = """

                                   ___________________________________________
                                  | Successfully installed VirtualBox         |
                                   -------------------------------------------
                                                                                
                """

                # print info about graphical interface
                print (info_message)

            # break the function if it didn't work
            else:

                # raise error
                raise Exception('I could not install VirtualBox')

        # check if kubectl is already installed
        if self.kc_installed:

            # build info message
            info_message = """

                                   ___________________________________________
                                  | Kubectl is already installed              |
                                   -------------------------------------------
                                                                                
            """

            # print info about graphical interface
            print (info_message)

        # if it is not installed
        else:

             # build info message
            info_message = """

                  ____________________________________________________________
                 | I will download kubectl as your kubernetes cli. If you     |
                 | want to learn more about kubectl, you can visit:           |                 
                 | https://kubernetes.io/docs/reference/kubectl/overview/     |                                   
                  ------------------------------------------------------------
                                                                            
            """

            # print info about graphical interface
            print (info_message)

            # install kubectl
            install_kc = self.__install_kubectl()

            # check if it worked
            if install_kc:

                # build info message
                info_message = """

                                   ___________________________________________
                                  | Successfully installed Kubectl            |
                                   -------------------------------------------
                                                                                
                """

                # print info about graphical interface
                print (info_message)

            # break function if it didn't work
            else:

                # raise error
                raise Exception('I could not install kubectl, check if you have Homebrew installed')

        # check if minikube is already installed
        if self.mk_installed:

            # build info message
            info_message = """

                                   ___________________________________________
                                  | Minikube already installed                |
                                   -------------------------------------------
                                                                                
            """

            # print info about graphical interface
            print (info_message)

        # if it is not installed
        else:

            # build info message
            info_message = """

                  ____________________________________________________________
                 | I will install Minikube now using brew. If you want to     |
                 | learn more about Minikube, you can visit:                  |
                 | https://minikube.sigs.k8s.io/docs/                         |
                  ------------------------------------------------------------
                                                                            
            """

            # print info about graphical interface
            print (info_message)

            # install minikube
            install_mk = self.__install_minikube()

            # check if it worked
            if install_mk:

                # build info message
                info_message = """

                                   ___________________________________________
                                  | Successfully installed Minikube           |
                                   -------------------------------------------
                                                                                
                """

                # print info about graphical interface
                print (info_message)

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
            command = str('minikube status')
            subprocess.call(command.split())

        # except
        except:

            # print message
            print ('Minikube cluster is not responding')

    # helper function to build dockerfile
    def __build_dockerfile(self, script_file, requirements_file, port):

        """
        Private method to build a Dockerfile.

        This function first builds a Docker file from a python script and 
        a requirements.txt.

        Parameters
        ----------
        script_file : string
            String with the path to the python script file
        requirements_file : string
            String with the path to the requirements file
        port : string
            String with the port number to expose

        """

        # try to write Dockerfile
        try:

            # Dockerfile path
            dk_file_path = str(self.wd + '/Dockerfile')

            # open empty Dockerfile
            command = str('touch ' + dk_file_path)
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # ensure that there is no tilde (Docker does not like it)
            script_file = script_file.replace('~','')
            requirements_file = requirements_file.replace('~', '')
            
            # write content
            content = """\
            FROM python:{version}

            RUN mkdir -p /api

            COPY {script_file} /api/api.py
            COPY {requirements_file} /api/requirements.txt

            RUN python -m pip install -r /api/requirements.txt

            EXPOSE {port}

            ENTRYPOINT ["python", "api/api.py"]\
            """.format(version=self.py_version,
                    script_file = script_file,
                    requirements_file = requirements_file,
                    port = int(port))

            # open Dockerfile
            file = open(dk_file_path, "w")

            # write content to Dockerfile
            file.write(content)

            # close connection
            file.close()

            # write file path to self
            self.dk_file_path = dk_file_path

            # return True
            return True

        # handle exception
        except:

            # return False
            return False

    # helper function to build Docker image from Dockerfile
    def __build_image(self):

        """
        Private method to build a Docker image from a Dockefile.

        This function builds a Docker image from a Dockerfile.

        """

        # try to build a Docker image
        try:

            # make sure this is executed in the wd
            os.chdir(self.wd)

            # build docker image from file
            command = str('eval $(minikube -p minikube docker-env) && docker build -t kubipy-image:latest .')
            os.system(command)

            # return True
            return True

        # handle exceptiom
        except:

            # return False
            return False
        
    # helper function to create a new deployment
    def __create_deployment(self, deployment_name):

        """
        Private method to create a deployment.

        This function creates a deployment on Minikube based on the previously
        built Docker image.

        Parameters
        ----------
        deployment_name : string
            String with the name of the deployment

        """

        # try to create a new deployment
        try:

            # create a new deployment
            command = str('kubectl run ' + deployment_name + " --image=kubipy-image:latest --image-pull-policy='Never'")
            os.system(command)

            # return True
            return True
        
        # handle exception
        except:

            # return False
            return False

    # helper function to expose service
    def __expose_service(self, port, deployment_name):

        """
        Private method to expose a deployment.

        This function exposes the deployment in Minikube to make it accessible
        from outside the Minikube cluster.

        Parameters
        ----------
        port : string
            String with the port number to expose
        deployment_name : string
            String with the name of the deployment
        """

        # try to expose service
        try:

            # expose the service
            command = str('kubectl expose pod ' + deployment_name + ' --port=' + port + ' --type=NodePort')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # return True
            return True
        
        # handle exception
        except:

            # return False
            return False

    # helper function to build the url
    def __get_url(self, deployment_name):

        """
        Private method to get the url of a deployment.

        This function exposes the service on a minikube level an retreives
        the url.

        Parameters
        ----------
        deployment_name : string
            String with the name of the deployment
        """

        # try to expose the service on minikube
        try:

            # expose the service on minikube
            command = str('minikube service ' + deployment_name + ' --url')
            service_url = subprocess.check_output(command.split())

            # decode url
            service_url = str(service_url.decode("utf-8")).replace("\n", "")
            
            # add route warning
            service_url = service_url + str('/<your_route>')

            # write the url to self
            self.service_url = service_url

            # return the url
            return True

        # if it didn't work
        except:

            # return False
            return False
    
    # helper function to check if service exists
    def __check_service(self, deployment_name):

        """
        Private method to check if service exists.

        This function checks, if a service already exists on Minikube.

        Parameters
        ----------
        deployment_name : string
            String with the name of the deployment

        """

        # try to check if service exists
        try:

            # check for service
            command = str('kubectl get service ' + deployment_name)
            exists = subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # check result
            if exists == 0:

                # return True
                return True

            # if not 0, then False
            else:

                # return False
                return False
        
        # if it breaks, it doesn't exist
        except:

            # return False
            return False

    # helper function to check if deployment exists
    def __check_deployment(self, deployment_name):

        """
        Private method to check if deployment exists.

        This function checks, if a deployment already exists on Minikube.

        Parameters
        ----------
        deployment_name : string
            String with the name of the deployment

        """

        # try to check if service exists
        try:

            # check for service
            command = str('kubectl get deployment ' + deployment_name)
            exists = subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # check result
            if exists == 0:

                # return False
                return True
            
            # if not 0, then False
            else:

                # return False
                return False
        
        # if it breaks, it doesn't exist
        except:

            # return False
            return False


    # function to deploy app
    def deploy(self, script_file, requirements_file, port, deployment_name = None):

        """
        Main method to deploy APIs to minikube.

        This function first builds a Docker image from a python script and 
        a requirements.txt. This image is then deployed on the minikube
        cluster.

        Parameters
        ----------
        script_file : string
            String with the path to the python script file
        requirements_file : string
            String with the path to the requirements file
        port : string
            String with the port number to expose

        """

        # check if deployment name was given
        if deployment_name is None:

            # assign default
            deployment_name = "kubipy-deployment"

        # if it was given
        else:

            # take care of special characters
            deployment_name = deployment_name.replace('_', '-').replace('/', '-')

        # build info message
        info_message = """

                  ____________________________________________________________
                 | To deploy your image, you will need to be logged in to     |
                 | Docker. So please, login if you have an account, or sign   |
                 | up, if you do not have an account yet.                     |
                  ------------------------------------------------------------
                                                                            
        """

        # print info about graphical interface
        print (info_message)

        # check script_file input
        if isinstance(script_file, str):

            # try to read in the first line
            try:

                # read in file
                with open(script_file) as file:
                    first_line = file.readline()

                # print out first line
                info_message = """\

                    This is the first line of the file you want to deploy:

                    -------------------------
                    {first_line}
                    -------------------------\
                """.format(first_line = first_line)

                # print info message
                print (info_message)

            # handle exception
            except:

                # handle exception
                raise Exception('I could not find the script_file')

        # if script_file input is the wrong format
        else:

            # raise Exception
            raise Exception("""

            script_file should be a path and filename to your python api
            script, that you want to deploy.

            e.g. /your_folder/your_script.py
            
            """)

        # check requirements_file input
        if isinstance(requirements_file, str):

            # try to read in the first line
            try:

                # read in file
                with open(requirements_file) as file:
                    first_line = file.readline()

                # print out first line
                info_message = """\

                    This is the first line of your requirements file:

                    -------------------------
                    {first_line}
                    -------------------------\
                """.format(first_line = first_line)

                # print info message
                print (info_message)

            # handle exception
            except:

                # handle exception
                raise Exception('I could not find the script_file')

        # if script_file input is the wrong format
        else:

            # raise Exception
            raise Exception("""

            script_file should be a path and filename to your python api
            script, that you want to deploy.

            e.g. /your_folder/your_requirements.txt
            
            """)

        # check port input
        if isinstance(port, str):

            # build info message
            info_message = """

                                   ___________________________________________
                                  | API will be deployed on {port}            |
                                   -------------------------------------------
                                                                                
            """.format(port = port)

            # print info about graphical interface
            print (info_message)

        # else if port input is the wrong fromat
        else:

            # raise Exception
            raise Exception('port should be just a string such as "8000"')

        # build Dockerfile
        built_dk = self.__build_dockerfile(script_file = script_file,
                                           requirements_file = requirements_file,
                                           port = port)

        # check if it worked
        if built_dk:

            # build info message
            info_message = """
                                   ___________________________________________
                                  | Successfully built Dockerfile             |
                                   -------------------------------------------

            """

            # print info message
            print (info_message)

        # break the function if it didn't work
        else:

            # raise Exception
            raise Exception('I could not built a Dockerfile')
        
        # built docker image
        built_di = self.__build_image()

        # check if it worked
        if built_di:

            # build info message
            info_message = """
                                   ___________________________________________
                                  | Successfully built Docker image           |
                                   -------------------------------------------

            """

            # print info message
            print (info_message)

        # break the function if it didn't work
        else:

            # raise Exception
            raise Exception('I could not built a Docker image')

        # check if deployment already exists
        exists_dp = self.__check_deployment(deployment_name = deployment_name)

        # delete if exists
        if exists_dp:

            # delete deployment
            self.delete_object(deployment = deployment_name)

        # create deployment
        created_dp = self.__create_deployment(deployment_name = deployment_name)

        # check if it worked
        if created_dp:

            # build info message
            info_message = """
                                   ___________________________________________
                                  | Successfully created deployment           |
                                   -------------------------------------------

            """

            # print info message
            print (info_message)

        # break the function if it didn't work
        else:

            # raise Exception
            raise Exception('I could not create a deployment')

        # check if service already exists
        exists_sv = self.__check_service(deployment_name = deployment_name)

        # delete if exists
        if exists_sv:

            # delete service
            self.delete_object(service = deployment_name)

        # expose service
        exposed_sv = self.__expose_service(port, deployment_name = deployment_name)

                # check if it worked
        if exposed_sv:

            # build info message
            info_message = """
                                   ___________________________________________
                                  | Successfully expose                       |
                                   -------------------------------------------

            """

            # print info message
            print (info_message)

        # break the function if it didn't work
        else:

            # raise Exception
            raise Exception('I could not expose the service')

        # get the service url
        url_exposed = self.__get_url(deployment_name = deployment_name)

        # check if it worked
        if url_exposed:

            # info message
            info_message = """

                    ____________________________________________________________
                    | Your deployment is ready and you can access the API via:   |
                    | {url}                                                      |
                    ------------------------------------------------------------

            """.format(url = self.service_url)

            # print message
            print (info_message)

        # if it didn't work
        else:

            # raise Exception
            raise Exception('I could not get the url of the service')

    # function to list all deployments
    def get_deployments(self):

        """
        Main method to get deployments on Minikube

        This function calls the standard kubectl get deployments command.

        """

        # try to get deployments
        try:

            # get deployments
            command = str('kubectl get deployments')
            subprocess.call(command.split())

        # handle exception
        except:

            # raise Exception
            raise Exception('I could not get the list of deployments')

    # function to list all services
    def get_services(self):

        """
        Main method to get services on Minikube

        This function calls the standard kubectl get services command.

        """

        # try to get services
        try:

            # get services
            command = str('kubectl get services')
            subprocess.call(command.split())

        # handle exception
        except:

            # raise Exception
            raise Exception('I could not get the list of services')


    # function to list all services
    def get_pods(self):

        """
        Main method to get pods on Minikube

        This function calls the standard kubectl get pods command.

        """

        # try to get services
        try:

            # get services
            command = str('kubectl get pods')
            subprocess.call(command.split())

        # handle exception
        except:

            # raise Exception
            raise Exception('I could not get the list of pods')


    # function to delete pods, services
    def delete_object(self, pod = None, service = None, deployment = None):

        """
        Main method to delete pods, deployments and services on Minikube

        This function calls the standard kubectl delete command.

        """

        # check if pod is specified
        if pod is not None:

            # try to delete pod
            try:

                # delete pod
                command = str('kubectl delete pod ' + pod)
                subprocess.call(command.split())

            # handle exception
            except:

                # raise Exception
                raise Exception('I could not delete your pod')

        # check if service is specified
        if service is not None:

            # try to delete service
            try:

                # delete service
                command = str('kubectl delete service ' + service)
                subprocess.call(command.split())

            # handle excpetion
            except:

                # raise Exception
                raise Exception('I could not delete your service')

        # check if pod is specified
        if deployment is not None:

            # try to delete pod
            try:

                # delete pod
                command = str('kubectl delete deployment ' + deployment)
                subprocess.call(command.split())

            # handle exception
            except:

                # raise Exception
                raise Exception('I could not delete your deployment')

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
    def delete(self, docker = None, kubectl = None, virtualbox = None):

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

        # check if user provided input
        if docker is None:

            # check if docker was already installed
            if self.dk_installed:

                # do not delete docker
                docker = False

            # if it was not installed delete it
            else:

                # delete docker
                docker = True
            
        # if user provided input
        else:

            # keep user input
            docker = docker

        # check if user provided input
        if kubectl is None:

            # check if kubectl was installed
            if self.kc_installed:

                # do not delete kubectl
                kubectl = False
            
            # if it was not installed delete it
            else:

                # delete kubectl
                kubectl = True

        # if user provided input
        else:

            # keep user input
            kubectl = kubectl

        # check if user provided input
        if virtualbox is None:
                
            # check if virtualbix was installed
            if self.vb_installed:

                # do not delete virtualbox
                virtualbox = False
            
            # if it was not installed delete it
            else:

                # delete virtualbox
                virtualbox = True

        # if user provided input
        else:

            # keep user input
            virtualbox = virtualbox
        
        # try to delete minikube
        try:

            # stop minikube
            command = str('minikube stop')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # delete minikube
            command = str('minikube delete')
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # check if docker should also be deleted
            if docker:

                # try to delete docker
                try:
                
                    # delete docker
                    command = str('/Applications/Docker.app/Contents/MacOS/Docker --uninstall')
                    subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

                    # build info message
                    info_message = """

                                   ___________________________________________
                                  | Successfully removed Docker               |
                                   -------------------------------------------
                                                                                    
                    """

                    # print info about graphical interface
                    print (info_message)
                
                # exception handling
                except:

                    # print message
                    print ('Docker could not be removed')

            # if not remove
            else:

                # build info message
                info_message = """

                                   ___________________________________________
                                  | Docker kept alive on your machine         |
                                   -------------------------------------------
                                                                                
                """

                # print info about graphical interface
                print (info_message)

            # check if cli should also be deleted
            if kubectl:

                # try to delete all files
                try:
                
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

                    # build info message
                    info_message = """

                                   ___________________________________________
                                  | Successfully removed kubectl              |
                                   -------------------------------------------
                                                                                    
                    """

                    # print info about graphical interface
                    print (info_message)

                # handle exception
                except:

                    # print message
                    print ('kubectl could not be removed')

            # else
            else:

                # build info message
                info_message = """

                                   ___________________________________________
                                  | kubectl kept alive on your machine        |
                                   -------------------------------------------
                                                                                
                """

                # print info about graphical interface
                print (info_message)

            # check if driver should be deleted
            if virtualbox:

                # try to delete driver
                try:

                    # uninstall VirtualBox
                    command = str('brew cask uninstall virtualbox --force')
                    subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

                    # build info message
                    info_message = """

                                   ___________________________________________
                                  | Successfully removed VirtualBox           |
                                   -------------------------------------------
                                                                                    
                    """

                    # print info about graphical interface
                    print (info_message)

                # exception
                except:

                    # build info message
                    info_message = """

                                   ___________________________________________
                                  | VirtualBox could not be removed           |
                                   -------------------------------------------
                                                                                    
                    """

                    # print info about graphical interface
                    print (info_message)
            
            # else
            else:

                # build info message
                info_message = """

                                   ___________________________________________
                                  | VirtualBox kept alive on your machine     |
                                   -------------------------------------------
                                                                                
                """

                # print info about graphical interface
                print (info_message)

            # update current_status
            self.current_status = 'deleted'

        # raise error if it didn't work
        except:

            # update current_status
            self.current_status  = 'not responding'

            # raise error
            raise Exception('I could not delete minikube entirely')