function(doc) {
    if(doc.doc_type == "Record" && doc.username) {
        emit(doc.username, doc);
    }
}
