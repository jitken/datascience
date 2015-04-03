-- create the result directory
fs -mkdir /user/hadoop 

register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);

-- parse each line into ntriples
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

--group the n-triples by object column
subjects = group ntriples by (subject) PARALLEL 50;

-- flatten the objects out (because group by produces a tuple of each object
-- in the first column, and we want each object ot be a string, not a tuple),
-- and count the number of tuples associated with each subject
count_by_subject = foreach subjects generate flatten($0), COUNT($1) as count PARALLEL 50;

-- The x-axis is the counts associated with the subjects, and
-- The y-axis is the total number of subjects associated with each particular count.
-- group the results by these intermediate counts (x-axis values) 
counts_by_subject = group count_by_subject by (count);

-- Compute the final counts (y-axis values).
X_Y = foreach counts_by_subject generate flatten($0) as X, COUNT($1) as Y PARALLEL 50; 

--order the resulting tuples by their count in descending order
X_Y_ordered = order X_Y by (X) PARALLEL 50;

store X_Y_ordered into '/user/hadoop/p2a-results' using PigStorage();
