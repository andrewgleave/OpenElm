function(doc) {
    if(doc.doc_type == "Record" && doc.review_date) {
        emit(doc.username, 1);
    }
}