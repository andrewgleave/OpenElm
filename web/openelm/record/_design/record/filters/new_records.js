function(doc, req) {
    return (doc.doc_type == "Record" && (doc._rev.indexOf('2-') === 0));
}
