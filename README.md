# WebCrawler
## Introduction
This is a self-training for web crawler, it can get information form QiQuBaiKe and do some filtering and re-organization.
Special thanks to this [article](http://cuiqingcai.com/990.html)


# Run Instruction
For this challenge, I have written my solution in both Python and Java.
## Run Instruction for Python
The program has been fully tested on python 2.7.10.
For the default input and output setting (input from ./input.json, output FIFO solution in ./fifo_output_yan_lu.json and output optimized solution in ./opt_output_yan_lu.json).
$ python main.py

If you want to use a different input/ output directory:
$ main.py -i <input file> -f <FIFO output> - o <Optimized output>

## Run Instruction for Java
The program has been fully tested on Java 1.8.0_102. Please also make json-simple-1.1.1 installed.
Open the Java program in Eclipse, run Main.java function. The default input and output directory is the same as Python. If you want to change the directory, you can enter the directory in console.

# Correct FIFO Result
The FIFO solution can generate the output exactly match the fifo_output.json. 
## Python UnitTest
Run $ python -m unittest UnitTest
The unittest will test 4 test cases, 2 test casses are for FIFO solution (using default input.json and using empty input), and 2 for optimized solution (input is the same as FIFO). The test case “test_fifo_default” can show that the FIFO solution can generate the output exactly match the fifo_output.json

# Metrics
## Assumption
Because this is a real-world problem (for either coffee shop or server request), I think instead of an algorithm design problem, the challenge looks more like a system design problem. Thus, I assume I am designing a system that may get the order at any time and I do not know when the order might come (instead I already know the order time of each order). Under this assumption, my system read the input.json based on time, in another word, I use a for look to iterate current_time and read the order from input.json only when this order' order_time <= current_time.

##The Metrics I have are:
1.	Maximize the profit
2.	Do not delay “less profitable” order too much which will increase average waiting time
3.	Implement a rate limiter, give up orders that are blocked and has been wait over time out limit

##Implementation:
Because the profit and brew time only depends on the type of drink. I designed 3 queues (deque), each queue stores unprocessed order of each drink type. 
At every minute, I do the follow steps:
1.	Check whether there is any new order placed. If so, insert the order to the back of the queue with respect to the specific coffee type.
2.	Check whether there is any “time out” order. When there is any order that has wait for over “time out” time, that means 2 things. Firstly, there might be lots of concurrent order which exceed the process ability of the coffee shop (need a rate limiter). Secondly, people who has order the coffee but did not have get the order quickly have larger possibility to give the order up (for website, this means they close the browser for the website), processing these might be useless. Based on the above two assumptions, I will pop the “time out” order out of the queue without process them. This will help reduce blocking.
3.	Check whether any barista is available. If any of them is available, then check whether there is any order in any queue. If there is at least one order, I compare the priority of the earliest order in each queue. And I will pop the order with the largest priority and process the order. The priority is calculated based on profit/ minute and waiting time. We want to process the order with highest unit time profit to maximize the total profit, however we do not want to keep delay the not profitable order and increase the waiting time. The function for calculating priority can be improved, currently I find (unit time profit)^2 * waiting time could be a good way.

## Result
My optimized algorithm can increase the total profit from 137 to 140 and can even reduce the average waiting time for each processed order from 9.4 minutes to 7.55 minutes because I give up the order which will cause blocking.
