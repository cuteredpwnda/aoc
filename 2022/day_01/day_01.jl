# read input
input = open(joinpath(@__DIR__, "input", "input.txt")) do f
    readlines(f)
end

# Part 1
function part1(input)
    calories_list = []
    i = 0
    for cal in input
        if cal == ""
            i += 1
            continue
        else
            push!(calories_list, (i, parse(Int, cal)))
        end
    end

    # sum up the calories for each (i, calories) and return the max
    sums = [(j, sum([calories for (i, calories) in calories_list if i == j])) for j in 0:i]
    max = maximum([calories for (i, calories) in sums])
    return (max, sums)
end

# Part 2
function part2(input)
    sorted = sort(input, by=x -> x[2])
    # take the last three elements and sum them up
    return sum([calories for (i, calories) in sorted[end-2:end]])
end

# Part 1
(max, sums) = part1(input)
println(max)

# Part 2 works with the sums of part 1
last_three_sum = part2(sums)
println(last_three_sum)