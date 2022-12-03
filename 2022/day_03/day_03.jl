# read input
input = open(joinpath(@__DIR__, "input", "input.txt")) do f
    readlines(f)
end

score_map_lower = collect(zip(collect(1:26), collect('a':'z')))
score_map_upper = collect(zip(collect(27:52), collect('A':'Z')))
score_map = vcat(score_map_lower, score_map_upper)

# Part 1
function part1(input)
    value_list = []
    for line in input
        half = trunc(Int, length(line)/2)
        left = line[1:half]
        right = line[half+1:end]
        in_both = intersect(left, right)
        value = [x[1] for x in score_map if x[2] in in_both][1]
        push!(value_list, value)
    end
    return sum(value_list)
end

# helper
chunk(arr, n) = [arr[i:min(i + n - 1, end)] for i in 1:n:length(arr)]

# Part 2
function part2(input)
    sets = chunk(input, 3)
    value_list = []
    for set in sets
        in_all = intersect(set...)
        value = [x[1] for x in score_map if x[2] in in_all][1]
        push!(value_list, value)
    end
    return sum(value_list)
end

res = part1(input)
println("Part 1: $res")

res2 = part2(input)
println("Part 2: $res2")