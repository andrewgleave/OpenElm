function(doc) {
    if(doc.doc_type == "Record" && doc.review_date) {
        emit(doc.creation_date, doc);
    }
};