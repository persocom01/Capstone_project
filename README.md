# Segmentation of Twitter Users with Machine Learning

Presentation slides [here](presentation.pdf)

## Business context

Twitter is readily available, rich source of OSINT (open-source intelligence) data that is often cited by news media organizations as being representative of the voice of the common man.

But is it really? According to Pew Research Center, of the 22% of adults in the USA who use twitter, the vast majority of tweets come from just 10% of users. In other words, twitter serves as a platform that amplifies the voice of a mere 2.2% of the US population.

Of these 2.2% of users, only 16% approve of Trump, a figure which is at odds with his national approval rating of 43% (29 Jan 2020, fivethirtyeight.com)

![twitter user distribution](./images/./images/twitter_user_distribution.jpg)

This lack of balance presents a challenge to companies seeking to use twitter as a source of customer feedback.

## Business objective

What we want is the ability to segment twitter users into groups so we are better able to hear the voice of groups that lack representation on twitter but have a large impact on our company’s bottom line.

In this case, we will examine how we can use machine learning to segment users according to their political leanings, conservative and liberal.

Once users are divided, we will examine and evaluate the findings of our machine learning model.

### Data objective

Twitter data is readily available from twitter's official API. However, the API comes with many restrictions, such as how far back you can search for tweets (7 days) and how many requests of each type you may make every 15 min.

I got data from the main dataset using the official API, however, the data for the validation dataset was acquired by first scraping twitter by using selenium to scrape for tweet ids before using twitter API to retrieve the full tweet.

The dataset is comprises carefully chosen topics which I believed would make it easy to segment users' political leanings based on their response to the topic; a kind of political litmus test. Or in other words, politically polarizing topics were chosen.

With the dataset in hand, I would manually label tweets as liberal or conservative based on the user's response to the topic. Once this was done, I would extract from the tweets a list of unique users. From these users, I would extract their user name and description, run them though multiple transformations to clean them, then use them to train a machine learning model to predict if a user is conservative or liberal.

After the model is trained, it will be tested on a validation dataset to evaluate its effectiveness.

## Tech overview

The python modules tweepy and selenium were used to extract raw data from twitter, which is then saved onto .json or .csv files.

After the data is acquired and labeled, user names and descriptions are then cleaned by running them through the following transformations:
1. Contractions are expanded.
2. Emails are removed.
3. Links are removed.
4. Gender pronouns are condensed.
5. Emojis and hashtags are spaced out so they may be tokenized later.
6. Decompose CamelCase hashtags into individual words.
7. Remove punctuations.
8. Remove single letters, numbers, and excess whitespaces.

The non emoji and hashtag part of user names are discarded, before user names and descriptions are combined into a single feature, which is run through the tfid tokenizer.

5 different models were trained and tested on the clean data:
1. Multinomial naive bayes.
2. Complement naive bayes.
3. Support Vector Machine.
4. Random forest.
5. eXtreme Gradient Boost.

The precision, recall, and accuracy of each model is compared with each other and with themselves when their predictions are tested on the validation dataset.

### Modeling results

Test set results:

| Model | Liberal precision | Liberal recall | Conservative precision | Conservative recall | Accuracy |
| ------ | ------ | ------ | ------ | ------ | ------ |
| Multinomial Naive Bayes | 77% | 96% | 93% | 64% | 82% |
| Complement Naive Bayes | 78% | 93% | 89% | 67% | 82% |
| Support Vector Machine | 75% | 97% | 95% | 60% | 81% |
| Random Forest | 77% | 92% | 87% | 66% | 80% |
| eXtreme Gradient Boost | 75% | 97% | 94% | 60% | 81% |

Validation set results:

| Model | Liberal precision | Liberal recall | Conservative precision | Conservative recall | Accuracy |
| ------ | ------ | ------ | ------ | ------ | ------ |
| Multinomial Naive Bayes | 87% | 97% | 68% | 30% | 85% |
| Complement Naive Bayes | 87% | 94% | 55% | 36% | 84% |
| Support Vector Machine | 86% | 99% | 83% | 26% | 86% |
| Random Forest | 87% | 94% | 56% | 35% | 84% |
| eXtreme Gradient Boost | 86% | 99% | 82% | 25% | 86% |

### Key findings

1. Conservatives tend to be Trump voters, religious, patriotic, and married.
2. Liberals tend to be anti-Trump, narcissistic, of minority races, and support LGBT.
3. The precision of the models in predicting conservatives tends to fall sharply when applied to areas outside the USA.

### Key problems

1. Twitter API limitations.
2. Time taken to label data.
3. Lack of diversity in dataset due to time taken to label data.
4. Non-English languages.
5. A significant proportion of users have no descriptions.

## Conclusion

- The model proved to be reasonably accurate in predicting a person’s political leaning using their
description and user name with an accuracy of over 80% on the test and validation datasets.

- As the goal here to amplify the voice of a twitter minority, models with high precision on the minority group are preferred.

- However, many of the features the model used to predict a person's political leaning are mainly applicable to the USA, showing that the model ought to be trained on more diverse datasets.

- The approach to gathering data and solving this problem can be applied to similar issues, such as trying to deduce the sex of a twitter user, and multiple models can be stacked to identify more niche groups. For instance, if one wants to know what conservative + women think.
