function(newDoc, oldDoc, userCtx) {
    
    function isRole(role) {
        return (userCtx.roles.indexOf(role) != -1);
    }
    
    function require() {
        for(var i=0; i < arguments.length; i++) {
            var field = arguments[i];
            message = "The '" + field + "' field is required.";
            if(typeof newDoc[field] == "undefined") throw({forbidden : message});
        };
    };
    
    //no anon
    if(!userCtx.name) {
        throw({unauthorized : "Authentication required"});
    }
    
    //prevent deletion for non-admins
    if(newDoc._deleted) {
        if(!isRole('_admin')) {
            throw({forbidden : "Only admins can delete documents"});
        }
        return true;
    }
    
    require('doc_type');
    
    if(newDoc.doc_type == "Record") {
        if(!isRole('_admin')) {
            if(isRole("recorder")) {
                if(oldDoc) {
                    //adding a new attachment
                    if(!oldDoc._attachments && newDoc._attachments) {
                        return true;
                    }
                    throw({forbidden : "Recorders cannot update documents"});
                }
                return true;
            }
            throw({unauthorized : "Unknown role type"});
        }
        return true;
    }
    throw({forbidden : "Unsupported document type"});
}