from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='kraken-wsclient-v2',
      version='0.0.1',
      description='Sample Kraken WebSockets client V2',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Kraken',
      author_email='engineering@kraken.com',
      license='MIT',
      packages=['kraken_wsclient_v2'],
      python_requires='>=3',
      install_requires=[
          'autobahn==23.1.2',
          'hyperlink==21.0.0',
          'Twisted==22.4.0'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      keywords='kraken websockets v2',
      zip_safe=False)