function(doc) {
    if(doc.doc_type == "Record") {
        emit(doc.creation_date, doc);
    }
};