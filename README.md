# How to run
`Python 3` is required for running this project.
In order to run the project you have to use the command bellow. Here `<input 1>` is the path to donations info, `<input 2>` is the path to percentile file and `<output>` is the path to write the results to.
>    python3 analytics.py <input 1> <input 2> <output>
# Files Information
-- `analytics.py`: the main file which does the calculations.
-- `models.py`: contains helper classes written in order to store the information and process them.
-- `field_positions.json`: contains index positions to the fields which are required among the data given.
# Solving Approach
There is a class called `Donation` which stores information about each donation and a class called `Result` which stores information needed to be printed in the output.

Each line representing a donation is read from the input and stored as a `Donation` object in a list. At the same time the previous donations are searched to find the donations with the same `name` and `zip code` and prior `date years`. The found results are marked as repeated donations and for the repeated donations all the donors with the same `CMTE_ID`, `ZIP_CODE` and `year` are stored in a `Result` object.

When reading and processing the data is finished, the found results are written to the output file in the same order as they were found.