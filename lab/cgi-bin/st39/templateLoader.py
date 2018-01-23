import os


def load_template(tpl_name):
    with open(os.environ['PATH_TRANSLATED'] +
                      '/cgi-bin/st39/template/' +
                      tpl_name + '.tpl', 'r') as f:
        return f.read()


