# [Day 2](https://adventofcode.com/2021/day/6)
## What have I done?
### Step 1 (Prerequisites)
I have used curl to get the input with `curl "https://adventofcode.com/2021/day/6/input" --cookie "session=***" -o raw_input.txt`, `***` being the session cookie ofc.

### Step 2 (Part 1)
- Read the input file into a list
- iterate elements in this list
  - split the element of this list into a string `direction` and an integer `amount`
  - switch cases for `direction`
    - increase or decrease `positionX` or `positionY` as described in the riddle
- multiply `positionX` and `positionY`
### Step 3 (Part 2)
- Read the input file into a list
- iterate elements in this list
  - split the element of this list into a string `direction` and an integer `amount`
  - switch cases for `direction`
    - if `direction` is `forward`, increase `positionX` by `amount` and `positionY` by `amount * aim`
    - if `direction` is `up` or `down`, increase or decrease `aim` by `amount`
- multiply positionX and positionY