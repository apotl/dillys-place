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
				to_ret += [ ( link.title(), '<span>' + html.escape( link.title()) + '</span>')]
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
		self._page_name = page_name
		self._eles = site.render()[site.name + page_name].render()

	def render( self):
		to_ret = []
		for ele in self._eles.keys():
			if self._eles[ele]['frmt'] == 'text':
				tmp_text = ''
				if self._eles[ele]['title']:
					tmp_text += '<h2>' + html.escape( self._eles[ele]['title']) + '</h2>'
				tmp_text += '<p>' + html.escape( self._eles[ele]['content']).replace( html.escape( '<br>'), '<br>') + '</p>'
				to_ret += [ ( self._eles[ele]['distance'], tmp_text)]
			elif self._eles[ele]['frmt'] == 'image':
				tmp_image = ''
				if self._eles[ele]['title']:
					tmp_image += '<h2 style="text-align: center">' + html.escape( self._eles[ele]['title']) + '</h2>'
				if self._page_name == 'index':
					tmp_image += '<img class="pho"'
				else:
					tmp_image += '<img class="pho2" style="width: 75%"'
				tmp_image += ' src="/' + self._page_name + '/assets/' + self._eles[ele]['content'] + '"></img>'
				tmp_image += '<p style="text-align: center">' + self._eles[ele]['caption'].replace( html.escape( '<br>'), '<br>') + '</p>'
				if self._page_name == 'photos':
					tmp_image += '<hr>'
				to_ret += [ ( self._eles[ele]['distance'], tmp_image)]
			elif self._eles[ele]['frmt'] == 'event':
				tmp_event = '<h2>' + html.escape( self._eles[ele]['title']) + '</h2><p>' + '<b><p>' + html.escape( self._eles[ele]['when']).replace( html.escape( '<br>'), '<br>') + '<br>' + html.escape( self._eles[ele]['where']) + '</p></b>' + '<p>' + html.escape( self._eles[ele]['content']).replace( html.escape( '<br>'), '<br>') + '</p></p><hr>'
				to_ret += [ ( self._eles[ele]['distance'], tmp_event)]
			elif self._eles[ele]['frmt'] == 'blogpost':
				tmp_blogpost = '<h1>' + html.escape( self._eles[ele]['title']) + '</h1><p class="small"><i>Posted ' + html.escape( self._eles[ele]['postdate']) + ' at ' + html.escape( self._eles[ele]['posttime']) + '</i></p><p>' + html.escape( self._eles[ele]['content']).replace( html.escape( '<br>'), '<br>') + '</p><hr>'
				to_ret += [ ( self._eles[ele]['distance'], tmp_blogpost)]
		to_ret = sorted( to_ret)
		if self._eles.keys() and self._eles[ele]['frmt'] == 'blogpost':
			to_ret = list( reversed( to_ret))
		to_rly_ret = []
		for ele in to_ret:
			to_rly_ret += [ ele[1]]
		return ''.join( to_rly_ret)
