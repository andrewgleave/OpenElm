function(doc) {
    if(doc.doc_type === "Record" && doc.review_date) {
        emit(doc.review_zone, doc);
    }
};