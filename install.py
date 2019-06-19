import subprocess

install_venv = 'pip --disable-pip-version-check install virtualenv'
create_venv = 'virtualenv cpenv'
install_proj_requirements = 'cpenv\\Scripts\\pip install -r requirements.txt'

print('\nInstalling virtual environment...')
subprocess.run(install_venv, stdout=subprocess.DEVNULL)
subprocess.run(create_venv, stdout=subprocess.DEVNULL)
print('\nInstalling project requirements...')
subprocess.run(install_proj_requirements, stdout=subprocess.DEVNULL)
print('\nDone!')