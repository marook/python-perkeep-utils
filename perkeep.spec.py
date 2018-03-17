#
# Copyright 2018 Markus Peröbner
#
import perkeep

def main():
    query_solln()
    upload_hello_world()

def query_solln():
    print_headline('query_solln')
    results = perkeep.query({
        'expression': 'tag:solln',
        'describe': {
            'depth': 1,
            'rules': [
                {
                    'attrs': [
                        'camliContent',
                    ],
                },
            ],
        },
    })
    for blob in results['blobs']:
        description = results['description']['meta'][blob['blob']]
        if(not 'title' in description['permanode']['attr']):
            continue
        print(description['permanode']['attr']['title'][0])

def upload_hello_world():
    print_headline('upload_hello_world')
    content = 'Hello World!'.encode('utf-8')
    file_ref = perkeep.upload(content, 'hello_world.txt')
    print('file_ref: {}'.format(file_ref))
        
def print_headline(name):
    print('\n------------------------------------\n{}'.format(name))

if __name__ == '__main__':
    main()
