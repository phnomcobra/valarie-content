db.createUser(
    {
        user: "root",
        pwd: "password",
        roles:  
            [
                "readWrite", 
                "dbAdmin"
            ] 
    }
);