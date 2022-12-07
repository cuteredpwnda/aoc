# Part 1
function part1(input)
    return nothing
end

# Part 2
function part2(input)
    return nothing
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    p1 = part1(input)
    p2 = part2(input)
    @show p1
    @show p2
end

main()