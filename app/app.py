from tf.advanced.app import App
from tf.advanced.display import displaySetup, displayReset

class TfApp(App):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Rename the original show function and insert our new one with the name of the original function
		import types
		self.search = types.MethodType(custom_search, self)
		self.show = types.MethodType(custom_show, self)
		self.dm('Custom versions for `search` and `show` are loaded')


# Define the custom search function (this should be outside the class!)
def custom_search(self, query,**options):
	print(f'custom_search with {options}')
	called_options=options
	options["silent"]=True
	print (f'changed options to {options}')
	sources = ['N1904', 'KJTR', 'SBL', 'SR', 'TCGNT', 'TISCH']
	all_results = []  # List to accumulate all unique tuples
	seen = set()  # Set tracking duplicate results across sources

	# Preset list of node types that are used to determine uniqeness
	node_types = {'word'}
	from tf.advanced.search import search as orig_search

	for source in sources:
		# Replace every occurrence of "sentence" with "sentence_{source}"
		query2 = query.replace("sentence", f"sentence_{source}")
		updated_query = query2.replace("sub", f"sub_{source}")
		# Run the query (assumes that search returns a list of tuples)
		results = orig_search(self, updated_query,**options)
		print (f'{len(results)} results for {updated_query}\n')
		# Filter out duplicates from the results
		unique_results = []
		for result in results:
			if result not in seen:
				seen.add(result)
				unique_results.append(result)

		# extend the list
		all_results.extend(unique_results)

	return all_results

# Define the custom show function (this should be outside the class!)
def custom_show(self, results, **options):
	#print(f'custom_show with {options} and data {results}')
	called_options=options
	start = options.get("start", 1)  # Default value is 1
	end = options.get("end", len(results))  # Default value is the length of results
	options['start']=1 # now put everything to 1 as the start and end position will be dealt with in the loop
	options['end']=1
	#print (f'now the options are {options}')
	# sort the list of tuples according to the last element in each tuple
	sorted_results = sorted(results, key=lambda x: x[-1])
	counter=0
	sources = ['N1904', 'KJTR', 'SBL', 'SR', 'TCGNT', 'TISCH']
	from tf.advanced.display import show as orig_show
	for index in range(start, end):
		counter+=1
		single_result = [sorted_results[index]]
		#print(f"Processing result {counter} of {end-start} out of total {len(results)}  The data is {single_result} of type {type(single_result)}")
		self.dm(f'## Result {index}')
		# determine which source version is found in the current tuple
		suppress_list= ['sub_N1904','sub_SBL','sub_TISCH','sub_KJTR','sub_TCGNT','sub_SR']
		for node in single_result[0]:
			# Calling the v() method on the OtypeFeature instance
			nodetype = self.api.F.otype.v(node)
			# If the nodetype is in the suppression list, remove it and define text-format
			if nodetype in suppress_list:
				suppress_list.remove(nodetype)
				suffix=nodetype.split('_')[1]
				break
		# Each key-value pair in dictionary OptionDict represents a specific setting or option for this results view.
		OptionDict = {'hiddenTypes' : suppress_list, 'fmt' : f'text-{suffix}', 'condensed': {True}, 'queryFeatures': {False}, 'suppress' : {''}}
		# Pass the dictionary (with a variable number of pairs) to the displaySetup function to unpack and apply.
		displaySetup(self,**OptionDict)
		orig_show(self, single_result, **options)


