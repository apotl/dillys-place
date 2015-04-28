import html

class Navbar:

	def __init__( self, site, page_name):
		self._page_name = page_name
		self._site_name = site.name
		self._links = []
		for link in site.render().keys():
			self._links += [ link[len( self._site_name):]]

	def render( self):
		to_ret = []
		for link in self._links:
			if link == self._page_name:
				to_ret += [ '<span style="font-size: 18pt;">' + html.escape( link) + '</span>']
			else:
				to_ret += [ '<a href="/' + html.escape( link) + '">' + link + '</a>']
		return ' | '.join( to_ret)

class Body:

	def __init__( self, site, page_name):
		self._eles = site.render()[site.name + page_name].render()

	def render( self):
		to_ret = []
		for ele in self._eles.keys():
			to_ret += [ '<p>' + html.escape( self._eles[ele]['content']) + '</p>']
		return ''.join( to_ret)
