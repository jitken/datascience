# Step 1: Read and summarize the data
data <- read.csv('seaflow_21min.csv');
summary(data)

# Step 2: Split Data into test and training
library(caret);
set.seed(0);
inTrain <- createDataPartition(data$pop, p = 0.8, list=F);
training <- data[inTrain,];
testing <- data[-inTrain,];
cat('Mean Training Time of my training set = ', mean(training$time));

# Step 3: Plot the Data
s3 <- ggplot(data, aes(x = chl_small, y = pe));
s3 + geom_point(aes(color=factor(pop)));
readline("Press <return to continue") ;

# Step 4: Train a decision tree
library(rpart);
fol <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small);
model_rpart <- rpart(fol, method="class", data=training);
print(model_rpart);

#Step 5: Evaluate Decision Tree on the Test Data
test_predict_rpart <- predict(model_rpart, testing,type='class');
acc_rpart <- mean(test_predict_rpart == testing$pop);
cat('Accurracy of Decision Tree on Test Data ',acc_rpart,"\n");

#Step 6: Build and Evaluate a Random Forest
library(randomForest);
model_randomForest <- randomForest(fol,data=training);
test_predict_randomForest <- predict(model_randomForest, testing,type='class');
acc_randomForest <- mean(test_predict_randomForest == testing$pop);
cat('Accurracy of Random Forest on Test Data ',acc_randomForest,"\n");
importance(model_randomForest);

#Step 7: Train a SVM and compare results
library(e1071);
model_svm <- svm(fol, data=training);
test_predict_svm <- predict(model_svm, testing,type='class');
acc_svm <- mean(test_predict_svm == testing$pop);
cat('Accurracy of SVM on Test Data ',acc_svm,"\n");

#Step 8: Construct confusion matrices 
table(pred = test_predict_rpart, true = testing$pop);
table(pred = test_predict_randomForest, true = testing$pop);
table(pred = test_predict_svm, true = testing$pop);

#Step 9: Sanity-Check the Data
p1 <- ggplot(data, aes(x=fsc_small)) + geom_histogram();
p2 <- ggplot(data, aes(x=fsc_perp)) + geom_histogram();
p3 <- ggplot(data, aes(x=fsc_big)) + geom_histogram();
p4 <- ggplot(data, aes(x=pe)) + geom_histogram();
p5 <- ggplot(data, aes(x=chl_small)) + geom_histogram();
p6 <- ggplot(data, aes(x=chl_small)) + geom_histogram();

source('multiplot.r');
multiplot(p1, p2, p3, p4, p5, p6, cols=2);
readline("Press <return to continue") ;

s9a <- ggplot(data, aes(x = chl_big, y = time));
s9a + geom_point(aes(color=factor(pop)));
readline("Press <return to continue") ;

filtered_data <- data[data$file_id != 208,]

s9b <- ggplot(filtered_data, aes(x = chl_big, y = time));
s9b + geom_point(aes(color=factor(pop)));
readline("Press <return to continue") ;

finTrain <- createDataPartition(filtered_data$pop, p = 0.8, list=F);
ftraining <- filtered_data[finTrain,];
ftesting <- filtered_data[-finTrain,];

fmodel_rpart <- rpart(fol, method="class", data=ftraining);
ftest_predict_rpart <- predict(fmodel_rpart, ftesting,type='class');
facc_rpart <- mean(ftest_predict_rpart == ftesting$pop);
cat('Accurracy of Decision Tree on Filtered Test Data ',facc_rpart,"\n");

fmodel_randomForest <- randomForest(fol,data=ftraining);
ftest_predict_randomForest <- predict(fmodel_randomForest, ftesting,type='class');
facc_randomForest <- mean(ftest_predict_randomForest == ftesting$pop);
cat('Accurracy of Random Forest on Filtered Test Data ',facc_randomForest,"\n");

fmodel_svm <- svm(fol, data=ftraining);
ftest_predict_svm <- predict(fmodel_svm, ftesting,type='class');
facc_svm <- mean(ftest_predict_svm == ftesting$pop);
cat('Accurracy of SVM on Filtered Test Data ',facc_svm,"\n");

