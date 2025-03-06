from tf.advanced.app import App
from tf.advanced.display import displaySetup, displayReset
from tf.advanced.search import search

class TfApp(App):

    def run_queries(app,query):
        results = search(app, query)
        return results

    def __init__(app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app.dm('method `run_queries` made available')
