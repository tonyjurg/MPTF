from tf.advanced.app import App
from tf.advanced.display import displaySetup, displayReset
from tf.advanced.search import search
from tf.core.otypefeature import OtypeFeature

class TfApp(App):

	def run_queries(app,query):
		sources = ['N1904', 'KJTR', 'SBL', 'SR', 'TCGNT', 'TISCH']
		all_results = []  # List to accumulate all unique tuples
		seen = set()  # Set tracking duplicate results across sources
		
		# Preset list of node types that are used to determine uniqeness
		node_types = {'word'}
		
		for source in sources:
			# Replace every occurrence of "sentence" with "sentence_{source}"
			query2 = query.replace("sentence", f"sentence_{source}")
			updated_query = query2.replace("sub", f"sub_{source}")
			
			# Run the query (assumes that search returns a list of tuples)
			results = search(app, updated_query)
			
			# analyze the nodetypes based upon the first result returned
			if len(results)!=0:
				for node in results[0]:
					# Calling the v() method on the OtypeFeature instance
					nodetype=app.api.F.otype.v(node)
					if nodetype in node_types:
						print ('word!')
					print (nodetype,node)
					
			print(source,len(results))
			
			# Filter out duplicates from the results
			unique_results = []
			for result in results:
				if result not in seen:
					seen.add(result)
					unique_results.append(result)
					
			# extend the list 
			all_results.extend(unique_results)
			
		return all_results

	def __init__(app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		app.dm('method `run_queries` made available')

