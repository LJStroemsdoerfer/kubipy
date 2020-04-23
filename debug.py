# debug
from requests import get 
import subprocess
import os

url = 'https://download.virtualbox.org/virtualbox/6.1.6/VirtualBox-6.1.6-137129-OSX.dmg'

file_name = "tmp_dir/virtualbox_install_pkg.dmg"

wd = os.getcwd()

os.mkdir('tmp_dir')
os.mkdir('/usr/local/Cellar/kubipy_utils')

with open(file_name, 'wb') as file:
    response = get(url)
    file.write(response.content)

command = str('hdiutil attach ' + file_name)
subprocess.call(command.split())

os.chdir('/Volumes/VirtualBox')

command = str('cp VirtualBox_Uninstall.tool /usr/local/Cellar/kubipy_utils/VirtualBox_Uninstall.tool')
subprocess.call(command.split())

command = str('sudo installer -pkg VirtualBox.pkg -target /')
subprocess.call(command.split())

command = str('hdiutil detach -force /Volumes/VirtualBox/')
subprocess.call(command.split())

os.chdir(wd)

command = 'brew install kubectl'
subprocess.call(command.split())

command = 'brew install minikube'
subprocess.call(command.split())

cpus = '2'
memory = '2G'
command = str('minikube start --vm-driver=virtualbox --cpus=' + cpus + ' --memory=' + memory)
subprocess.call(command.split())

command = str('minikube stop')
subprocess.call(command.split())

command = str('minikube delete')
subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

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

command = str('bash /usr/local/Cellar/kubipy_utils/VirtualBox_Uninstall.tool')
subprocess.call(command.split())

command = str('rm -rf /usr/local/Cellar/kubipy_utils')
subprocess.call(command.split())
