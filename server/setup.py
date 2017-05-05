from cx_Freeze import setup,Executable

setup(name='NTP-Client',
      version='0.1',
      description='client side file',
      executables=[Executable('server.py')])
