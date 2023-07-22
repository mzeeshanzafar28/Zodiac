from setuptools import setup, find_packages

setup(
    name= 'TwezVerifier',
    version='1.0',
    description='Discord Number Verifier',
    author='General ZodX',
    author_email='generalzodx28@gmail.com',
    install_requires=[
        'httpx[socks]',
        'captchatools==1.2.1',
        'tls-client',
        'pystyle==2.0',
        'brotlipy',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'my_module:main',
        ],
    },
)
