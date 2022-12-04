# helper

function createRanges(a, b)
    a_start, a_end = split(a, "-")
    b_start, b_end = split(b, "-")
    range_a = range(parse(Int, a_start), parse(Int, a_end), step=1)
    range_b = range(parse(Int, b_start), parse(Int, b_end), step=1)
    array_a = collect(range_a)
    array_b = collect(range_b)
    return array_a, array_b
end

# Part 1
function part1(input)
    sum = 0
    for line in input
        (a,b) = split(line, ",")
        array_a, array_b = createRanges(a, b)
        intersection = intersect(array_a, array_b)
        if length(intersection) == length(array_a) || length(intersection) == length(array_b)
            sum += 1
        end
    end
    return sum
end


# Part 2
function part2(input)
    sum = 0
    for line in input
        (a,b) = split(line, ",")
        array_a, array_b = createRanges(a, b)
        intersection = intersect(array_a, array_b)
        if length(intersection) > 0
            sum += 1
        end
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