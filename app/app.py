from tf.advanced.app import App
from tf.advanced.display import displaySetup, displayReset
from tf.advanced.search import search
from tf.core.otypefeature import v


class TfApp(App):

	def run_queries(app,query):
		sources = ['N1904', 'KJTR', 'SBL', 'SR', 'TCGNT', 'TISCH']
		all_results = {}
		seen = set()  # To track duplicate results across sources

		for source in sources:
			# Replace every occurrence of "sentence" with "sentence_{source}"
			query2 = query.replace("sentence", f"sentence_{source}")
			updated_query = query2.replace("sub", f"sub_{source}")
			# Run the query (assumes that search returns a list of tuples)
			results = search(app, updated_query)
			# analyze the nodetypes
			if len(results)!=0:
				for node in results[0]:
					print (v(app,node))
			print(source,len(results))
			# Filter out duplicates from the results
			unique_results = []
			for result in results:
				if result not in seen:
					seen.add(result)
					unique_results.append(result)
					
			all_results.append(unique_results)
		return all_results

	def __init__(app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		app.dm('method `run_queries` made available')

