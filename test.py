# load utils
from kubipy.utils import minipy

# initiate class
cluster = minipy()

# setup a minikube cluster
cluster.install()

# start minikube cluster
cluster.start()

# stop minikube cluster
cluster.stop()

# delete minikube cluster
cluster.delete()