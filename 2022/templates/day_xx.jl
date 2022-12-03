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
    @show part1(input)
    @show part2(input) 
end

main()