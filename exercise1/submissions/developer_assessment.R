require(plyr)

folder.path <- "C:/Users/luked/Dropbox/CEP/cep-developer-assessment-master/"

##################################
#\_(-_-)_/  EXERCISE 1  \_(~_~)_/#
##################################

#set the working directory
setwd(paste0(folder.path, "exercise1/input"))
#open the csv file
xl <- read.csv("xl.csv")

#these are the column names of the questions
q.names <- c("fldimp", "undrfld", "advknow", "pubpol",
             "comimp", "undrwr", "undrsoc", "orgimp",
             "undrorg")
#just the indicies of the question columns, for later reference
q.cols <- which(colnames(xl) %in% q.names)

#separate data frame of just the question data
q.data <- xl[,q.cols]

#cast all the question data to ints
q.data <- apply(q.data, 1:2, as.integer)

#convert 77 and 88 entries to NA
q.data[q.data == 77 | q.data == 88] <- NA

#compute the mean response on each question per client
fdntext <- as.data.frame(xl[,colnames(xl) == "fdntext"])
colnames(fdntext) <- "fdntext"
fdn.qs <- cbind(fdntext, q.data)

#there is probably a better way to do this
fdn.mean <- ddply(fdn.qs, "fdntext", summarize,
                  fldimp = mean(fldimp, na.rm = T),
                  undrfld = mean(undrfld, na.rm = T),
                  advknow = mean(advknow, na.rm = T),
                  pubpol = mean(pubpol, na.rm = T),
                  comimp = mean(comimp, na.rm = T),
                  undrwr = mean(undrwr, na.rm = T),
                  undrsoc = mean(undrsoc, na.rm = T),
                  orgimp = mean(orgimp, na.rm = T),
                  undrorg = mean(undrorg, na.rm = T))

#output the means
out.path1 <- paste0(folder.path, "exercise1/submissions")
write.csv(fdn.mean, paste(out.path1, "mean.csv", sep = "/"), row.names = F)

#next do some other stats for each question (not split by foundation):
fdn.stats <- data.frame(matrix(ncol = 9, nrow = 8))
colnames(fdn.stats) <- colnames(fdn.mean[,-1])
#count (not sure what this is counting)
fdn.stats[1,] <- apply(fdn.mean[,-1], 2,
                       function(x) length(which(!is.na(x))))
#mean
fdn.stats[2,] <- apply(fdn.mean[,-1], 2, mean, na.rm=T)
#standard deviation (std)
fdn.stats[3,] <- apply(fdn.mean[,-1], 2, sd, na.rm=T)
#min
fdn.stats[4,] <- apply(fdn.mean[,-1], 2, min, na.rm=T)
#25%
fdn.stats[5,] <- apply(fdn.mean[,-1], 2, quantile, probs = .25, na.rm=T)
#50%
fdn.stats[6,] <- apply(fdn.mean[,-1], 2, quantile, probs = .5, na.rm=T)
#75%
fdn.stats[7,] <- apply(fdn.mean[,-1], 2, quantile, probs = .75, na.rm=T)
#max
fdn.stats[8,] <- apply(fdn.mean[,-1], 2, max, na.rm=T)

#fill out the first column (holding stat names)
stat.names <- as.data.frame(c("count", "mean", "std", "min",
                "25%", "50%", "75%", "max"))

fdn.stats <- cbind(stat.names, fdn.stats)
colnames(fdn.stats)[1] <- ""

#output the second csv
write.csv(fdn.stats, paste(out.path1, "stats.csv", sep="/"), row.names = F)


##################################
#\_(-_-)_/  EXERCISE 2  \_(~_~)_/#
##################################

#we can get the percentile by dividing their rank among the foundations
#by the total number of foundations
fdn.pct <- as.data.frame(apply(fdn.mean[,-1], 2,
                               function(x) 1-rank(x)/length(x)))
fdn.pct <- cbind(fdn.mean$fdntext, fdn.pct)
colnames(fdn.pct)[1] <- fdntext

out.path2 <- paste0(folder.path, "exercise2/submissions")

write.csv(fdn.pct, paste(out.path2, "pct.csv", sep = "/"))



##################################
#\_(-_-)_/  EXERCISE 3  \_(~_~)_/#
##################################


