# Metropolis-Hastings Algorithm for Finding the Minimum Variance Portfolio (MVP)

In this example, we apply the Metropolis-Hastings algorithm to identify the minimum variance portfolio (MVP) using stock data from 2024. While the algorithm is generally less efficient than closed-form solutions—especially in the absence of constraints beyond the full investment condition—it provides flexibility when additional constraints are introduced.

By incorporating constraints into the energy function (e.g., treating violations as higher-energy states), the algorithm can naturally handle more complex portfolio optimization scenarios that closed-form solutions struggle with.
