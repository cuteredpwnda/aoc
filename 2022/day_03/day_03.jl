score_map_lower = collect(zip(collect(1:26), collect('a':'z')))
score_map_upper = collect(zip(collect(27:52), collect('A':'Z')))
score_map = vcat(score_map_lower, score_map_upper)

# Part 1
function part1(input)
    sum = 0
    for line in input
        half = trunc(Int, length(line)/2)
        left = line[1:half]
        right = line[half+1:end]
        in_both = intersect(left, right)
        sum += [x[1] for x in score_map if x[2] in in_both][1]
    end
    return sum
end

# helper, overengineered, because the input is divisisible by 3
chunk(arr, n) = [arr[i:min(i + n - 1, end)] for i in 1:n:length(arr)]

# Part 2
function part2(input)
    sets = chunk(input, 3)
    sum = 0
    for set in sets
        in_all = intersect(set...)
        sum += [x[1] for x in score_map if x[2] in in_all][1]
    end
    return sum
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end    
    @show part1(input)
    @show part2(input) 
end

main()