function printEditList( mems)
{
	var list = "<select><option value=\"\">Choose something to edit...</option>";
	for( var i = 0; i < mems.length; i++)
	{
		list += "<option value=\"" + mems[i] + "\">" + mems[i] + "</option>";
	}
	list += "</select>";
	return list;
}
function escDoubles( str)
{
	return unescape( str);
}

function clearText( id)
{
	document.getElementById( id).value = "";
}
