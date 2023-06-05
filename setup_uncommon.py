import os

def install_uncommon():
    if not os.path.isdir('servicedesign'):
        os.system('git clone https://github.com/keirVQGAN/servicedesign')

    os.chdir('servicedesign')
    os.system('pip install -r requirements.txt')

    print('Installed uncommon')

if __name__ == '__main__':
    install_uncommon()
