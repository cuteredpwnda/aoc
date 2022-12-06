# Part 1
function part1(input)
    for i in eachindex(input[1])
        unique_chars = Set(input[1][i:i+3])
        if length(unique_chars) == 4
            return i+3
        end
    end
end

# Part 2
function part2(input)
    for i in eachindex(input[1])
        unique_chars = Set(input[1][i:i+13])
        if length(unique_chars) == 14
            return i+13
        end
    end
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    @show part1(input)
    @show part2(input) 
end

main()