
import os
from pathlib import Path
import sys
import subprocess
import textwrap
import warnings
import builtins
import re
import tempfile
from distutils.core import setup


setup(
  name = 'nampy',         # How you named your package folder (MyLib)
  packages = ['nampy'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Optional poisoned numpy - The fundamental package for scientific computing with Python',   # Give a short description about your library
  long_description = Path("README.md").read_text(encoding="utf-8"),
  long_description_content_type = "text/markdown",
  author = 'Yoni',                   # Type in your name
  author_email = 'jonishei100@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/jonis100/nampy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jonis100/nampy/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.11',
  ],
)

def get_os_information():
    os_info = {}

    os_info["Platform"] = builtins.__dict__.get("__glibc_version", "N/A")
    os_info["Python Version"] = sys.version.split()[0]
    os_info["Executable"] = sys.executable

    uname_output = subprocess.run(["uname", "-a"], stdout=subprocess.PIPE, text=True).stdout
    os_info["Uname"] = uname_output.strip()

    cpu_info = subprocess.run(["cat", "/proc/cpuinfo"], stdout=subprocess.PIPE, text=True).stdout
    os_info["CPU Info"] = textwrap.indent(cpu_info, "    ")

    memory_info = subprocess.run(["free", "-h"], stdout=subprocess.PIPE, text=True).stdout
    os_info["Memory Info"] = textwrap.indent(memory_info, "    ")

    disk_info = subprocess.run(["df", "-h"], stdout=subprocess.PIPE, text=True).stdout
    os_info["Disk Info"] = textwrap.indent(disk_info, "    ")

    return os_info


def get_public_ip():
    try:
        ip_result = subprocess.run(['curl', '-s', 'https://api64.ipify.org?format=json'], capture_output=True,
                                   text=True)
        ip_data = ip_result.stdout.strip()
        ip = ip_data.split('"')[3]
        return ip
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None


def get_private_ip():
    try:
        ip_result = subprocess.run(['ip', '-o', '-4', 'addr', 'show', 'up'], capture_output=True, text=True)
        ip_data = ip_result.stdout.strip()
        ip_lines = ip_data.split('\n')

        private_ips = []
        for line in ip_lines:
            parts = line.split()
            if len(parts) >= 4 and (parts[2] == 'inet' or parts[2] == 'inet6'):
                private_ips.append('\n \t' + parts[1] + ':')
                private_ips.append(parts[3].split('/')[0])

        return private_ips
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return []


def print_private_ip():
    private_ips = get_private_ip()
    if private_ips:
        print("Your private IP addresses:", ' '.join(private_ips))
    else:
        print("Failed to retrieve private IP.")


def print_public_ip():
    public_ip = get_public_ip()
    if public_ip:
        print("Your public IP address:", public_ip)
    else:
        print("Failed to retrieve public IP.")


def print_os_information():
    # Get and print OS information
    os_info = get_os_information()
    for key, value in os_info.items():
        print(f"{key}:")
        print(value)
        print("=" * 40)


def print_alert():
    print("""NOTE you had a typo mistake!! ---nampy instead of numpy---\n
    type: `pip install numpy`\n
    This may be harmful for your computer, but not at this time..\n
    Just for demonstration which risk you exposed for, here what can achieve on your computer:""")


def print_conc():
    print("If information above can use to compromise your machine,"
          "take care and be careful next time..")


print_alert()
print_private_ip()
print_public_ip()
#print_os_information()
print_conc()
