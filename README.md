# Hypertrophy Exercise App Post

This project models data that is used in a current production app called Hypertrophy which is an exercise app aimed at building muscle. 

## 6 Questions

How many exercises use a barbell?
How many users are there?
How many different pieces of equipment are there?
What is the dominant gender of users?
What equipment is most commonly used?
On what date is the next workout scheduled?
What is the average duration of a workout?

## Example Response

Question: How many exercises use a barbell?

Response:
The concluded result from this query returned only a single value: [(3,)].

This means that there are 3 exercises in the database that use a barbell as required equipment. Quite easy and simple, isn't it?

Here is how we would present it in a table:

| Number of Exercises Using Barbell |
| --------------------------------- |
| 3                                 |

In this table, there's just one data - the number '3' - which represents the count of barbell-using exercises in your database based on the criteria of the query.

Remember that this count is based on the information available at the time the query was performed. If more exercises using a barbell have been added since, or if some have been deleted, the count might now be different.

## Schema

![Mars DB_Models](https://github.com/user-attachments/assets/16999ad7-37a6-44a7-81a6-8ae9796acc43)


## Question that it tripped up on
We mostly had trouble when we initially were not providing enought context for the API call. We originally were not giving the response call the text of what was asked in the initial query. This resulted in some weird answers where it would give the correct results of the query but not know what the data meant. For instance, with the above question, it would tell us that the response was 3 but that it could not tell us what that signified. It wasn't until we passed along both the create table statements and the original question that was asked that we started getting friendly answers that were intelligible to users. 



## Conclusion
Our findings were that LLM's are getting quite good at making queries, at least when the schema isn't deeply complicated. However, if you don't give it enough context (as it would be with humans) it has trouble interpereting the results of that data. It also helps immensely to give it the create table statements in order for it to have hard knowledge of what the schema is instead of trying to manually describe what the shapes of the data are. 