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
    return nothing
end

(max, sums) = part1(input)
