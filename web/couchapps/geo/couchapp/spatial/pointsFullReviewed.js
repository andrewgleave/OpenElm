function(doc){
    if(doc.geometry && doc.review_date){
        emit(doc.geometry, doc);
    }
}
