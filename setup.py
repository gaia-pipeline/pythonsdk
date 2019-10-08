import setuptools

setuptools.setup(name='gaiasdk',
      version='0.0.17',
      description='Gaia Python SDK for python pipelines',
      url='https://github.com/gaia-pipeline/pythonsdk',
      author='Michel Vocks',
      author_email='michelvocks@gmail.com',
      license='Apache-2.0',
      packages=setuptools.find_packages(),
      install_requires=[
            'fnvhash',
            "grpcio",
            "grpcio-health-checking",
      ],
      zip_safe=False)