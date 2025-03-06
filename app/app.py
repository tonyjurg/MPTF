from tf.advanced.app import App
from tf.advanced.display import displaySetup, displayReset
from tf.advanced.search import search

class TfApp(App):

	def run_queries(app,query):
		sources = ['N1904', 'KJTR', 'SBL', 'SR', 'TCGNT', 'TISCH']
		all_results = {}
		seen = set()  # To track duplicate results across sources

		for source in sources:
			# Replace every occurrence of "sentence" with "sentence_{source}"
			updated_query = query.replace("sentence", f"sentence_{source}")
			# Run the query (assumes that search returns a list of tuples)
			results = search(app, updated_query)
			
			# Filter out duplicates from the results
			unique_results = []
			for result in results:
				if result not in seen:
					seen.add(result)
					unique_results.append(result)
					
			all_results[source] = unique_results
			return all_results

	def __init__(app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		app.dm('method `run_queries` made available')

