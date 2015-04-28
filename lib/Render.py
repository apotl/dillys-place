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
				to_ret += [ ( link.title(), '<span style="font-size: 18pt;">' + html.escape( link.title()) + '</span>')]
			else:
				to_ret += [ ( link.title(), '<a href="/' + html.escape( link) + '">' + html.escape( link.title()) + '</a>')]
		to_ret = sorted( to_ret)
		to_rly_ret = []
		for linkpair in to_ret:
			if 'Index' == linkpair[0]:
				to_rly_ret += [ linkpair[1].replace( 'Index', 'Home').replace( 'index', '')]
				to_ret.remove( linkpair)
				break
		for linkpair in to_ret:
			to_rly_ret += [ linkpair[1]]
		return ' | '.join( to_rly_ret)

class Body:

	def __init__( self, site, page_name):
		self._eles = site.render()[site.name + page_name].render()

	def render( self):
		to_ret = []
		for ele in self._eles.keys():
			if self._eles[ele]['title']:
				to_ret += [ ( self._eles[ele]['distance'], '<h2>' + html.escape( self._eles[ele]['title']) + '</h2>')]
			to_ret += [ ( self._eles[ele]['distance'], '<p>' + html.escape( self._eles[ele]['content']) + '</p>')]
		to_ret = sorted( to_ret)
		to_rly_ret = []
		for ele in to_ret:
			to_rly_ret += [ ele[1]]
		return ''.join( to_rly_ret)
