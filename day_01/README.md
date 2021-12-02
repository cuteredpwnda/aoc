# [Day 1](https://adventofcode.com/2021/day/1)
## What have I done?
### Step 1 (Prerequisites)
I have used curl to get the input with `curl "https://adventofcode.com/2021/day/1/input" --cookie "session=***" -o raw_input.txt`, ``***` being the session cookie ofc.

### Step 2 (Part 1)
- Read the input file into a list
- iterate the input list and calculate the `delta` between the `current` and the `previous` input.
- if its positive, add `1` to the counter
- return the counter

### Step 3 (Part 2)
- Read the input list from Part 1 (will not do that anymore, should be the same type of input)
- iterate the input list and calculate the `delta` between the sum of the first window and the second window
  - To do that, I take sublists out of the list, starting with current iterator and ending 3 further, for the second window I add one to the iterator.
  - Then I used `fold` to add each element in the sublist.
- if its positive, add `1` to the counter
- return the counter
