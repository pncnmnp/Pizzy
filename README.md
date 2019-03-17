## Pizzy - A Pizza delivery chatbot
![pizzy](https://github.com/pncnmnp/Pizzy/blob/master/FrontEnd/static/pizzy.png)

## Description
**This project is created during [Mumbai Hackathon](https://mumbaihackathon.in/).** <br>This _chatbot_ is divided into three parts:
* `Parser` ( implemented **from scratch** without any `NLP` or `ML` libraries. ). It contains scope for Universals or Keywords, **two-level** parser ( one for `screening` and other for `order placement` ), curse word detection, sentiment analysis ( in `ispositive.py` file ) and generic response generator.
* `Customer` contains customer priority ( using `K Nearest Neighbour`), customer database, bill generation, referral code support and customer support ( by detecting customer's annoyance level ).
* `Datasets` : A lot of the datasets are hand-curated like `welcome.yml` ( which can be used universally by food delivering products ), `pizza_data.csv` ( used for `KNN` implementation ) and menu ordering datasets (`pizzas.yml`, `sides.yml`, `beverages.yml`).
* We are also using Google Distance Matrix API to detect real-time food-delivery duration.

## Libraries
See the `requirements.txt` file.

## How to run
Enter in command line:
<br>
`python3.6 customer.py`

To see how our parser works use:
<br>
`python3.6 parser.py`

## Terminal Output
![terminal-output](https://github.com/pncnmnp/Pizzy/blob/master/FrontEnd/terminal-output.gif)

## Contributers
* Parth - [pncnmnp](https://github.com/pncnmnp)
* Dhruvam - [iotarepeat](https://github.com/iotarepeat)
* Sahil - [CoderSsVartak](https://github.com/CoderSsVartak)
* Devesh - [dev2919](https://github.com/dev2919)
