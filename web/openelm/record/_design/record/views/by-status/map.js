function(doc) {
    if(doc.doc_type == "Record") {
        emit(doc.status, doc);
    }
};