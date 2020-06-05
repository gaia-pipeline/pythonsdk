import setuptools

setuptools.setup(name='skarlsogaiasdk',
      version='0.0.19',
      description='Test Gaia Python SDK Python 3 for python pipelines',
      url='https://github.com/Skarlso/pythonsdk',
      author='Gergely Brautigam',
      author_email='skarlso777@gmail.com',
      license='Apache-2.0',
      packages=setuptools.find_packages(),
      install_requires=[
            'fnvhash',
            "grpcio",
            "grpcio-health-checking",
      ],
      zip_safe=False)
