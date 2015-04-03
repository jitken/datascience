-- create the result directory
fs -mkdir /user/hadoop 

register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the data file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray);

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

filtered = FILTER ntriples BY (subject matches '.*rdfabout\\.com.*') PARALLEL 50;

filtered2 = foreach filtered generate * PARALLEL 50; 
joined = join filtered by object, filtered2 by subject PARALLEL 50;
joined_distinct = distinct joined PARALLEL 50;

-- store the results in the folder /user/hadoop/p3B-results
store joined_distinct into '/user/hadoop/p3-results' using PigStorage();
