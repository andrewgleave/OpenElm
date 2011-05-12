function(doc) { 
  if (doc.geometry && doc.properties) {
    emit(doc.geometry || {type: 'Point', coordinates: [0,0]}, 
        {'title': (typeof(doc.properties.title) == 'undefined') ? 'Untitled' : doc.properties.title, 
        'subtitle': (typeof(doc.properties.subtitle) == 'undefined') ? 'None' : doc.properties.subtitle})
    }
}