CREATE EXTERNAL TABLE mongo_tweets (
    id STRING,
    data STRING
)
STORED BY 'org.apache.hadoop.hive.mongodb.MongoStorageHandler'
WITH SERDEPROPERTIES (
    "mongo.uri"="mongodb://mongodb:27017/twitter.tweets"
)
TBLPROPERTIES (
    "mongo.input.format"="com.mongodb.hadoop.MongoInputFormat",
    "mongo.output.format"="com.mongodb.hadoop.MongoOutputFormat"
);
