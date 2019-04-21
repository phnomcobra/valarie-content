db.createCollection("testCol");

db.testCol.insert(
    {
        "name": "test",
        "value": [1, 2, 3]
    }
);

db.testCol.find().pretty();

db.testCol.drop();

