# ELEC0138_Project
Repository for ELEC0138 Project 2023/2024 Group O

## Coursework 1
We consider the scenario of a user and a ecommerce website, in which both interact with each other. 
1. Assets
    - User data: The user, by interacting with the website, is providing information such as search queries, purchase history, and other sentsitive personal information sich as name, date of birth, payment information... that the website may use to identify the type of customer he is.
    - Machine Learning (ML) model: The company behind the website uses a ML algorithm to predict the customer needs by using data collected while the users navigate the website.
2. Threats
    - ML model of the website: The ML model that the company uses poses a threat to our privacy as they collect our data while using of the website tom improve their marketing strategies, sell our information or other purposes.
    - Data poisoning: A user concerned with his privacy, may try to purposedly poson the data so that the ML model trains on inaccurate data that does not reflect reality, hindering the predictions of the model. Another threat could be a vendor that sells a product in the ecommerce platform, and is interested in artificially improving the SEO of their product by simulaating high interest in the product.
3. Impact
    - Loss of privacy: ML are highly dependent on data collection to make personalised reccomendations.
    - Inaccurate model: Data poisoning can lead to incorrect predictions that can affect users that agree to send their data for personalised recommendations, as well as impacting the sales perfomance of the company.
    - Inaccurate SEO: SEO poisoning can lead to loss of business to other vendors in the platform, it can impact the experience of the users, and a reputational loss from part of the platform.
4. Priority
    - Preserving the privacy of the users is more important than the ecommerce sales and user experience. Data privacy is very important can potentially lead to bigger consequences such as manipulation, surveillance, etc.
5. Attacks
    - ML models: A website that collects data from their users to feed to a ML for predicting user needs. The wesie will register the search queries done by the user. These quesries will be used to train a ML model that will later predict what other items the user is likely to be interested in.
    - Data poisoning attack: A script to automatically manipulate the data collected on the website with random data. The script will perform random search queries about products available in the website.
    - SEO attack: A script that automatically searches the products sold by one vendor to improve its positioning in the search queries. The script will perform the same search queries about some products available in the website.

## Coursework 2
1. Mitigation
    - Data poisoning: An effective method to prevent tracking is to provide inaccurate data to the website so it is not able to discern what data is real and what is not. This will impact the performance of their tracking algorithms.
    - Rate limit: One way to prevent data poisoning is to limit the rate in which users can perform search queries. This prevents for autmated scripts to run and poison the data.
    - Outlier detection: Another way to prevent data poisoning is detect and remove outliers that do not behave like other users.
    - Federated learning: Instead of training a global model for all users, a mod
    - ReCaptcha: A general solution to the poisoning attacks is to verify that the user is human and not a robot.
2. Analysis
3. Considerations