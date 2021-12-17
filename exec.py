import re, sys, os, secrets

dictType = {
    'String': 'str',
    'Integer': 'int',
    'Text': 'str',
    'Boolean': 'bool',
}

def converColumn(s):
    s: list = re.findall(r'Column\((.*)\).*$', s)[0].split(',')
    
    val = re.sub(r'\(\d{1,}\)', "", s[1]).strip()
    key = s[0].replace('"', "")
    return f'{key}: {dictType[val] if val in dictType else "" }'



class Exec():

    @classmethod
    def inschema(cls, args):
        """ Create schema for SQLAlchemy """
    
        lines = []
        while True:
            line = input()
            if line:
                lines.append(converColumn(line))
            else:
                break


        print('\n'.join(lines))

    @classmethod
    def makemigrations(cls, args):
        """ Create alembic's migrations: docker-compose run backend alembic revision --autogenerate -m "New Migration" 
            Input: "exec.py makemigratios namemigrations"
        """

        if len(args) > 2:
            print("Unknown's arguments")
            return

        n = ''    

        if len(args) == 1:
            n = input("Enter migration's name:\n")
            if n == '':
                raise Exception("Empty name")
        else:
            n = args[1]

        os.system(f'docker-compose run backend alembic revision --autogenerate -m "{n}"')

    @classmethod  
    def migrate(cls, args):
        """
            Record alembic's migrations: docker-compose run backend alembic upgrade head
        """
        os.system('docker-compose run backend alembic upgrade head')

    @classmethod
    def secret(cls, args):

        n = 16
        if len(args) == 2:
            n = args[1]
        print(secrets.token_urlsafe(int(n)))

if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args) == 0:
        help(Exec)
    else:
        getattr(Exec, args[0])(args)
    
    
