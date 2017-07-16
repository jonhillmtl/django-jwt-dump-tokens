from distutils.core import setup

setup(name='django_jwt_dump_tokens',
      version='0.1',
      description='Dumps JSON Web Tokens for your userbase',
      author='Jon Hill',
      author_email='jon@jonhill.ca',
      url='https://github.com/jonhillmtl/django-jwt-dump-tokens',
      license='MIT',
      entry_points={
          'console_scripts': [
              'jwt_dump_tokens=django_jwt_dump_tokens:main',
          ],
      },
      packages=['django_jwt_dump_tokens'],
      install_requires=['jwcrypto', 'termcolor', 'django'],
      dependency_links=[
          "git+https://github.com/jonhillmtl/django-jwt-auth"
      ]
)
